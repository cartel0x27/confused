#!/usr/bin/python

# confused - (c) 2008,2010 Thoughtcrime
# http://this.is.thoughtcrime.org.nz/confused


from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os, struct

def elevate(user, key): s = SHA256.new(user); s.update(key); return s
pad = lambda s: str(s) + (16 - len(str(s)) % 16) * " "
aes = lambda s: AES.new(s.digest(), AES.MODE_CBC)

class DuressError(Exception):
    pass

class DuressEntry:
    def __init__(self, user=None, password=None, mode=None, action=None):
        self.user = user
        self.password = password
        self.mode = mode
        self.action = action
    def pack(self, a):
        fs = "BBBH" + "".join(map(lambda x: str(len(x)) + "s", [self.user, self.password, self.action]))
        s = struct.pack(fs, self.mode,
                        len(self.user), len(self.password), len(self.action),
                        self.user,
                        self.password,
                        self.action)
        return a.encrypt(pad(len(s))) + a.encrypt(pad(s))
    def unpack(self, s, length, a):
        s = a.decrypt(s)
        self.mode,b,c,d = struct.unpack("BBBH", s[:6])
        fs = "".join(map(lambda x: str(x) +"s", [b,c,d]))
        self.user, self.password, self.action = struct.unpack(fs, s[6:length])
        return self

class DuressFile:
    def __init__(self, backend, wipe=False, size=65536, mode="rb+"):
        if not os.path.exists(backend) or wipe == True:
            f = open(backend, "w")
            f.write(os.urandom(size))
            f.close()
        self.backend = open(backend, mode)
        self.size = os.path.getsize(backend)
    def seek_entry(self, s):
        self.backend.seek(int(s.hexdigest(), 16) % self.size)
    def store(self, d):
        k = elevate(d.user, d.password)
        self.seek_entry(k)
        self.backend.write(d.pack(aes(k)))
    def retr(self, u, p):
        k = elevate(u, p)
        self.seek_entry(k)
        try:
            a = aes(k)
            l = int(a.decrypt(self.backend.read(16)))
            c = self.backend.read(len(pad("a"*l)))
            return DuressEntry().unpack(c, l, a)
        except ValueError:
            return None
    def close(self):
        self.backend.close()

if __name__ == "__main__":
    from tempfile import mkstemp
    from getpass import getpass
    o, tempfile = mkstemp()
    f = DuressFile(tempfile, True)
    
    user = "cartel"
    action = os.urandom(4096)
    keys = []
    while True:
        key = getpass("k: ")
        if key == "": break
        keys.append(key)
        d = DuressEntry(user,key,1,action)
        f.store(d)

        for key in keys:
            q = f.retr(user, key)
            if q.user == user and q.password == key and q.mode == 1 and q.action == action:
                print "Test passed: %s"%key
            else:
                print "Test failed: %s"%key

    f.close()
    os.remove(tempfile)
