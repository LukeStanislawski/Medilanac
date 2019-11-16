from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
import hashlib, string, random, json


def hash(digest):
        hash_object = hashlib.sha256(digest)
        hex_dig = hash_object.hexdigest()
        return hex_dig

def hash_block(block):
    body = json.dumps(block['block'], sort_keys=True)
    return hash(body)


def gen_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_str, public_key_str


def encrypt(public_key, body):
    key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )

    encrypted = key.encrypt(
        body,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted


def decrypt(private_key, body):
    key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )

    original_message = key.decrypt(
        body,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message


def sign(private_key, body):
    key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )

    signature = key.sign(
        body,
        padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),  
        salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


def get_rand_str(size=64, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))



def verify(public_key, body, signature):
    key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )

    try:
        key.verify(
            signature,
            body,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    


if __name__ == "__main__":
    print "Testing..."
    priv, pub = gen_keys()
    
    print decrypt(priv, encrypt(pub, "Encryption/decryption work!"))
    
    if verify(pub, "hello", sign(priv, "hello")):
        print "Signing works!"
    else:
        print "Signing doesnt work :("

    print hash("Hello")