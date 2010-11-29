#!/bin/bash

if [ $(whoami) != "root"]
    echo "Please run as root."
    exit

set -e

echo "Building pam-python..."
tar -zxvf ./pam-python-1.0.0.tar.gz
cd pam-python-1.0.0/src
make && make install
cd ../..

echo "Installing confused.py..."
python ./setup.py install

echo "Copying other files..."
cp pam_confused.py /lib/security
cp mkconfused.py /usr/local/sbin/
chmod 700 /usr/local/sbin/mkconfused.py /lib/security/pam_confused.py

echo "Installation finished."

echo "To activate confused, change your /etc/pam.d/common-auth primary block to:

auth    [default=ignore success=done]   pam_unix.so nullok_secure
auth    [default=ignore success=done]   pam_python.so pam_confused.py"




