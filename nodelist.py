class NodeList:
    
    def __init__(self):
        self.pending_list = list()
        self.completed_list = list()
        
    def add_node_completed(self, node):
        self.completed_list.append(node)

    def add_node_pending(self, node):
        self.pending_list.append(node)

    def get_completed_list(self):
        return self.completed_list
        
    def get_pending_list(self):
        return self.pending_list

    def print_nodes(self, nexus_nodes_list:list()) -> None:
        """ Prints Nexus nodees to screen"""

        headers = ["Hostname", "IP Address", "Device_Type",""]
        print(f"{headers[3]:<3} {headers[0]:30} {headers[1]:20} {headers[2]}")
        for count, node in enumerate(nexus_nodes_list, start=1):
            print(f"{count:<4}{node['hostname']:30} {node['ip']:20} {node['device_type']}")