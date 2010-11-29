

 pam_confused -- Confusion for Linux.
-------------------------------

Confused is a duress authentication layer that can be used to execute code if and only if a specific password is entered at a login prompt.

All duress credentials and scripts are stored in a special encrypted key:value store at /etc/confused.

Installation is a simple:
# install.sh

The install script lists the changes that need to be made to /etc/pam.d/common-auth for confused to work.

To create or add an entry to /etc/confused, type:

# mkconfused.py <user> <mode> <duress script file>

<user>: self explanatory
<mode>: the mode the duress script should be executed under. Currently only mode 1 is supported: write the file to tmp and execute it with /bin/sh.
<duress script file> Path to the script that should be triggered if the duress password is entered.

You will then be prompted for a username and password.

To verify that this password will work correctly, type:

# mkconfused.py <user> t

This puts you in test mode,  where you will be prompted to enter one or more passwords to verify they decrypt and unpack correctly.


History
------

Feb 2008: First bodged implementation of Confused for mac is written and stashed in an encrypted filesystem.

??? 2008: Apple fixes the bug in screensaverengine that allowed confused to work. Original code is thought lost.

Nov 2008: "You've Got Nothing" keynote at Kiwicon demonstrates Confused for the first time. This is a hacked up video only presentation.

March 2009: A prototype for a linux version of Confused using code from amnesia is begun and abandoned.

August 2009: pam_solitaire is released. Renewed interest in amnesia leads to reactivation of the confused project. metlstorm releases metloduress-1.0.

21 August 2009: After a full ground up rewrite, pam_confused is released in 0.2 state.


Greetz
-----

Thanks to metlstorm for motivating me to get this working and released.
Greetz to #kiwicon - see you in november!
