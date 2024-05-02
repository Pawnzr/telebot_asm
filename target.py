from app import *
import subprocess

class Target:
    def __init__(self, url):
        self.url = url
        self.subdomain = None
        self.httpx = None
        self.port = None
    
    def scan_subdomains(self):
        result_path = f"./Result/{self.url}"
        result_file = f"{result_path}/subdomain.txt"
        
        if not os.path.exists(result_path):
            create_directory(result_path)
        
        subdomain_cmd = f"subfinder -d {self.url} > {result_file}"
        subprocess.run(subdomain_cmd, shell=True)
        
        with open(result_file, 'r') as f:
            self.subdomain_results = f.read().strip() or "Không tìm thấy subdomain"
    def scan_httpx(self):
        if self.subdomain_results is None:
            self.scan_subdomains()
        
        result_file = f"./Result/{self.url}/httpx.txt"
        httpx_cmd = f"httpx -l ./Result/{self.url}/subdomain.txt -nc --no-fallback -tls-probe -csp-probe -title -vhost -td -status-code -fr -cdn -random-agent > {result_file}"
        subprocess.run(httpx_cmd, shell=True)
        
        with open(result_file, 'r') as f:
            self.httpx_results = f.read().strip() or "Không tìm thấy httpx"

    def get_subdomain_results(self):
        return self.subdomain

    def get_httpx_results(self):
        return self.httpx
    
    def get_port(self):
        return self.port
