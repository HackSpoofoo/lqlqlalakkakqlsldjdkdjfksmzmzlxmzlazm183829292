import telebot
import random

bot = telebot.TeleBot('6496585628:AAHbTUc5f8EvygaGCIQxROFUs0suyXpPokk')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Сколько слов тебе нужно в тексте?')

@bot.message_handler(func=lambda message: True)
def generate_text(message):
    try:
        word_count = int(message.text)
        if word_count > 0:
            if word_count <= 10000:
                markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
                markup.add('Без ошибок', 'С ошибками')
                msg = bot.send_message(message.chat.id, 'Выбери вариант создания текста:', reply_markup=markup)
                bot.register_next_step_handler(msg, lambda m: generate_text_with_errors(m, word_count))
            else:
                bot.send_message(message.chat.id, 'Максимальное количество слов - 10000')
        else:
            bot.send_message(message.chat.id, 'Количество слов должно быть больше 0')
    except ValueError:
        bot.send_message(message.chat.id, 'Введите число')

def generate_text_with_errors(message, word_count):
    if message.text == 'Без ошибок':
        use_errors = False
        generate_text_with_percentage(message, word_count, use_errors, error_percentage=0)
    elif message.text == 'С ошибками':
        use_errors = True
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add('10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
        msg = bot.send_message(message.chat.id, 'Выбери процент ошибок:', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: generate_text_with_percentage(m, word_count, use_errors))
    else:
        bot.send_message(message.chat.id, 'Выберите вариант из предложенных')

def generate_text_with_percentage(message, word_count, use_errors):
    error_values = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    if message.text in error_values:
        error_percentage = int(message.text[:-1])
        text = generate_random_text(word_count, use_errors, error_percentage)
        with open('generated_text.txt', 'w') as file:
            file.write(text)
        bot.send_document(message.chat.id, open('generated_text.txt', 'rb'))
    else:
        bot.send_message(message.chat.id, 'Выберите вариант из предложенных')

def generate_random_text(word_count, use_errors=False, error_percentage=0):
    words = ['я', 'твою', 'мамашу', 'шалаву', 'ебал', 'ты', 'тупорылый', 'говноед', 'жопу', 'хуесос', 'мамку', 'слабачела', 'ебаная', 'нахуй', 'пидор', 'насиловал', 'маманю', 'закрой', 'ебло', 'отсосешь', 'хуй', 'пососи', 'ебанат', 'умрешь', 'на', 'текстах', 'я же твое ебало сломаю в два счета', 'закрой свой рыльник даун ебаный', 'дебилойд попробуй сказать что это генер', 'я те внатуое ебало сломаю нахуй щас', 'закрой уже свое ебало олень ебучий', 'нахуй ты много выебываешься если в итоге пиздв получишь', 'ты', 'сын говна', 'долбоеб ебаный', 'я тя ебал', 'свинья ебаная', 'ты', 'курица ебаная', 'ебашил твою голову хуем слышь', 'сука слово про генер скажи ебло сломаю', 'как нехуй делать', 'выебу твою мать и плюну в ебло ей', 'закрой свой ебасос даун', 'я же твою мамку трахну', 'ты на что надеешься хуйло', 'я тебе шанса не оставлю', 'выживать тебе придется среди яиц моих еблан', 'ебал тя книгой даун', 'нахуй ты мой пенис отсосал ебанат', 'дал право твоему отцу чтобы тот тебе в ебло въехал', 'ахаха попробуй сказать что либо про наличие ошибок', 'я твою мамашку ебал',  'нахуй ты мой пенис то пососал и бросил как собаке кость скажи мне, тупорылый ты говноед']
    generated_text = []
    while len(generated_text) < word_count:
        word = random.choice(words)
        generated_word = word_with_errors(word, error_percentage) if use_errors else word
        generated_text.append(generated_word)
    return ' '.join(generated_text)

def word_with_errors(word, error_percentage):
    error_rate = error_percentage / 100
    error_word = ''
    for letter in word:
        if random.random() < error_rate:
            error_word += random.choice('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        else:
            error_word += letter
    return error_word

bot.polling()
