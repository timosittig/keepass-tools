"""
KeePass brute forcing script

Based on another GitHub project by Raphael Vallat: https://gist.github.com/raphaelvallat/646bd1675f2dadff09c50ebc85f298b8

List of most probable passwords and english names can be found, respectively, at:
- https://github.com/danielmiessler/SecLists/blob/master/Passwords/probable-v2-top12000.txt
- https://github.com/dominictarr/random-name/blob/master/middle-names.txt

Author: Timo Sittig
Date: 17th March 2021
Python 3.8.2
"""

from pykeepass import PyKeePass
import sys

import string
from itertools import product
from time import time
from numpy import loadtxt

from datetime import datetime

def check_credentials(file, passwords):
    for current in passwords:
        kp = None
        current = ''.join(current)

        try:
            kp = PyKeePass(file, password=current)
        except:
            pass

        if isinstance(kp, PyKeePass):
            print('\nPassword for ', file, ' is  ', current)
            return current
    return False

def bruteforce(file, max_nchar=8):
    print('1) Comparing with most common passwords / first names')
    common_pass = loadtxt('../res/probable-v2-top12000.txt', dtype=str)
    #common_names = loadtxt('middle-names.txt', dtype=str)
    
    cp = [c for c in common_pass if check_credentials(file, c)]
    if len(cp) == 1:
        print('\nPassword:', cp)
        return cp
#    cn = [c for c in common_names if check_credentials(file, c)]
#    if len(cn) == 1:
#        print('\nPassword:', cn)
#        return cn
#    cnl = [c.lower() for c in common_names if check_credentials(file, c.lower())]
#    if len(cnl) == 1:
#        print('\nPassword:', cnl)
#        return cnl

    print('2) Digits cartesian product')
    for l in range(1, max_nchar + 1):
        current_passwords = product(string.digits, repeat=l)
        print("\t..%d digit" % l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

    print('3) Digits + ASCII lowercase')
    for l in range(1, max_nchar + 1):
        print("\t..%d char" % l)
        current_passwords = product(string.digits + string.ascii_lowercase,
                            repeat=l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

    print('4) Digits + ASCII lower / upper + punctuation')
    all_char = string.digits + string.ascii_letters + string.punctuation

    for l in range(1, max_nchar + 1):
        print("\t..%d char" % l)
        current_passwords = product(all_char, repeat=l)
        p = check_credentials(file, current_passwords)
        if p is not False:
            return p

def main():
    max_length = 8

    if 1 < len(sys.argv):
        file = str(sys.argv[1])
        
        if 2 < len(sys.argv):
            max_length = int(sys.argv[2])
        
        start = time()
        print('Starting bruteforce on ', file, ' at ', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        bruteforce(file, max_length)
        
        end = time()
        print('Total time: %.2f seconds' % (end - start))

if __name__=='__main__':
    main()