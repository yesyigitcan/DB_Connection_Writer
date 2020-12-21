from cryptography.fernet import Fernet
import pickle
import os
import json

if __name__ == '__main__':
    # Configuration file read
    with open('Config.json', 'r') as inputfile:
        conf = json.load(inputfile)
        key_name = conf["KEY_NAME"]
        if conf["KEY_PATH"] == "CURRENT":
            key_path = os.getcwd()
        else:
            key_path = conf["KEY_PATH"]
    filename = os.path.join(key_path, key_name)

    # Encryption key generation
    key = Fernet.generate_key()
    if not os.path.isfile(key_name):
        with open(filename, 'wb') as outputfile:
            outputfile.write(key)
        print("Key generated in path ", key_path)
    else:
        raise Exception("A key is already exist in " +  key_path +  " and cannot overwrite it")