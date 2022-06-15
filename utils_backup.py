import os

def createDirectory (parent_dir="./", directory="backups"):
    """ Creates a backup directory """
    path = os.path.join(parent_dir, directory)
    try:  
        os.makedirs(path)  
        print('Directory "% s" created\n' % path) 
    except OSError as error:  
        #print(error)  
        print('\nStoring backups in directory - "% s"\n' % path)        
    
    return path

def saveBackUP( parent_dir, node, show_run_config, filemode="w" ):
    """ Generates Backup for NODE """
        
    NODE_filename = parent_dir + "/"+ node + ".txt"
    NODE_backup_file = open(NODE_filename, filemode )
    NODE_backup_file.write(show_run_config)
    NODE_backup_file.close()
    output = 'Backup complete: "%s"' % NODE_filename    
    return output