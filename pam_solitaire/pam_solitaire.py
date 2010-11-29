#
# pam_solitaire.py -- challenge/response using a solitaire deck as secret.
#
# as a pam handler:
# auth       required     pam_python.so pam_solitaire.py

# to generate deck:
# python /lib/security/pam_solitaire.py /etc/pam_solitaire/username.deck

DEFAULT_USER= "nobody"

import string, sys, struct, os, random

def toNumber(c):
    """
    Convert letter to number: Aa->1, Bb->2, ..., Zz->26.
    Non-letters are treated as X's.
    """
    if c in string.letters:
        return ord(string.upper(c)) - 64
    return 24  # 'X'

def toChar(n):
    """
    Convert number to letter: 1->A,  2->B, ..., 26->Z,
    27->A, 28->B, ... ad infitum
    """
    return chr((n-1)%26+65)


class Solitaire:
    """ Solitaire Encryption Algorithm
    http://www.counterpane.com/solitaire.html
    """

    def __init__(self, deck=False, key=False):
        if deck:
            self.deck = deck
        elif key:
            self._setKey(key)
        else:
            self.deck= range(1,55)

    def _setKey(self, passphrase):
        """
        Order deck according to passphrase.
        """
        self.deck = range(1,55)
        # card numbering:
        #  1, 2,...,13 are A,2,...,K of clubs
        # 14,15,...,26 are A,2,...,K of diamonds
        # 27,28,...,39 are A,2,...,K of hearts
        # 40,41,...,52 are A,2,...,K of spades
        # 53 & 54 are the A & B jokers
        for c in passphrase:
            self._round()
            self._countCut(toNumber(c))

    def _down1(self, card):
        """
        Move designated card down 1 position, treating
        deck as circular.
        """
        d = self.deck
        n = d.index(card)
        if n < 53: # not last card - swap with successor
            d[n], d[n+1] = d[n+1], d[n]
        else: # last card - move below first card
            d[1:] = d[-1:] + d[1:-1]
        
    def _tripleCut(self):
        """
        Swap cards above first joker with cards below
        second joker.
        """
        d = self.deck
        a, b = d.index(53), d.index(54)
        if a > b:
            a, b = b, a
        d[:] = d[b+1:] + d[a:b+1] + d[:a]
        
    def _countCut(self, n):
        """
        Cut after the n-th card, leaving the bottom
        card in place.
        """
        d = self.deck
        n = min(n, 53) # either joker is 53
        d[:-1] = d[n:-1] + d[:n]

    def _round(self):
        """
        Perform one round of keystream generation.
        """
        self._down1(53) # move A joker down 1
        self._down1(54) # move B joker down 2
        self._down1(54)
        self._tripleCut()
        self._countCut(self.deck[-1])

    def _output(self):
        """
        Return next output card.
        """
        d = self.deck
        while 1:
            self._round()
            topCard = min(d[0], 53)  # either joker is 53
            if d[topCard] < 53:  # don't return a joker
                return d[topCard]

    def encrypt(self, txt, key=False):
        """
        Return 'txt' encrypted using 'key'.
        """
        if key:
            self._setKey(key)
        cipher = [None] * len(txt)
        for n in range(len(txt)):
            cipher[n] = toChar(toNumber(txt[n]) + self._output())
        return string.join(cipher, '')

    def decrypt(self, cipher, key=False):
        """
        Return 'cipher' decrypted using 'key'.
        """
        if key:
            self._setKey(key)
        # remove white space between code blocks
        cipher = string.join(string.split(cipher), '')
        txt = [None] * len(cipher)
        for n in range(len(cipher)):
            txt[n] = toChar(toNumber(cipher[n]) - self._output())
        return string.join(txt, '')

# we could encrypt the decks using the password offered in the pam handler... maybe later
def saveDeck(deck, filename):
    f = open(filename, "wb")
    f.write(struct.pack("B"*len(deck), *deck))
    f.close()

def loadDeck(filename):
    f = open(filename)
    buf = f.read()
    f.close()
    return Solitaire(deck=list(struct.unpack("B"*len(buf),buf)))

def genChallenge(length):
    def chal():
        for i in range(0,length):
            yield string.letters[26:][random.randint(0,25)]
    return "".join(list(chal()))

def pam_sm_authenticate(pamh, flags, argv):
    """The actual pam handler function."""
    try:
      user = pamh.get_user(None)
      try:
        sol = loadDeck("/etc/pam_solitaire/%s.deck"%user)
      except IOError:
        # deck doesnt exist, allow axx
        return pamh.PAM_SUCCESS

      try:
        challengelength = int(argv[1])
      except IndexError:
        challengelength=10
      challenge = genChallenge(challengelength)

      pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Challenge: %s"%challenge))
      x = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_ON , "Response: "))

      response = sol.encrypt(challenge)

      saveDeck(sol.deck, "/etc/pam_solitaire/%s.deck"%user)
      if x.resp == response:
        pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Response authenticated."))
        return pamh.PAM_SUCCESS
      else:
        pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Invalid response."))
        return pamh.PAM_AUTH_ERR
    except pamh.exception, e:
      pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Error: %s"%e.pam_result))
      return e.pam_result
    if user == None:
      pam.user = DEFAULT_USER
    return pamh.PAM_AUTH_ERR

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

if __name__ == "__main__":
    """Quick hack to generate decks from command line"""
    challenge = genChallenge(10)
    deck = sys.argv[1]
    sol = Solitaire(key=str(raw_input("Order Passphrase: ")))
    saveDeck(sol.deck, deck)
    #print "deck: "+" ".join(map(str, sol.deck))
    print "challenge is: %s"%challenge
    x = raw_input("response ---> ")
    response = sol.encrypt(challenge)
    if response == x:
        print "Success!"
    else:
        print "Fail"





