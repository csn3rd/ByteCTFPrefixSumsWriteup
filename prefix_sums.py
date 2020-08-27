from math import gcd
import hashlib

def get_flag(n, p):
	a = n-2*p
	b = n

	factor = gcd(a, b)

	a = a//factor
	b = b//factor

	print("simplified fraction:\t\t" + str(a) + "/" + str(b))

	dec = int(str(a) + str(b))
	flag = "flag{" + hex(dec) + "}"

	print("flag:\t\t\t\t" + flag)

	hash = hashlib.md5(flag.encode()).hexdigest()

	if hash == "6046f30cf9e942ed47c88621a69ed0b2":
		print("flag is correct. hash:\t\t" + hash)
	else:
		print("flag is incorrect. hash:\t" + hash)


n = 3141592653589793238
p = 101124131231734
get_flag(n, p)