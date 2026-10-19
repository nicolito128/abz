"""
Módulo con las interfaces necesarias para implementar un codificador.
"""

from abc import ABC, abstractmethod

from reader import Reader
from writer import Writer


class Encoder(ABC):
    """Encoder permite codificar datos."""

    @abstractmethod
    def encode(self, dst: Writer, src: Reader) -> bytes:
        """
        encode lee los datos provenientes del reader 'src' (fuente) y
        codifica el contenido en el write 'dst' (destino).
        """
        pass
