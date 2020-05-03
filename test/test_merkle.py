import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import pytest
from utils.merkle import merkle_tree


def test_even():
	"""
	Test string list of even length
	"""
	i = ["a", "b", "c", "d"]
	o = [['12a40550c10c6339bf6f271445270e49b844d6c9e8abc36b9b642be532befe94'], ['fb8e20fc2e4c3f248c60c39bd652f3c1347298bb977b8b4d5903b85055620603', '21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4'], ['a', 'b', 'c', 'd']]
	assert merkle_tree(i) == o,"test failed"


def test_odd():
	"""
	Test string list of odd length
	"""
	i = ["a", "b", "c", "d", "e"]
	o = [['8c1019a40ed98f7351a92ba5b890e25ad3469982d9da6677293fe2c08d61d9bb'], ['12a40550c10c6339bf6f271445270e49b844d6c9e8abc36b9b642be532befe94', 'e'], ['fb8e20fc2e4c3f248c60c39bd652f3c1347298bb977b8b4d5903b85055620603', '21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4', 'e'], ['a', 'b', 'c', 'd', 'e']]
	assert merkle_tree(i) == o,"test failed"


def test_even_int():
	"""
	Test int list of even length
	"""
	i = [0, 1, 2, 3]
	o = [['862532e6a3c9aafc2016810598ed0cc3025af5640db73224f586b6f1138385f4'], ['fa13bb36c022a6943f37c638126a2c88fc8d008eb5a9fe8fcde17026807feae4', '70311d9d203b2d7e4ff70d7fce219f82a4fcf73a110dc80187dfefb7c6e4bb87'], ['5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce']]
	assert merkle_tree(i) == o,"test failed"


def test_odd_int():
	"""
	Test int list of odd length
	"""
	i = [0, 1, 2, 3, 4]
	o = [['a45a2925b7c95556029e0b7e0636a74741354feef1d9078a01d5d4c4c4584f6d'], ['862532e6a3c9aafc2016810598ed0cc3025af5640db73224f586b6f1138385f4', '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'], ['fa13bb36c022a6943f37c638126a2c88fc8d008eb5a9fe8fcde17026807feae4', '70311d9d203b2d7e4ff70d7fce219f82a4fcf73a110dc80187dfefb7c6e4bb87', '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'], ['5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce', '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a']]
	assert merkle_tree(i) == o,"test failed"


def test_even_bytes():
	"""
	Test bytes list of even length
	"""
	i = [b"a", b"b", b"c", b"d"]
	o = [['ec76c0093ed3c7e1f835fe39f5edc92d89a44c5a12229062101c8a7db3786264'], ['662e24ce494ab860d18296e2064c6332c34aae7f7a26629f114a0c21ccb5cf3d', 'ecc4f39141a3661badd6e9e0d2a6f675c47be2075e1cc76b0654aa8a047f2b7d'], ['3ccb732a4e5439e4c70585e28604c48313346e773550013bccaa17162f4f4430', 'ddbd7ef28aee8d32c5d66f4644b0ce26d3f8e0a9deae4a4de8ae7f803a0c7291', '61823508b684b8bd7f7aa74ac4d8647e1ed8e3fb4213ae3f2692b5710bde1764', 'da589a3ceeab4f08dd90556f1ce5f5e2aa2a84bb0087f1aa7780d2e6036de872']]
	assert merkle_tree(i) == o,"test failed"


def test_odd_bytes():
	"""
	Test bytes list of odd length
	"""
	i = [b"a", b"b", b"c", b"d", b"e"]
	o = [['dc6018b867fd9221c3d65fac09414f19e499105bcae36666e5987fcee717bc0e'], ['ec76c0093ed3c7e1f835fe39f5edc92d89a44c5a12229062101c8a7db3786264', '17eb90aab6b1f4069db2d6c7a0f02963843a60faf0eaa3ce3bd286c2373cf4b7'], ['662e24ce494ab860d18296e2064c6332c34aae7f7a26629f114a0c21ccb5cf3d', 'ecc4f39141a3661badd6e9e0d2a6f675c47be2075e1cc76b0654aa8a047f2b7d', '17eb90aab6b1f4069db2d6c7a0f02963843a60faf0eaa3ce3bd286c2373cf4b7'], ['3ccb732a4e5439e4c70585e28604c48313346e773550013bccaa17162f4f4430', 'ddbd7ef28aee8d32c5d66f4644b0ce26d3f8e0a9deae4a4de8ae7f803a0c7291', '61823508b684b8bd7f7aa74ac4d8647e1ed8e3fb4213ae3f2692b5710bde1764', 'da589a3ceeab4f08dd90556f1ce5f5e2aa2a84bb0087f1aa7780d2e6036de872', '17eb90aab6b1f4069db2d6c7a0f02963843a60faf0eaa3ce3bd286c2373cf4b7']]
	assert merkle_tree(i) == o,"test failed"


def test_empty():
	"""
	Test empty list
	"""
	i = []
	o = []
	assert merkle_tree(i) == o,"test failed"
