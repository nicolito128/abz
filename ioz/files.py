"""
Implementación io.ReadWriteCloser para el trabajo con archivos del sistema.
"""

from typing import IO, Any, override

from .ioz import ReadWriteCloser


class File(ReadWriteCloser):
    """
    Archivo en disco, legible y escribible.

    `mode` sigue las reglas de `open` en binario: "rb" (por defecto),
    "wb", "ab", "r+b", "w+b", etc. Si el modo no permite una operación,
    Python lanza `io.UnsupportedOperation`.
    """

    _file: IO[Any]

    def __init__(self, path: str, mode: str = "rb") -> None:
        if "b" not in mode:
            raise ValueError("File solo trabaja en modo binario")

        self._file = open(path, mode)

    @override
    def read(self, n: int = -1) -> bytes:
        return self._file.read(n)

    @override
    def write(self, data: bytes) -> int:
        return self._file.write(data)

    @override
    def close(self) -> None:
        self._file.close()

    @override
    def closed(self) -> bool:
        return self._file.closed
