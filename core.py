import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from main.pref import *

def send_keyboard_message(vk, peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open('common/keyboards/refactoring.json', "r", encoding='utf-8-sig').read()
    )

def get_message(event):
    message = event.obj['text'].lower()
    if '[club198702757|@club198702757]' in message:
        message = message.replace('[club198702757|@club198702757] ', '')
    else:
        message = message.replace('[club198702757|тайное общество ктбо 1-3] ', '')
        
    return message

def connect_to_chat():
    bot_session = vk_api.VkApi(
    token=CHAT_TOKEN)
    vk = bot_session.get_api()
    longpoll = VkBotLongPoll(bot_session, ID)
    
    return longpoll, vk

def communication(longpoll, vk):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                message = get_message(event)
                if message == 'а где?':
                    send_keyboard_message(vk, event.chat_id, 'Sorry, but we need to close this bot for the duration of the refactoring. Good luck!')
    
    
if __name__ == "__main__":
    longpoll, vk = connect_to_chat()
    communication(longpoll, vk)
    