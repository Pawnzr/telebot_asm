import os
import errno
import subprocess

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
    
def scan_subdomain(target):
    result_path = f"Result/{target}"
    result_file = f"Result/{target}/subdomain.txt"
    create_directory(result_path)
    subdomain_cmd = f"subfinder -d {target} > {result_file}"
    subprocess.run(subdomain_cmd, shell=True)
    with open(result_file, 'r') as f:
        subdomains = f.read().strip() or target
    return subdomains
