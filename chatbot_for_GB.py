import telebot
import json


API_TOKEN='5890357652:AAH0Q6hKziZqCiPtL0JKw-qJQIuhmqmuZmk'

select=''
# delete=False
# add=False
# find = False
text=''
data=[]
phone =[]
commands =['/start','/add','/all','/stop','/delete','/save','/load','/random']
base={}
def save ():
    with open("phone.json",'w',encoding='utf-8') as fh:
        fh.write(json.dumps(base,ensure_ascii=False))
        print('Наша база телефонов была успешно сохранена в файле')
def load ():
    with open("phone.json", 'r', encoding='utf-8') as fh:
        global base
        base = json.load(fh)
        print('Наша база телефонов была успешно загружена')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Готов к работе!")
    bot.send_message(message.chat.id, "Команды по работе с телефонным спарвочником /add /all /stop /delete /find")
@bot.message_handler(commands=['add'])
def show_message(message):
    global select
    select='add'
    bot.send_message(message.chat.id,'Введите фамилию и телефоны через пробел' )

@bot.message_handler(commands=['all'])
def show_message(message):

    bot.send_message(message.chat.id,'В базе есть:')
    load()
    for key, value in base.items():
        s = (f'{key} {value}')
        print(s)
        bot.send_message(message.chat.id, s)
@bot.message_handler(commands=['find'])
def show_message(message):
    bot.send_message(message.chat.id, 'Какую запись нужно найти?')
    global select
    select = 'find'


@bot.message_handler(commands=['delete'])
def show_message(message):
    bot.send_message(message.chat.id,'Какую запись нужно удалить?')
    global select
    select = 'delete'

@bot.message_handler(commands=['stop'])
def show_message(message):
    global select
    select = 'stop'
    bot.send_message(message.chat.id, 'Работу закончил! До новых встреч!')


@bot.message_handler(content_types='text')
def check_message(message):
    if select=='add':
        load()
        data=message.text.split()
        phone.clear()
        for i in range (1,len(data)):
            phone.append(data[i])
        s=(f'{data[0]} успешно сохранен')
        bot.send_message(message.chat.id,s)
        base.update({data[0] : phone})
        save()
    if select=='delete':


        load()
        phone.clear()
        data = message.text

        check = True
        for key in base.keys():
            if key == data:
                base.pop(key)
                check = False
                s = (f'Я успешно удалил  {data} ')
                save()
                bot.send_message(message.chat.id, s)
                break
        if check == True: bot.send_message(message.chat.id, 'С такими данными в базе никого нет')



    if select=='find':

        load()
        phone.clear()
        data = message.text

        check=True
        s = (f'По значению {data} найдены:')
        bot.send_message(message.chat.id, s)
        for key, value in base.items():
            if key == data:
                s = (f'{key} {value}')
                check=False
                print(s)
                bot.send_message(message.chat.id, s)
            for i in value:
                if data==i:
                    s = (f'{key} {value}')
                    check = False
                    print(s)
                    bot.send_message(message.chat.id, s)

        if check==True: bot.send_message(message.chat.id, 'С такими данными в базе никого нет')
    if select == 'stop':

        exit()

bot.polling()