import json
import time
from typing import Any

import brotli

from source.handlers.file_handler import load_file


def is_json_serializable(value: Any) -> bool:
    """
    Check if a value is JSON serializable.

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is JSON serializable, False otherwise.
    """
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False



# import mdgpack
#
#
# def compress_json_to_msgpack(json_data):
#     # Convert JSON string to Python object if it's not already
#     if isinstance(json_data, str):
#         data = json.loads(json_data)
#     else:
#         data = json_data
#
#     # Compress data using MessagePack
#     compressed_data = msgpack.packb(data)
#
#     return compressed_data
#
#
# def decompress_msgpack_to_json(compressed_data):
#     # Decompress MessagePack data
#     decompressed_data = msgpack.unpackb(compressed_data)
#
#     return decompressed_data

data = load_file("level_0.json", "levels")# dict

start = time.time()
compressed_data = brotli.compress(json.dumps(data).encode("utf-8"))
end = time.time()-start


print (f"data compressed in: {end}s. original size: {len(str(data))} compressed size: {len(compressed_data)}")
print (compressed_data)

start = time.time()
decompressed_data = brotli.decompress(compressed_data)
end = time.time()-start

print(f"data decompressed in: {end}s. original size: {len(str(data))} decompressed size: {len(decompressed_data)}")