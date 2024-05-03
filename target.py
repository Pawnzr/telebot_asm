from app import create_directory,  read_file
import subprocess
import os
class Target:
    def __init__(self, url):
        self.url = url
        self.subdomains = None
        self.httpx = None
        self.ports = None
        
    def save_to_sqlite(self, conn):
        # Create the table if it doesn't exist
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    subdomains TEXT,
                    ports TEXT,
                    httpx TEXT
                    )''')

        # Insert data into the table
        c.execute("INSERT INTO targets (url, subdomains, httpx, ports ) VALUES (?, ?, ?, ?)",
                  (self.url, self.subdomains, self.httpx, self.ports))
        conn.commit()
        
    def scan_subdomains(self, conn):
        try:
            result_path = f"./Result/{self.url}"
            result_file = f"{result_path}/subdomains.txt"
            c = conn.cursor()
            c.execute("SELECT subdomains FROM targets WHERE url = ?", (self.url,))
            existing_subdomains = c.fetchone()
            if not existing_subdomains:
            # if not os.path.exists(result_path):
            #     create_directory(result_path)
                subdomains_cmd = f"subfinder -d {self.url} > {result_file}"
                subprocess.run(subdomains_cmd, shell=True)
                with open(result_file, 'r') as f:
                    self.subdomains = f.read().strip() or "Không tìm thấy subdomains hahaha ngu "
            self.insert_subdomains(conn)

        except Exception as e:
            self.subdomains = f"Không tìm thấy subdomains hahaha except {e}"

    def scan_httpx(self, conn):
        try:
            result_file = f"./Result/{self.url}/httpx.txt"
            if self.subdomains is None:
                self.scan_subdomains(conn)
            if self.httpx is None:
                httpx_cmd = f"httpx -l ./Result/{self.url}/subdomain.txt -nc --no-fallback -tls-probe -csp-probe -title -vhost -td -status-code -fr -cdn -random-agent > {result_file}"
                subprocess.run(httpx_cmd, shell=True)

            with open(result_file, 'r') as f:
                self.httpx = f.read().strip() or "Không tìm thấy Httpx"
        except:
            self.httpx = "Lỗi khi chạy Httpx"

    def get_subdomain(self, conn):
        if self.subdomains is None:
            self.scan_subdomains(conn)
        if self.subdomains:
            return self.subdomains
        try:
            c = conn.cursor()
            c.execute("SELECT subdomains FROM targets WHERE url = ?", (self.url,))
            subdomains_data = c.fetchone()
            if subdomains_data:
                self.subdomains = subdomains_data[0]
            return self.subdomains
        except:
            # Handle any exceptions during database retrieval
            return "Lỗi khi truy cập cơ sở dữ liệu"
    def insert_subdomains(self, conn):
    # Check if subdomains have been scanned
        if self.subdomains is None:
            # Scan for subdomains if not already scanned
            self.scan_subdomains()

        # If subdomains are available, insert them into the database
        if self.subdomains:
            c = conn.cursor()
            c.execute("UPDATE targets SET subdomains = ? WHERE url = ?", (self.subdomains, self.url))
            conn.commit()


    def get_httpx(self, ):
        return self.httpx
    
    
