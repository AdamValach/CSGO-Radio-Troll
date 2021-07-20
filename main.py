import telnetlib
import keyboard
import items
import config
import random

colors = {
    "lightblue": "",
    "blue": "",
    "pink": "",
    "red": "",
}


def connect():
    print(f'Conencting to the CSGO Telnet at {config.HOST}:{str(config.PORT)}')
    try:
        tn = telnetlib.Telnet(config.HOST, config.PORT)
    except ConnectionRefusedError:
        print(
            f'Connection error. Make sure you have CSGO running and set the -netconport {str(config.PORT)} launch option')
        exit(1)
    return tn


def start_up_check():
    if config.BLUE_UNBOX_CHANCE + config.PINK_UNBOX_CHANCE + config.KNIFE_UNBOX_CHANCE != 100:
        print("Wrong unbox probability values set in the config. Sum of the chances have to be 100%")
        exit(1)
    if config.DECOY_OUT_CHANCE + config.FLASHBANG_OUT_CHANCE + config.SMOKE_OUT_CHANCE + config.NO_RADIO_VOICEMESSAGE_CHANCE != 100:
        print("Wrong radio phrase probability values set in the config. Sum of the values have to be 100%")
        exit(1)


def get_item_rarity():
    rand = random.randint(0, 10000)
    if config.BLUE_UNBOX_CHANCE != 0 and rand < config.BLUE_UNBOX_CHANCE * 100:
        return "blue"
    elif config.PINK_UNBOX_CHANCE != 0 and rand < (config.BLUE_UNBOX_CHANCE + config.PINK_UNBOX_CHANCE) * 100:
        return "pink"
    else:
        return "knife"


def get_random_collection(rarity):
    list_of_collections = []
    for key in items.ITEMS[rarity]:
        list_of_collections.append(key)
    return random.choice(list_of_collections)


def get_random_knife():
    return random.choice(items.KNIVES)


def get_random_knife_finish():
    return random.choice(items.KNIFE_FINISHES)


def get_random_item(rarity):
    if rarity != "knife":
        item_collection = get_random_collection(rarity)
        return colors[rarity] + random.choice(items.ITEMS[rarity][item_collection])
    else:
        return f"★ {get_random_knife()} | {get_random_knife_finish()}"


def get_random_voicemessage():
    rand = random.randint(0, 10000)
    if config.DECOY_OUT_CHANCE != 0 and rand < config.DECOY_OUT_CHANCE * 100:
        return "Radio.Decoy"
    elif config.FLASHBANG_OUT_CHANCE != 0 and rand < (config.DECOY_OUT_CHANCE + config.FLASHBANG_OUT_CHANCE) * 100:
        return "Radio.Flashbang"
    elif config.SMOKE_OUT_CHANCE != 0 and rand < (
            config.DECOY_OUT_CHANCE + config.FLASHBANG_OUT_CHANCE + config.SMOKE_OUT_CHANCE) * 100:
        return "Radio.Smoke"
    else:
        return "X"


def get_message():
    rarity = get_item_rarity()
    item = get_random_item(rarity)
    voice_message = get_random_voicemessage()

    message = f'playerradio {voice_message} "'
    if voice_message == "Radio.Decoy":
        message += "Decoy Out!"
    elif voice_message == "Radio.Flashbang":
        message += "Flashbang Out!"
    elif voice_message == "Radio.Smoke":
        message += "Smoke Out!"
    message += f' {config.PLAYERNAME} has opened a container and found: {item}\n'
    print(message)
    return message


tn = connect()
if tn is None:
    exit(1)
else:
    print("Successfully connected")

while True:
    keyboard.wait(config.KEYBIND)
    tn.write(str.encode(get_message()))
