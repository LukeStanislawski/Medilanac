from utils import crypt


def merkle_tree(data : [str]):
	"""
	Generates a merkle tree for a list of strings.
	Merkle tree leaves are hashes of the combination of two item hashes.
	E.g. if len(data) == 6, len(mtree[-1]) = 3

	data: List of items to generate merkle tree for
	"""
	if data is None or len(data) < 1:
		return []
	elif all([type(x)==str for x in data]):
		return merkle([data])
	else:
		return merkle([ [crypt.hash(x) for x in data] ])


def merkle_tree_files(data : [str]):
	"""
	Generates a merkle tree for a list of files.
	Merkle tree leaves are hashes of each file.
	E.g. if len(data) == 6, len(mtree[-1]) = 6

	data: List of items to generate merkle tree for
	"""
	if data is None or len(data) < 1:
		return []
	else:
		hashes = []
		for d in data:
			hashes.append(d["hash"])
		return merkle([hashes])


def merkle(tree):
	"""
	Recursive function that generates the next level up 
	of a tree, with each call

	tree: Incomplete merkle tree
	"""
	if len(tree[-1]) == 1:
		tree.reverse()
		return tree
	else:
		tree.append(hash_list(tree[-1]))
		return merkle(tree)


	# while len(tree[-1]) != 1:
	# 	tree.append(hash_list(tree[-1]))
	# tree.reverse()
	# return tree
	

def hash_list(a):
	"""
	Returns a list of the hashes of pairs of list items
	E.g. hash_list([a,b,c,d,e,f]) = [hash(a+b), hash(c+d), hash(e+f)]

	a: List of items to hash zipped
	"""
	b = []
	for i in range(1, len(a), 2):
		b.append(crypt.hash(a[i-1] + a[i]))
	if len(a) % 2 != 0:
		b.append(a[-1])
	return b