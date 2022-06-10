import asyncio
import logging
from typing import Optional
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

    def is_connected(self) -> bool:
        return self._protocol is not None and self._protocol.is_connected()

    def is_connecting(self) -> bool:
        return self._connecting

    async def connect(self, host: str, port: int):
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

    async def get_path(self, container_ids: list, host_ids: list, path: list,
                       metrics: Optional[list] = None,
                       expr: Optional[dict] = None) -> list:
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATH,
            data=[container_ids, host_ids, path, metrics, expr]
        )
        return await self._request(pkg)

    async def get_path_set(self, container_ids: list, host_ids: list,
                           path: list, metric: str) -> list:
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATH_SET,
            data=[container_ids, host_ids, path, metric]
        )
        return await self._request(pkg)

    async def get_paths(self, container_ids: list,
                        host_ids: Optional[list] = [],
                        paths: Optional[list] = []) -> list:
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_PATHS,
            data=[container_ids, host_ids, paths]
        )
        return await self._request(pkg)

    async def get_alerts(self, container_ids: list,
                         host_ids: Optional[list] = [],
                         paths: Optional[list] = [],
                         user_id: Optional[int] = None,
                         all_messages: Optional[bool] = False) -> list:
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS,
            data=[container_ids, host_ids, paths, user_id, all_messages]
        )
        return await self._request(pkg)

    async def alerts_assign(self, alerts: list, message: str, user_id: int,
                            assign_user_id: int, ts: int):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_ASSIGN,
            data=[alerts, message, user_id, assign_user_id, ts]
        )
        return await self._request(pkg)

    async def alerts_message(self, alerts: list, message: str, user_id: int,
                             ts: int):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_MESSAGE,
            data=[alerts, message, user_id, ts]
        )
        return await self._request(pkg)

    async def alerts_close(self, alerts: list, message: str, user_id: int,
                           ts: int):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_ALERTS_CLOSE,
            data=[alerts, message, user_id, ts]
        )
        return await self._request(pkg)

    async def send(self, path: list, rows: dict, ts: int):
        pkg = Package.make(
            ApiProtocol.PROTO_REQ_DATA,
            data=[path, rows, ts]
        )
        return await self._request(pkg)

    async def _request(self, pkg: Package):
        if self._protocol and self._protocol.transport:
            try:
                resp = await self._protocol.request(pkg, timeout=10)
            except Exception as e:
                logging.error(e)
            else:
                return resp
