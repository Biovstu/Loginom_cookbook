import telebot

API_TOKEN = '5788009110:AAEP5l9JHGZjn1mULk6fIQRQ0Y3dqoV0srQ'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def take_start(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'{msg.from_user.full_name}!\nВаш ID {msg.from_user.id}')
    print(f'{msg.from_user.full_name}!\nВаш ID {msg.from_user.id}')

print('Бот запущен')

bot.polling()