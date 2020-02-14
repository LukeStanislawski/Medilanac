from utils import crypt


def merkle_tree(data : [str]):
	hashes = []
	for d in data:
		hashes.append(crypt.hash(d))
	return merkle([hashes])


def merkle(tree):
	while len(tree[-1]) != 1:
		tree.append(hash_list(tree[-1]))
	tree.reverse()
	return tree
	

def hash_list(a):
	b = []
	for i in range(1, len(a), 2):
		b.append(crypt.hash(a[i-1] + a[i])[:6])
	if len(a) % 2 != 0:
		b.append(a[-1])
	return b