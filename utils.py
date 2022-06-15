import yaml
from getpass import getpass
import os

def read_nodes_file_yaml(filename:str) -> list():
    """ read nodes from json file -> returns a list """
    nodes = []
    with open(filename) as f:
        nodes = yaml.safe_load(f)
    return nodes
    
def getCredentials(username=None, password="", threading:bool=False):
    """Gets Login creditials from User"""
    
    password = None
    confirmPassword = str()
    username = input("Enter username: ")

    while not password:
        password = getpass()
        if threading == True: 
            confirmPassword = getpass("Confirm password: ")
            if password == confirmPassword: 
                pass
            else:
                print("Passwords dont match")
                password = None    
        
    return username, password

def getCommandsFromFile(commands_file):
    """ description: Gets the commands from commands file"""
    n_list = []
    with open(commands_file) as f:
        n_list = f.read().splitlines()
    return n_list


def createDirectory (parent_dir="./", directory="backups"):
    """ Creates a backup directory """
    path = os.path.join(parent_dir, directory)
    try:  
        os.makedirs(path)  
        print('Directory "% s" created\n' % path) 
    except OSError as error:  
        #print(error)  
        print('Storing backups in directory - "% s"\n' % path)        
    
    return path
