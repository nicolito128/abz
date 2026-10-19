"""
Módulo con clases y funciones útiles para trabajar con archivos IO.
"""

from typing import BinaryIO

from reader import ReadCloser
from writer import WriteCloser


class FileReader(ReadCloser):
    def __init__(self, path: str) -> None:
        self._file: BinaryIO = open(path, "rb")

    def read(self, n: int = -1) -> bytes:
        return bytes(self._file.read(n))

    def close(self) -> None:
        self._file.close()

    def closed(self) -> bool:
        return self._file.closed


class FileWriter(WriteCloser):
    def __init__(self, path: str) -> None:
        self._file: BinaryIO = open(path, "wb")

    def write(self, data: bytes) -> int:
        return self._file.write(data)

    def close(self) -> None:
        self._file.close()

    def closed(self) -> bool:
        return self._file.closed
