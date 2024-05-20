from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

with open('private_key.pem', 'rb') as f:
    loaded_private_key = serialization.load_pem_private_key(
        f.read(), password=None, backend=default_backend())

def sign(uuid):
    signature = loaded_private_key.sign(
        bytes(uuid, 'utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return base64.b64encode(signature).decode('utf-8')
