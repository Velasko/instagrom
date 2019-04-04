import hashlib

def passwd_hash(passwd):
	sha_signature = \
		hashlib.sha256(passwd.encode()).hexdigest()
	return sha_signature