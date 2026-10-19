"""
Módulo con las interfaces que definen a una clase capaz de escribir en un stream de datos.
"""

from abc import ABC, abstractmethod


class Writer(ABC):
    """Interfaz para escribir bytes en un stream."""

    @abstractmethod
    def write(self, data: bytes) -> int:
        """Escribe los bytes de 'data' en el stream subyacente.
        Devuelve la cantidad de bytes escritos."""
        pass


class WriteCloser(Writer):
    """Interfaz para escribir bytes en un stream y liberar el recurso al finalizar."""

    @abstractmethod
    def close(self) -> None:
        """Libera los recursos asociados al stream."""
        pass

    @abstractmethod
    def closed(self) -> bool:
        """Indica si el stream ya fue cerrado."""
        pass
