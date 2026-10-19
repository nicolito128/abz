"""
Módulo con clases y funciones útiles para trabajar con streams de bytes.
"""

from reader import ReadCloser
from writer import WriteCloser


class BytesReader(ReadCloser):
    def __init__(self, data: bytes) -> None:
        self._data = data
        self._pos = 0
        self._closed = False

    def read(self, n: int = -1) -> bytes:
        if self._closed:
            raise ValueError("I/O operation on closed stream")
        if n < 0:
            n = len(self._data) - self._pos
        chunk = self._data[self._pos: self._pos + n]
        self._pos += len(chunk)
        return chunk

    def close(self) -> None:
        self._closed = True

    def closed(self) -> bool:
        return self._closed


class BytesWriter(WriteCloser):
    def __init__(self, buff: bytearray | None = None) -> None:
        self._buffer = buff if buff is not None else bytearray()
        self._closed = False

    def write(self, data: bytes) -> int:
        if self._closed:
            raise ValueError("I/O operation on closed stream")
        self._buffer.extend(data)
        return len(data)

    def data(self) -> bytes:
        return bytes(self._buffer)

    def close(self) -> None:
        self._closed = True

    def closed(self) -> bool:
        return self._closed
