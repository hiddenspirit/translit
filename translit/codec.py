import codecs

from .downgrade import encode_factory
from .upgrade import decode_factory


def search_function(encoding):
    parts = encoding.split("/")
    if len(parts) > 1 and parts[1] == "translit":
        e = parts[0]
        encode_func = encode_factory(e)
        decode_func = decode_factory(e, parts[2] if len(parts) > 2 else None)
        return codecs.CodecInfo(encode_func, decode_func)


codecs.register(search_function)
