from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
import advancedEncrypt
from design import design 

def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def addPassword( mp, ds, sitename, url, email, username):
    password = getpass("Password: ")
    masterKey = computeMasterKey(mp, ds)
    encrypted = advancedEncrypt.encrypt(key=masterKey, source=password, keyType="bytes")

    db = design()
    cursor = db.cursor()
    query = "INSERT INTO pm.entries (sitename, url, email, username, password) values (?, ?, ?, ?, ?)"
    val = (sitename,url,email,username,encrypted)
    cursor.execute(query, val)
    db.commit()
