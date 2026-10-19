"""
Módulo con las interfaces necesarias para implementar un decodificador.
"""

from abc import ABC, abstractmethod

from reader import Reader
from writer import Writer


class Decoder(ABC):
    """Decoder permite decodificar datos."""

    @abstractmethod
    def decode(self, dst: Writer, src: Reader) -> bytes:
        """
        decode lee los datos provenientes del reader 'src' (fuente) y
        decodifica el contenido en el writer 'dst' (destino).
        """
        pass
