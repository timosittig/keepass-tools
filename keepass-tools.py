from pykeepass import PyKeePass
import sys
import os.path
import argparse

def handle_sys_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("database", help="is the database file that you want to prove", type=str)
    parser.add_argument("-p", "--password", help="is the password", type=str, required=False)
    parser.add_argument("-k", "--keyfile", help="is your key file", type=str, required=False)
    
    parser.add_argument("-u", "--update", help="", required=False)
    parser.add_argument("-v", "--version", help="", required=False)
    
    args = parser.parse_args()

    #handle_update(args.update)
    #handle_version(args.version)

    return args.database, args.password, args.keyfile

def handle_update():
    print('Update function running')

def main():
    database, password, keyfile = handle_sys_args()

if __name__=='__main__':
    main()