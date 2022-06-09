import asyncio
import logging
from .net.package import Package
from .protocol import ApiProtocol


class ApiClient:

    def __init__(self):
        self._connecting = False
        self._protocol = None

    def close(self):
        if self._protocol and self._protocol.transport:
            self._protocol.transport.close()
        self._protocol = None

    def is_connected(self):
        return self._protocol is not None and self._protocol.is_connected()

    def is_connecting(self):
        return self._connecting

    async def connect(self, host, port):
        loop = asyncio.get_event_loop()
        conn = loop.create_connection(
            ApiProtocol,
            host=host,
            port=port
        )
        self._connecting = True

        try:
            _, self._protocol = await asyncio.wait_for(conn, timeout=10)
        except Exception as e:
            logging.error(f'connecting to mh failed: {e}')
        else:
            pass

        finally:
            self._connecting = False

    async def get_path(self, container_ids, host_ids, path, metrics, expr):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATH,
            data=[container_ids, host_ids, path, metrics, expr]
        )
        return await self._request(pkg)

    async def get_path_set(self, container_ids, host_ids, path, metric):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATH_SET,
            data=[container_ids, host_ids, path, metric]
        )
        return await self._request(pkg)

    async def get_paths(self, container_ids, host_ids=[], paths=[]):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATHS,
            data=[container_ids, host_ids, paths]
        )
        return await self._request(pkg)

    async def get_alerts(self, container_ids, host_ids=[], paths=[],
                         user_id=None, all_messages=False):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS,
            data=[container_ids, host_ids, paths, user_id, all_messages]
        )
        return await self._request(pkg)

    async def get_alert(self, alert):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERT,
            data=[alert]
        )
        return await self._request(pkg)

    async def alerts_assign(self, alert, message, user_id, assign_user_id, ts):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_ASSIGN,
            data=[alert, message, user_id, assign_user_id, ts]
        )
        return await self._request(pkg)

    async def alerts_message(self, alert, message, user_id, ts):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_MESSAGE,
            data=[alert, message, user_id, ts]
        )
        return await self._request(pkg)

    async def alerts_close(self, alert, message, user_id, ts):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_CLOSE,
            data=[alert, message, user_id, ts]
        )
        return await self._request(pkg)

    async def send(self, path, rows, ts):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_DATA,
            data=[path, rows, ts]
        )
        return await self._request(pkg)

    async def _request(self, pkg):
        if self._protocol and self._protocol.transport:
            try:
                resp = await self._protocol.request(pkg, timeout=10)
            except Exception as e:
                logging.error(e)
            else:
                return resp
