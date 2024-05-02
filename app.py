import os
import errno

def create_directory(target_dir):
    try:
        os.makedirs(target_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            pass
def read_file(file_path):
    if not os.path.exists(file_path):
        return "Hehe :)))"
    with open(file_path, 'r') as f:
        return(f.read())