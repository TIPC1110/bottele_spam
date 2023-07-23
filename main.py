import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import datetime

bot_token = '6252831853:AAGq-zBUk6Ded9C4sqjTH9150Pds2F56MmA' 
bot = telebot.TeleBot(bot_token)

allowed_group_id = -931515045

allowed_users = []
processes = []
ADMIN_ID = 6217429305

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()

def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY😾.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, ' VUI LÒNG NHẬP ID NGƯỜI DÙNG ')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'🚀NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /supersms.🚀')


load_users_from_database()

@bot.message_handler(commands=['laykey'])
def laykey(message):
    bot.reply_to(message, text='🚀 VUI LÒNG CHỜ ĐỢI! 🚀')

    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    url_key = requests.get(f'https://link4m.co/api-shorten/v2?api=63c3c7c54c38317d4e76ae5c&url=https://card1s.store/key?key!{key}').json()['shortenedUrl']
    
    text = f'''
- KEY Hôm Nay Của Bạn LÀ:
» {key} «
- Dùng Lệnh /key {{key của bạn}} ĐỂ Tiếp Tục
❗️[ Lưu ý: mỗi key chỉ có 1 người dùng ]❗️
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP KEY CỦA BẠN.')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, '🚀 KEY HỢP LỆ. Cảm Ơn Bạn Đã Ủng Hộ. Bây giờ bạn đã có thể sử dụng lệnh /supersms 🚀\n❗️[Lưu ý :mỗi key chỉ có 1 người dùng]❗️')
    else:
        bot.reply_to(message, '🚀 KEY KHÔNG HỢP LỆ.❗️\n❗️[Lưu ý :mỗi key chỉ có 1 người dùng]❗️')

@bot.message_handler(commands=['supersms'])
def lqm_sms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, text='BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY! Hãy /laykey để sử dụng lệnh này.')
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return

    if phone_number in ['113','911','114','115','+84328774559','0328774559','0865711812']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Spam spam cái địt mẹ mày, BỐ mày BAN mày luôn bây giờ chứ Spam cái địt mẹ mày à???")
        return

    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "120"])
    processes.append(process)
    bot.reply_to(message, f'⊂🚀⊃ BOOM ĐÃ LÊN NÒNG ⊂🚀⊃  \n➤ Bot 👾 : @spamlananh_bot \n┏➤ Tên Lửa Đã Chuẩn Bị Xong \n➤ ĐÃ PHÓNG 𝟮𝟬𝟬 💣 NGUYÊN TỬ TỚI \n➤ SĐT : » {phone_number} \n┗➤ Gói 💸 : [ 𝗩𝗶𝗣 ]\n ---- Những chi tiết khác----  \n༻ ┌» Thông tin «༻  \n༻ ├ SPAM » SMS ┇CALL « \n༻ ├ OWNER  » Manh Ti3n « \n༻ └ ADMIN  » Hoang Anh «')

@bot.message_handler(commands=['start'])
def how_to(message):
    how_to_text = '''
🚀Cách sử dụng và All lệnh của Bot:🚀
- Sử dụng lệnh /laykey để lấy key.
- Khi lấy key xong, sử dụng lệnh /key {key của bạn} để xác định key.
( ví dụ: /key keycuaban )
- /supersms <số điện thoại>: Gửi tin nhắn spam đến số điện thoại (chỉ người dùng được phép).
- /hdsd: Xem hướng dẫn để sử dụng các lệnh Spam của bot.
- /status: Xem thông tin về thời gian hoạt động, % CPU, % Memory, % Disk đang sử dụng của bot.
- /stop: Dừng lại tất cả các tệp sms.py đang chạy. ( Chỉ Quản Trị Viên Mới Được Dùng Lệnh Này
- /admin: Hiển thị thông tin admin.
- /owner: Hiển thị thông tin owner.
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['hdsd'])
def how_to(message):
    how_to_text = '''
🚀Hướng dẫn sử dụng:🚀
- Sử dụng lệnh /laykey để lấy key.
- Khi lấy key xong, sử dụng lệnh /key {key của bạn} để xác định key.
- Nếu key hợp lệ, bạn sẽ có quyền sử dụng lệnh /supersms {số điện thoại} để gửi tin nhắn và gọi.
- Chỉ những người dùng có key hợp lệ mới có quyền sử dụng các lệnh trên!.
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = '''
🚀Danh sách lệnh:🚀
- /supersms {số điện thoại}: Gửi tin nhắn SMS (chỉ người dùng đã lấy key).
- /laykey: Lấy key để sử dụng lệnh /supersms.
- /key {key của bạn}: Kiểm tra key và xác nhận quyền sử dụng lệnh /supersms.
- /how: Hướng dẫn sử dụng.
- /help: Danh sách lệnh.
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['admin'])
def how_to(message):
    how_to_text = '''
🚀Thông Tin Admin:🚀
- Hoang Anh🚀📱
- Owner Channel: https://t.me/HAHiPA

🚀Thông Tin Liên Hệ ☎️:🚀
- Facebook: ❌
- Zalo: ❌
- Instagram: ❌
- Telegram: @Hoang_Anhp
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['owner'])
def how_to(message):
    how_to_text = '''
🚀Thông Tin Owner:🚀
- Manh Ti3n🚀📱
- Owner Group: https://t.me/+8eM411Q0l8xjNGU9

🚀Thông Tin Liên Hệ ☎️:🚀
- Facebook: ❌
- Zalo: ❌
- Instagram: ❌
- Telegram: @Manh_Ti3n
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này😾.')
        return
    if user_id not in allowed_users:
        bot.reply_to(message, text='Bạn không có quyền sử dụng lệnh này😾.')
        return
    process_count = len(processes)
    bot.reply_to(message, f'🚀Số quy trình đang chạy:🚀 {process_count}.')

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Đã Khởi Động Lại BOOM.')
        return

    bot.reply_to(message, '🚀Bot sẽ được khởi động lại trong giây lát...🚀')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, '🚀Đã dừng lại tất cả các tệp sms.py đang chạy🚀.')
        return

    bot.reply_to(message, '🚀Đã dừng lại tất cả các tệp sms.py đang chạy🚀.')
    time.sleep(2)
    bot.stop_polling()



bot.polling()
