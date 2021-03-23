from pykeepass import PyKeePass
import sys
import os.path
import urllib.request
import hashlib
import argparse

def handle_sys_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("database", help="is the database file that you want to prove", type=str)
    parser.add_argument("-p", "--password", help="is the password", type=str, required=False)
    parser.add_argument("-k", "--keyfile", help="is your key file", type=str, required=False)
    
    args = parser.parse_args()

    return args.database, args.password, args.keyfile

def check_pwned(entry):
    pw = entry.password

    result = hashlib.sha1(pw.encode())
    result = result.hexdigest()
    result_five = result[0:5]

    api_url = 'https://api.pwnedpasswords.com/range/' + result_five

    with urllib.request.urlopen(api_url) as response:
        html = (response.read()).decode('ascii').lower().split('\r\n')
        for line in html:
            current_hash=result_five+line.split(':')[0]
            if result==current_hash:
                print('Your ' + entry.title + ' account has been pwned. Password ' + entry.password + ' was found ' + line.split(':')[1] + ' times in the data set of haveibeenpwned.com')
                return True

    return False

def main():
    database, password, keyfile = handle_sys_args()
    
    if os.path.isfile(str(database)):
        if password != None or str(keyfile) != None:
            kp = PyKeePass(database, password=password, keyfile=keyfile)

            groups = kp.groups
            pwned_entries = []
            
            for group in groups:
                entries = group.entries

                for entry in entries:
                    if str(entry.password)=='None':
                        pass
                    elif check_pwned(entry):
                        pwned_entries.append(entry)
            
            print()
            print('In total ' + str(len(pwned_entries)) + ' entries have been pwned.')

if __name__=='__main__':
    main()