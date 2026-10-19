"""
Módulo con la interfaz de un codec: algo que codifica y decodifica.
"""

from encoder import Encoder
from decoder import Decoder


class Codec(Encoder, Decoder):
    """Codec agrupa un Encoder y un Decoder en una sola interfaz."""
    pass
