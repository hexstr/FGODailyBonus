__version__ = '0.2.6'

import sys

import pprp.adapters

from pprp.adapters import \
    rjindael_encrypt_gen, \
    rjindael_decrypt_gen

if sys.version_info[0] >= 3:
    from pprp.pbkdf2_3 import \
        pbkdf2

    import pprp.crypto_3

    pprp.adapters.rijndael_cls = pprp.crypto_3.rijndael
else:
    from pprp.pbkdf2_2 import \
        pbkdf2

    import pprp.crypto_2

    pprp.adapters.rijndael_cls = pprp.crypto_2.rijndael

from pprp.utility import \
    trim_pkcs7_padding

from pprp.source import \
    file_source_gen, \
    data_source_gen

from pprp.sink import \
    decrypt_sink, \
    encrypt_sink, \
    decrypt_to_file_sink, \
    encrypt_to_file_sink
