from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
import logging

logger = logging.getLogger(__name__)

class GCNode:
    def __init__(self, node) -> None:
        # self.hostname = node["hostname"]
        # self.ip = node["ip"]    
        self.node = node
        self.prompt = "#"
        self.tacdownFixed = False

    def settacDownFix(self, value):
        self.tacdownFixed = value

    def get_node(self):
        return self.node

    def set_node(self, node):
        self.node = node

    def send_command(self, commands:str, threading:bool=False) -> str:
        """ execute a read onlycommand"""
        output = str()
        try:
            node = self.get_netmiko_ready_node()
            if not threading: print(f"\n--- Connecting to {node['ip']} ... --- ")
            net_connect = ConnectHandler(**node)
            self.prompt = net_connect.find_prompt()
            # print(self.prompt)
            # print(self.prompt+" "+command)
            # output = net_connect.send_command(command)

            for command in commands:
                output = output + "\n" + str("-" * 23) + command + str("-" * 23) + "\n"
                if not threading: print(self.prompt + command)
                output += self.prompt + command + "\n"
                output += net_connect.send_command(command)
            
        except NetMikoTimeoutException:
            print(f"\n!! {self.node['hostname']} ERROR: Connection to {self.node['ip']} timed-out.\n")
        except NetMikoAuthenticationException:
            e_message = f"\n!! {self.node['hostname']} ERROR: Authenticaftion failed for {self.node['ip']}. Stopping script.\n"
            logging.exception(e_message)
            print(e_message)
            exit(1)
        net_connect.disconnect()

        return output
    

    def config_command(self, command) -> None:
        
        try:
            node = self.get_netmiko_ready_node()
            
           
            net_connect = ConnectHandler(**node)

             #set delay_factor to prevent "ValueError:Unable to find prompt" because of slow responding node
            self.prompt = net_connect.find_prompt(delay_factor=2)

            print_command = '\n'.join(command)           
            print(f"{self.prompt} {print_command}")
            
            net_connect.send_config_set(command)

            saves_changes_command = str("copy run start")
            print(f"{self.prompt} {saves_changes_command}")
            net_connect.send_command(saves_changes_command)

            
        except NetMikoTimeoutException:
            print(f"\n!! {self.node['hostname']} ERROR: Connection to {self.node['ip']} timed-out.\n")
        except NetMikoAuthenticationException:
            print(f"\n!! {self.node['hostname']} ERROR: Authenticaftion failed for {self.node['ip']}. Stopping script.\n")
            exit(1)
        except ValueError as e:
            print(e)
            logger.exception("%s %s", self.node['hostname'], e)
           

        net_connect.disconnect()

        

    def get_netmiko_ready_node(self) -> list:
        s = list()
        s = self.node.copy()
        s.pop("hostname")

        return s
    

def verifyPassword(output) -> bool:
    return len(output.split()[4]) > 5 
        
def verifyNTPservers(output) -> bool:
    return bool(output.strip()) 



