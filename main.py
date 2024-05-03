import telebot
from target_manager import Target, TargetManager
from env_var import authorized_users, TOKEN
import sqlite3
import subprocess
from app import *
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
        ip = resolve_domain_to_ip(target)
        
        target_obj = Target(ip,target,"","","")
        
        manager = TargetManager(db_path)
        manager.create_table()
        manager.add_target(target_obj)
        targets = manager.get_target_by_domain(target)
        
        if targets[3] == "":
            subdomains = scan_subdomain(target)
            manager.update_target_subdomain_by_domain(target, subdomains)
        else:
            subdomains = manager.get_target_by_domain(target)[3]

        if targets[2] == "":
            ports = scan_port(ip)
            manager.update_target_port_by_ip(ip, str(ports))
        else:
            ports = manager.get_target_by_domain(target)[2]

        bot.reply_to(message,targets)

        # for subdomain in subdomains.split("\n"):
        #     ip = resolve_domain_to_ip(subdomain)
        #     target_object = Target(ip,subdomain,"","","")
        #     manager.add_target(target_object)
            

        
bot.infinity_polling()
