from netmiko import ConnectHandler
from pprint import pprint
import signal
import logging

from utils import read_nodes_file_yaml
from utils import getCredentials
from utils import getCommandsFromFile
from utils_backup import createDirectory
from utils_backup import saveBackUP

from nodelist import NodeList
from node import GCNode, verifyNTPservers
from node import verifyNTPservers

import concurrent.futures

# These capture errors relating to hitting ctrl+C (I forget the source)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

BACKUP_PATH = createDirectory()
COMMANDS = getCommandsFromFile("backup_commands.txt")
username, password = getCredentials(threading=True)

def main():
    logging.basicConfig(filename='backup_error.log', level=logging.WARNING)

    nodes_list = list()
    nodes_list = read_nodes_file_yaml("nodes_gc.yaml")

    
    
    results = NodeList()
    
    
    print(f"Nodes to backup:")
    results.print_nodes(nodes_list)

    with concurrent.futures.ThreadPoolExecutor() as exe:
        results = exe.map(backup, nodes_list)

    
    #backup_PATH = createDirectory()

    
 
    # backup_node_list = list()
    # for node in nodes_list:
    #     if not node['hostname'].startswith("#"): #Skip any node starting with a hashtag (#)
    #         node["username"] = username
    #         node["password"] = password
            
                        
            # output = gcnode.send_command(commands)
            # #print(output)            
            # print(saveBackUP(backup_PATH, node['hostname'], output))
            
            # if not verifyNTPservers(output):
            #     print(f"{node['hostname']} [Fixing...]")
            #     config_command = getCommandsFromFile("ntp_config_commands.txt")
            #     gcnode.config_command(config_command)    
                
            #     print(f"{node['hostname']} [OK]")            
            #     results.add_node_completed(gcnode.get_node())
            # else:
            #     print(f"{node['hostname']} [OK]")

    

    
    #results.print_nexus_nodees(results.get_completed_list())
    #print(f"nodees FIXED:")
    #pprint(results.get_completed_list())
    #results.print_nexus_nodees(results.get_completed_list())

def backup(node):
    node["username"] = username
    node["password"] = password 
    gcnode = GCNode(node)
    
    output = gcnode.send_command(COMMANDS, threading=True)
    #print(output)            
    print(saveBackUP(BACKUP_PATH, node['hostname'], output))


if __name__ == "__main__":
    main()


