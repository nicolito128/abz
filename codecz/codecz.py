"""
Módulo que define las interfaces necesarias para un codec: codificadores (Encoder) y decodificadores (Decoder).
"""

from abc import ABC, abstractmethod

from ioz import Writer, Reader


class Encoder(ABC):
    """Encoder permite codificar datos."""

    @abstractmethod
    def encode(self, dst: Writer, src: Reader) -> bytes:
        """
        encode lee los datos provenientes del reader 'src' (fuente) y
        codifica el contenido en el write 'dst' (destino).
        """


class Decoder(ABC):
    """Decoder permite decodificar datos."""

    @abstractmethod
    def decode(self, dst: Writer, src: Reader) -> bytes:
        """
        decode lee los datos provenientes del reader 'src' (fuente) y
        decodifica el contenido en el writer 'dst' (destino).
        """


class Codec(Encoder, Decoder, ABC):
    """Codec agrupa un Encoder y un Decoder en una sola interfaz."""
