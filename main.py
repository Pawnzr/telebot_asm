import telebot
from target_manager import Target, TargetManager
from env_var import authorized_users, TOKEN
import sqlite3
import subprocess
from app import create_directory, scan_subdomain
authorized_users = authorized_users
bot = telebot.TeleBot(TOKEN)
db_path = "database.db"

@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.reply_to(message, f'Xin chào :D đây là bot tele của An. \n Hướng dẫn sử dụng: \n /scan <target>')

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    
    if str(message.chat.id) in authorized_users:
        target = message.text.split()[1]
        target_obj = Target("",target,"","","")
        manager = TargetManager(db_path)
        manager.create_table()
        manager.add_target(target_obj)
        targets = manager.get_target_by_domain(target)
        if targets[3] == "":
            subdomains = scan_subdomain(target)
            manager.update_target_subdomain_by_domain(target, subdomains)
        else:
            subdomains = manager.get_target_by_domain(target)[3]
        

        
bot.infinity_polling()
