import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import pytest
from utils import crypt


def test_hash():
	o = "64ec88ca00b268e5ba1a35678a1b5316d212f4f366b2477232534a8aeca37f3c"
	assert crypt.hash("Hello world") == o,"test failed"


def test_encrypt():
	priv, pub = crypt.gen_keys()
	assert crypt.decrypt(priv, crypt.encrypt(pub, "Hello world")) == "Hello world","test failed"


def test_sign():
	body = "hello world"
	priv, pub = crypt.gen_keys()
	sig = crypt.sign(priv, body)
	assert crypt.verify(pub, body, sig) == True,"test failed"
	assert crypt.verify(pub, body+"x", sig) == False,"test failed"
