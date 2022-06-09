import struct
import msgpack


class Package(object):

    __slots__ = ('length', 'pid', 'tp', 'data', 'total')

    st_package = struct.Struct('<IHBB')

    def __init__(self, barray=None):
        if barray is None:
            return

        self.length, self.pid, self.tp, checkbit = \
            self.__class__.st_package.unpack_from(barray, offset=0)
        if self.tp != checkbit ^ 255:
            raise ValueError('invalid checkbit')
        self.total = self.__class__.st_package.size + self.length
        self.data = None

    @classmethod
    def make(cls, tp, data=b'', pid=0, is_binary=False):
        pkg = cls()
        pkg.tp = tp
        pkg.pid = pid

        if is_binary is False:
            data = msgpack.packb(data)

        pkg.data = data
        pkg.length = len(data)
        return pkg

    def to_bytes(self):
        header = self.st_package.pack(
            self.length,
            self.pid,
            self.tp,
            self.tp ^ 0xff)

        return header + self.data

    def extract_data_from(self, barray):
        self.data = None
        try:
            if self.length:
                data = barray[self.__class__.st_package.size:self.total]
                self.data = msgpack.unpackb(data)

        finally:
            del barray[:self.total]

    def __repr__(self):
        return '<id: {0.pid} size: {0.length} tp: {0.tp}>'.format(self)