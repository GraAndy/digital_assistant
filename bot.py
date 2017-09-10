# -*- coding: utf-8 -*-
import config
import telebot
import requests
import yandex

bot = telebot.TeleBot(config.token)

def get_text_from_voice(id):
    file_info = bot.get_file(id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path))
    text = yandex.speech_to_text(bytes=file.content)
    return text

def get_answer(text):
    answer = 'Повторите ваш вопрос.'
    for key in config.unit_to_multiplier:
        if key in text:
            answer = config.unit_to_multiplier[key]
            break
    return answer

# Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    text = get_text_from_voice(message.voice.file_id)
    answer = get_answer(text)
    bot.send_message(message.chat.id, 'Вы спросили: ' + text)
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
     bot.polling(none_stop=True)