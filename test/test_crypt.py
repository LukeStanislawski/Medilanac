import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import pytest
from utils import crypt


def test_hash():
	o = "64ec88ca00b268e5ba1a35678a1b5316d212f4f366b2477232534a8aeca37f3c"
	assert crypt.hash("Hello world") == o,"test failed"


def test_hash_neq():
	assert crypt.hash("Hello world") != crypt.hash("Hello world "),"test failed"


def test_encrypt():
	priv, pub = crypt.gen_keys()
	assert crypt.decrypt(priv, crypt.encrypt(pub, "Hello world")) == "Hello world","test failed"


def test_false_encrypt():
	priv, pub = crypt.gen_keys()
	assert crypt.decrypt(priv, crypt.encrypt(pub, "Hello world")) != "Hello world ","test failed"


def test_ciphertext_diffkey():
	priv_a, pub_a = crypt.gen_keys()
	priv_b, pub_b = crypt.gen_keys()

	body = "Hello world"

	ct_a = crypt.encrypt(pub_a, body)
	ct_b = crypt.encrypt(pub_b, body)
	assert ct_a != ct_b,"test failed"


def test_ciphertext_diffmsg():
	priv, pub = crypt.gen_keys()

	body_a = "Hello world"
	body_b = "Hello_world"

	ct_a = crypt.encrypt(pub, body_a)
	ct_b = crypt.encrypt(pub, body_b)
	assert ct_a != ct_b,"test failed"


def test_sign():
	body = "hello world"
	priv, pub = crypt.gen_keys()
	sig = crypt.sign(priv, body)
	assert crypt.verify(pub, body, sig) == True,"test failed"


def test_false_sign():
	body = "hello world"
	priv, pub = crypt.gen_keys()
	sig = crypt.sign(priv, body)
	assert crypt.verify(pub, body+" ", sig) == False,"test failed"
