import telebot
from target import Target
from app import create_directory, read_file
from env_var import authorized_users, TOKEN
import sqlite3

authorized_users = authorized_users
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.reply_to(message, f'Xin chào :D đây là bot tele của An. \n Hướng dẫn sử dụng: \n /scan <target>')

@bot.message_handler(commands=['subdomain'])
def handle_subdomain(message):
    conn = sqlite3.connect('mydatabase.db')
    if str(message.chat.id) in authorized_users:
        target = message.text.split()[1]
        target_obj = Target(target)
        subdomains = target_obj.get_subdomain()
        if subdomains:
            bot.reply_to(message, subdomains)
        else:
            target_obj.scan_subdomains()
            subdomains = target_obj.get_subdomain()
            bot.reply_to(message, subdomains)
        target_obj.save_to_sqlite(conn)
    else:
        bot.reply_to(message, "Bạn không được phép sử dụng bot này.")


@bot.message_handler(commands=['httpx'])
def handle_httpx(message):
    conn = sqlite3.connect('mydatabase.db')
    if str(message.chat.id) in authorized_users:
        target = message.text.split()[1]
        target_obj = Target(target)
        if target_obj.httpx:
            bot.reply_to(message, target.httpx)
        target_obj.scan_httpx()
        subdomain_results = target_obj.get_subdomain()
        bot.reply_to(message, subdomain_results)
        # subdomain_results = target_obj.get_subdomain_results()
        # httpx_results = target_obj.get_httpx()
        bot.reply_to(message, subdomain_results)
        # bot.reply_to(message, httpx_results)
        target_obj.save_to_sqlite(conn)
    else:
        bot.reply_to(message, "Bạn không được phép sử dụng bot này.")


@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        target = message.text.split()[1]
        target_obj = Target(target)
        bot.reply_to(message, f'Bắt đầu scan {target}')
        target_obj.scan_subdomains()
        subdomain_results = target_obj.get_subdomain()
        bot.reply_to(message, f"Kết quả subdomain:\n{subdomain_results}")
        target_obj.scan_httpx()
        httpx_results = target_obj.get_httpx()
        bot.reply_to(message, f"Kết quả httpx:\n{httpx_results}")
    except ValueError:
        bot.reply_to(message, 'Sai định dạng số. Vui lòng nhập hai số hợp lệ.')

bot.infinity_polling()
