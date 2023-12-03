import hashlib

input = "abcdef"
input = "pqrstuv"
input = "yzbqklnj"

suffix = 1
secret_key = input + str(suffix)
while not hashlib.md5(secret_key.encode()).hexdigest().startswith("000000"):
	secret_key = input + str(suffix)
	suffix += 1

suffix -= 1

print('input: {}\nsuffix: {}\nmd5: {}\n'.format(
	input,
	suffix,
	hashlib.md5(secret_key.encode()).hexdigest()
))
