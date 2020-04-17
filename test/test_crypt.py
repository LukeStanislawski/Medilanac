import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import pytest
from utils import crypt


def test_hash():
	"""
	Test ensures that the hash of constant string does not change
	"""
	o = "64ec88ca00b268e5ba1a35678a1b5316d212f4f366b2477232534a8aeca37f3c"
	assert crypt.hash("Hello world") == o,"test failed"


def test_hash_neq():
	"""
	Test that two different strings do not have the same hash
	"""
	assert crypt.hash("Hello world") != crypt.hash("Hello world "),"test failed"


def test_encrypt():
	"""
	Test that message is equal to message after encryption and decryption
	"""
	priv, pub = crypt.gen_keys()
	assert crypt.decrypt(priv, crypt.encrypt(pub, "Hello world")) == "Hello world","test failed"


def test_false_encrypt():
	"""
	Checks that encryption round trip does not return diffrent value
	"""
	priv, pub = crypt.gen_keys()
	assert crypt.decrypt(priv, crypt.encrypt(pub, "Hello world")) != "Hello world ","test failed"


def test_ciphertext_diffkey():
	"""
	Test that the same message produced different cipher text when encrypted with two different keys
	"""
	priv_a, pub_a = crypt.gen_keys()
	priv_b, pub_b = crypt.gen_keys()

	body = "Hello world"

	ct_a = crypt.encrypt(pub_a, body)
	ct_b = crypt.encrypt(pub_b, body)
	assert ct_a != ct_b,"test failed"


def test_ciphertext_diffmsg():
	"""
	Test that two different messages do not have the same ciphertext when encrypted with the same key
	"""
	priv, pub = crypt.gen_keys()

	body_a = "Hello world"
	body_b = "Hello_world"

	ct_a = crypt.encrypt(pub, body_a)
	ct_b = crypt.encrypt(pub, body_b)
	assert ct_a != ct_b,"test failed"


def test_sign():
	"""
	Test that a valid signature can be verified
	"""
	body = "hello world"
	priv, pub = crypt.gen_keys()
	sig = crypt.sign(priv, body)
	assert crypt.verify(pub, body, sig) == True,"test failed"


def test_false_sign():
	"""
	Test that an invalid signature is not verified
	"""
	body = "hello world"
	priv, pub = crypt.gen_keys()
	sig = crypt.sign(priv, body)
	assert crypt.verify(pub, body+" ", sig) == False,"test failed"
