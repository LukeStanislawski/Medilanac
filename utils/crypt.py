from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import hashlib
import string
import random
import json
import base64


def hash(digest):
    """
    Hash function

    digest: data to be hashed
    """
    byte_code = str(digest).encode('utf-8')
    hash_object = hashlib.sha256(byte_code)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def gen_keys():
    """
    Generate public and private RSA keys
    """
    new_key = RSA.generate(2048, e=65537)
    private_key = new_key.exportKey("PEM")
    public_key = new_key.publickey().exportKey("PEM")

    return private_key, public_key


def encrypt(public_key, body):
    """
    Encrypt a message with public key

    public_key: Public key to be used to encrypt message with
    body: body of message to be encrypted
    """
    bytes_code = str(body).encode('utf-8')
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)
    encrypted = rsa_key.encrypt(bytes_code)

    return encrypted


def decrypt(private_key, body):
    """
    Decrypt ciphertext with private key

    private_key: Private key to be used to decrypt ciphertext
    body: Ciphertext to be decrypted
    """
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(body)
    return decrypted.decode("utf-8")


def sign(private_key, body):
    """
    Sign a message with provate key

    private_key: Private key used to sign message
    body: Body of message to be signed
    """
    bytes_code = str(body).encode('utf-8')
    rsakey = RSA.importKey(private_key)
    # rsakey = PKCS1_OAEP.new(rsakey)
    signature = rsakey.sign(bytes_code, "")

    return signature[0]


def verify(public_key, body, signature):
    """
    Verify a message using a given signature

    public_key: The public key of sender
    body: Message to be verified
    signature: The signature to be used for verification
    """
    bytes_code = str(body).encode('utf-8')
    rsakey = RSA.importKey(public_key)
    return rsakey.verify(bytes_code, (signature, None))


def hash_block(block, attrs=["head", "body", "foreign_chunks"]):
    """
    Hashes a block from a blockchain

    block: block to be hashed
    attrs: Attributes of block to be included in hash
    """
    raw_block = {}

    for attr in attrs:
        if attr in block:
            raw_block[attr] = block[attr]
    return hash(json.dumps(raw_block, sort_keys=True))


def hash_chunk(chunk, attrs=["head", "data"]):
    """
    Hashes a chunk of a block

    chunk: chunk to be hashed
    attrs: Attributes of chhunk to be included in hash
    """
    raw_chunk = {}
    for attr in attrs:
        raw_chunk[attr] = chunk[attr]

    return hash(json.dumps(raw_chunk, sort_keys=True))


def hash_filedata(filedata, attrs=["data", "filename", "filesize", "patient_id", "patient_pub_key"]):
    """
    Hashes file and metadata

    filedata: dict filedata object to be hashed
    attrs: Attributes of dict to be included in hash
    """
    raw_filedata = {}
    for attr in attrs:
        if attr in filedata:
            raw_filedata[attr] = filedata[attr]

    return hash(json.dumps(raw_filedata, sort_keys=True))
    

def get_rand_str(size=64, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """
    Generates a random string

    size: Length of string
    chars: Character set to be used
    """
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


if __name__ == "__main__":
    print ("Generating keys")
    priv, pub = gen_keys()
    print("\n")

    print("Testing hash")
    if hash("Hello") == "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969":
        print("PASS")
    else:
        print("FAIL")
    print ("\n")

    text = "Luke Stanislawski"
    print("Testing RSA encryption with text: '{}'".format(text))
    cyphertext = encrypt(pub, text)
    if decrypt(priv, cyphertext) == text:
        print("PASS")
    else:
        print("FAIL")
        print(decrypt(priv, cyphertext))
    print("\n")

    print("Testing RSA Signing")
    sig = sign(priv, "Luke Stanislawski")
    if verify(pub, "Luke Stanislawski", sig):
        print ("PASS")
    else:
        print("FAIL")