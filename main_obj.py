import telebot
from app import create_directory, read_file
import subprocess
import os
from env_var import authorized_users, TOKEN

authorized_users = authorized_users

bot = telebot.TeleBot(TOKEN)


class Target:
    def __init__(self, url):
        self.url = url
        self.subdomain_results = None
        self.httpx_results = None

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
        result_file = f"./Result/{self.url}/httpx.txt"
        if self.subdomain_results is None:
            self.scan_subdomains()
            

            
            httpx_cmd = f"httpx -l ./Result/{self.url}/subdomain.txt -nc --no-fallback -tls-probe -csp-probe -title -vhost -td -status-code -fr -cdn -random-agent > {result_file}"
            subprocess.run(httpx_cmd, shell=True)

        with open(result_file, 'r') as f:
            self.httpx_results = f.read().strip() or "Không tìm thấy httpx"

    def get_subdomain_results(self):
        return self.subdomain_results

    def get_httpx_results(self):
        return self.httpx_results


@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.reply_to(message, f'Xin chào :D đây là bot tele của An. \n Hướng dẫn sử dụng: \n /scan <target>')

@bot.message_handler(commands=['subdomain'])
def handle_subdomain(message):
    if message.chat.id in authorized_users:
        target = message.text.split()[1]
        target_obj = Target(target)
        target_obj.scan_subdomains()
        subdomain_results = target_obj.get_subdomain_results()
        bot.reply_to(message, subdomain_results)
    else:
        bot.reply_to(message, "Bạn không được phép sử dụng bot này.")


@bot.message_handler(commands=['httpx'])
def handle_httpx(message):
    if str(message.chat.id) in authorized_users:
        target = message.text.split()[1]
        target_obj = Target(target)
        target_obj.scan_httpx()
        subdomain_results = target_obj.get_subdomain_results()
        bot.reply_to(message, subdomain_results)
        # subdomain_results = target_obj.get_subdomain_results()
        # httpx_results = target_obj.get_httpx_results()
        bot.reply_to(message, subdomain_results)
        # bot.reply_to(message, httpx_results)
    else:
        bot.reply_to(message, "Bạn không được phép sử dụng bot này.")


@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        target = message.text.split()[1]
        target_obj = Target(target)
        bot.reply_to(message, f'Bắt đầu scan {target}')
        target_obj.scan_subdomains()
        subdomain_results = target_obj.get_subdomain_results()
        bot.reply_to(message, f"Kết quả subdomain:\n{subdomain_results}")
        target_obj.scan_httpx()
        httpx_results = target_obj.get_httpx_results()
        bot.reply_to(message, f"Kết quả httpx:\n{httpx_results}")
    except ValueError:
        bot.reply_to(message, 'Sai định dạng số. Vui lòng nhập hai số hợp lệ.')


bot.infinity_polling()
