from Cryptodome import Cipher
from Cryptodome import PublicKey
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA

message = b'To be encrypted'
h = SHA.new(message)

key = RSA.importKey(open('app/rsa_keys/key.pem').read())
cipher = PKCS1_v1_5.new(key)
ciphertext = cipher.encrypt(message+h.digest())