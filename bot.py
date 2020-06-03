import telebot
import config
import pymysql
import pymysql.cursors

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('img/welcome.tgs','rb')
	bot.send_sticker(message.chat.id, sti)

	markup = types.InlineKeyboardMarkup(row_width=2)

	# keyboard сюда категории из таблички
	connection = pymysql.connect(
		host='95.216.155.184',
		user="whydohow",
		password="Admin",
		db="whydohowdb"
	)
	with connection.cursor() as cursor:
		query = "SELECT `id_category` FROM `category`"
		cursor.execute(query)
		for row in cursor:
			strin = str(row)[2:len(row) - 4]
			item = types.InlineKeyboardButton(strin,callback_data=strin)
			markup.add(item)
	bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			connection = pymysql.connect(
				host='95.216.155.184',
				user="whydohow",
				password="Admin",
				db="whydohowdb"
			)
			with connection.cursor() as cursor:
				query = "SELECT `id_post` FROM `post` WHERE `id_category` = '" + call.data + "' ORDER BY popularity DESC LIMIT 10"
				cursor.execute(query)
				i=1
				for row in cursor:
					strin = str(i) + ") http://i668320w.beget.tech/viewpost.php?id=" + str(row)[1:len(row) - 3]
					bot.send_message(call.message.chat.id, strin)
					i+=1
				if i == 1:
					bot.send_message(call.message.chat.id, "Таких постов пока нет!")
			#https: // whydohow.000webhostapp.com / post.php?id =
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию",reply_markup=None)

	except Exception as e:
		print(repr(e))

#Run
bot.polling(none_stop=True)