"""
Módulo con las interfaces que definen a una clase capaz de leer un stream de datos.
"""

from abc import ABC, abstractmethod


class Reader(ABC):
    """Interfaz para leer los bytes de un stream."""

    @abstractmethod
    def read(self, n: int = -1) -> bytes:
        """Lee hasta 'n' bytes. Si n es -1, lee todo lo que quede.
        Devuelve vacío (b"") cuando el stream se terminó."""
        pass


class ReadCloser(Reader):
    """Interfaz para leer los bytes de un stream y liberar el recurso al finalizar."""

    @abstractmethod
    def close(self) -> None:
        """Libera los recursos asociados al stream."""
        pass

    @abstractmethod
    def closed(self) -> bool:
        """Indica si el stream ya fue cerrado."""
        pass
