import io

import pprp
import pprp.config

def decrypt_sink(dg, block_size=pprp.config.DEFAULT_BLOCK_SIZE_B):
    s = io.BytesIO()
    last_block = None
    for block in dg:
        block_to_send = last_block
        last_block = block

        if block_to_send is not None:
           s.write(block_to_send)

    trimmed_last_block = pprp.trim_pkcs7_padding(last_block)
    s.write(trimmed_last_block)
    return s.getvalue()

def encrypt_sink(eg):
    s = io.BytesIO()
    for block in eg:
        s.write(block)

    return s.getvalue()

def decrypt_to_file_sink(f, dg, block_size=pprp.config.DEFAULT_BLOCK_SIZE_B):
    last_block = None
    for block in dg:
        (block_to_send, last_block) = (last_block, block)

        if block_to_send is not None:
           f.write(block_to_send)

    trimmed_last_block = pprp.trim_pkcs7_padding(last_block)
    f.write(trimmed_last_block)
    f.flush()

def encrypt_to_file_sink(f, eg):
    for block in eg:
        f.write(block)

    f.flush()
