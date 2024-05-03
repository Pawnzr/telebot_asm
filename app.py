import os
import errno
import subprocess
import socket
import xml.etree.ElementTree as ET

def check_file_exists(filepath):
    if os.path.exists(filepath):
        return True
    else:
        return False

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

def scan_port(target):
    nmap_export_path = f"Result/{target}"
    create_directory(nmap_export_path)
    nmap_export_file = f'Result/{target}/nmap.xml'
    if check_file_exists(nmap_export_file):
        data = export_data(nmap_export_file)
        return data
    else:
        try:
            nmap_cmd = f"nmap -sV -Pn -T4 {target} -oX {nmap_export_file}"
            subprocess.run(nmap_cmd, shell=True)
            data = export_data(nmap_export_file)
            return data
        except:
            return ""
    
def resolve_domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return ""

def resolve_ip_to_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return ""
    
def export_data(data_path):
    port_result = []
    with open(f"{data_path}",'r') as f:
        data = f.read()
    root = ET.fromstring(data)
    port_id = ''
    protocol = ''
    state = ''
    service_name = ''
    service_product = ''
    service_version = ''
    hostname = ''
    service_servicefp = ''
    service_service_extra = ''
    try:
        for port in root.findall('.//port'):
            port_id = port.get('portid') or ''
            protocol = port.get('protocol') or ''
            state = port.find('.//state').get('state') or ''
            service_name = port.find('.//service').get('name') or ''
            service_product = port.find('.//service').get('product') or ''
            service_version = port.find('.//service').get('version') or ''
            hostname = port.find('.//service').get('hostname') or ''
            service_servicefp = port.find('.//service').get('servicefp') or ''
            service_service_extra = port.find('.//service').get('extrainfo') or ''
            version = service_product + ' ' + service_version
            port_data = {
                "port" : port_id,
                "protocol" : protocol,
                "state" : state,
                "service": service_name,
                "version" : version,
                "extra_info" :  {"hostname": hostname,"servicefp":service_servicefp,"extrainfo":service_service_extra}
            }
            
            port_result.append(port_data)
        return port_result
    except:
        return ""