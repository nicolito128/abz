"""
Módulo con clases y funciones útiles para trabajar con archivos IO.
"""

from typing import BinaryIO

from reader import ReadCloser
from writer import WriteCloser


class File(ReadCloser, WriteCloser):
    """
    Archivo en disco, legible y escribible.

    `mode` sigue las reglas de `open` en binario: "rb" (por defecto),
    "wb", "ab", "r+b", "w+b", etc. Si el modo no permite una operación,
    Python lanza `io.UnsupportedOperation`.
    """

    def __init__(self, path: str, mode: str = "rb") -> None:
        if "b" not in mode:
            raise ValueError("File solo trabaja en modo binario")

        with open(path, mode) as file:
            self._file = file

    def read(self, n: int = -1) -> bytes:
        return self._file.read(n)

    def write(self, data: bytes) -> int:
        return self._file.write(data)

    def close(self) -> None:
        self._file.close()

    def closed(self) -> bool:
        return self._file.closed
