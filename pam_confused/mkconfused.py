#!/usr/bin/python
from confused import DuressFile, DuressEntry
from getpass import getpass
import sys, os

# mkconfused - (c) 2008,2010 Thoughtcrime
# http://this.is.thoughtcrime.org.nz/confused
# syntax: mkconfused.py user mode script

def mkpasswd(duress, user, mode, script):
    p1 = getpass("Enter duress password:")
    p2 = getpass("Re-enter duress password:")

    if p1 != p2:
        print "Passwords did not match."
        raise SystemExit
    else:
        duress.store(DuressEntry(user, p1, mode, script))
        print "Updated successfully."

def test(duress, user):
    while True:
        p = getpass("Enter a password to test, or blank to quit:")
        if p == "": raise SystemExit
        t = duress.retr(user, p)
        if t != None:
            print "Test successful"
        else:
            print "An error occurred unpacking this struct."

if __name__ == "__main__":
    #if os.getuid != 0:
    #    print "Please run as root."
    #    raise SystemExit

    duress = DuressFile("/etc/confused")
    user = sys.argv[1]
    mode = sys.argv[2]

    if mode == "t":
        test(duress, user)
    else:
        script = open(sys.argv[3]).read()
        mkpasswd(duress, user, int(mode), script)
