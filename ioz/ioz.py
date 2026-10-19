"""
Módulo de entrada y salida para ABZ. Define las interfaces necesarias de lectura (Reader) y escritura (Writer).
"""

from abc import ABC, abstractmethod


class Reader(ABC):
    """Interfaz para leer los bytes de un stream."""

    @abstractmethod
    def read(self, n: int = -1) -> bytes:
        """Lee hasta 'n' bytes. Si n es -1, lee todo lo que quede.
        Devuelve vacío (b"") cuando el stream se terminó."""


class ReadCloser(Reader, ABC):
    """Interfaz para leer los bytes de un stream y liberar el recurso al finalizar."""

    @abstractmethod
    def close(self) -> None:
        """Libera los recursos asociados al stream."""

    @abstractmethod
    def closed(self) -> bool:
        """Indica si el stream ya fue cerrado."""


class Writer(ABC):
    """Interfaz para escribir bytes en un stream."""

    @abstractmethod
    def write(self, data: bytes) -> int:
        """Escribe los bytes de 'data' en el stream subyacente.
        Devuelve la cantidad de bytes escritos."""


class WriteCloser(Writer, ABC):
    """Interfaz para escribir bytes en un stream y liberar el recurso al finalizar."""

    @abstractmethod
    def close(self) -> None:
        """Libera los recursos asociados al stream."""

    @abstractmethod
    def closed(self) -> bool:
        """Indica si el stream ya fue cerrado."""


class ReadWriter(Reader, Writer, ABC):
    """Interfaz para aquellas clases que implementan Reader y Writer."""

class ReadWriteCloser(ReadCloser, WriteCloser, ABC):
    """Interfaz para aquellas clases que implementan ReadCloser y WriterCloser"""
