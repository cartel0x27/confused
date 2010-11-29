#!/usr/bin/python
from confused import DuressFile, DuressEntry
from tempfile import mkstemp
from os import system

# pam_confused - (c) 2008,2010 Thoughtcrime
# http://this.is.thoughtcrime.org/confused

# change your /etc/pam.d/common-auth Primary section to:
#auth    [default=ignore success=done]   pam_unix.so nullok_secure
#auth    [default=ignore success=done]   pam_python.so pam_confused.py


def pam_sm_authenticate(pamh, flags, argv):
      user = pamh.get_user(None)
      if user == None:
        pam.user = "nobody"
        return pamh.PAM_SUCCESS
      password = pamh.authtok
      duress = DuressFile("/etc/confused", mode="rb")

      entry = duress.retr(user, password)
      if entry == None:
          # no match
          return pamh.PAM_AUTH_ERR

      if entry.mode == 1:
          o, script = mkstemp()
          open(script, "w").write(entry.action)
          system("/bin/sh %s"%script)
      return pamh.PAM_SUCCESS


# everything else as pam_permit.py... might need more stuff here?
def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS
