import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(level=logging.INFO)


API_TOKEN = "введите токен бота"
bot = telebot.TeleBot(API_TOKEN)

# Список энергетиков и их цены, вы можете изменить
ENERGY_DRINKS = {
    "Red Bull": 320,
    "Monster": 219.99,
    "GORILLA": 140,
    "BURN": 140,
    "JAGUAR": 139.99,
    "LIT|ENERGY": 150,
    "MILANO": 130,
    "DRIVE": 140
}

# Хранение корзины пользователей
user_carzina = {}

#обработка команды старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Добро пожаловать в магазин энергетиков!\n"
                          "Используйте для просмотра /catalog\n"
                          "\n"
                          "Или  для ознакомления с /info о боте " )

#обработка команды каталог
@bot.message_handler(commands=['catalog'])
def catalog(message):
    keyboard = InlineKeyboardMarkup()
    for drink, price in ENERGY_DRINKS.items():
        button = InlineKeyboardButton(f"{drink} - {price}₽", callback_data=drink)
        keyboard.add(button)

    bot.send_message(message.chat.id, "Выберите энергетик:", reply_markup=keyboard)

#обработка команды инфо
@bot.message_handler(commands=['info'])
def info (message):
    bot.send_message(message.chat.id, 'команды бота:\n'
                                         '/start - включение и перезапуск бота\n'
                                         '/catalog - открывает каталог имеющихся энергетиков \n'
                                         '/checkout - переход к оплате \n'
                                         '/info - информация о боте  ')

#обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    drink = call.data
    price = ENERGY_DRINKS[drink]

    # Добавляем напиток в корзину
    user_id = call.from_user.id
    if user_id not in user_carzina:
        user_carzina[user_id] = []
    user_carzina[user_id].append(drink)

    bot.edit_message_text(
        text=f"Вы добавили {drink} в корзину. \n"
             f"Цена: {price}₽. \n"
             f"Используйте /checkout для оформления заказа.\n"
             f"Или для добавления: /catalog",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id)

#обработка команды чекаут
@bot.message_handler(commands=['checkout'])
def checkout(message):
    user_id = message.from_user.id
    if user_id not in user_carzina or not user_carzina[user_id]:
        bot.reply_to(message, "Ваша корзина пуста. Используйте  /catalog для добавления товаров.")
        return

    total_price = sum(ENERGY_DRINKS[drink] for drink in user_carzina[user_id])
    bot.reply_to(message,
                 f"Ваш заказ: {', '.join(user_carzina[user_id])}. \n"
                 f"Общая сумма: {total_price}₽.\nПожалуйста, переведите сумму на счет и отправьте подтверждение.\n"
                 f"\n"
                 f"счет: ('<code>2204 2401 9318 1510</code>') \n"
                 f"\n"
                 f"после оплаты ожидайте ответа администратора. Если в течение 2-5 часов не последует ответ от админа\n"
                 f"<u>деньги вернутся</u>!\n"
                 f"\n"
                 f"Так-же напоминаем что администратор <b>САМ</b> назначает время-встречи для передачи напитка в строго отведенном <b>МЕСТЕ</b> и <B>ВРЕМЕНИ</b>!\n"
                 f"\n"
                 f"если вы хотите начать занова то воспользуйтесь командой: /start", parse_mode='html')

    user_carzina[user_id] = []
    return

#что бы бот не выключался при первой команде (действовал бесконечно)

if __name__ == '__main__':
  bot.polling(none_stop=True)
