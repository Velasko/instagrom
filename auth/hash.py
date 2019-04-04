import hashlib

def passwd_hash(passwd):
	sha_signature = \
		hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature