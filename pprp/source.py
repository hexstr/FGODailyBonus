import logging

import pprp.config

_logger = logging.getLogger(__name__)

def file_source_gen(filepath, block_size=pprp.config.DEFAULT_BLOCK_SIZE_B):
    with open(filepath, 'rb') as f:
        i = 0
        while 1:
            offset = 0
            block = f.read(block_size)
            if not block:
                break

            _logger.debug("Yielding [file] source block: (%d)-(%d)", i, offset)
            yield block
            i += 1
            offset += len(block)

def data_source_gen(data, block_size=pprp.config.DEFAULT_BLOCK_SIZE_B):
    i = 0
    for offset in range(0, len(data), block_size):
        block = data[offset:offset + block_size]

        _logger.debug("Yielding [data] source block: (%d)-(%d)", i, offset)
        yield block
        i += 1
