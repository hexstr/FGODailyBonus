import os

# Required we're acting as AES.
DEFAULT_BLOCK_SIZE_B = int(os.environ.get('PPRP_BLOCK_SIZE_B', str(128 // 8)))
