from durakonline import durakonline
from datetime import datetime
from threading import Thread
from colorama import Fore, Back, Style
import time
wins = 0

MAIN_TOKEN = "$2a$06$gqO.jKJWHJ7aCMRkKd4YSe"
BOT_TOKEN = "$2a$06$EIOW8.vnsUhSRNSTnNpmK."

servers = ["u9","uA","uB","uC","uD"]

def start_game(main, bot, s) -> None:
    game = bot.game.create(100, "3095", 2, 24, ch=True, fast=True)

    main.game.join("3095", game.id)
    main._get_data("game")
    for i in range(bot.info['points']):
        main.game.ready()
        bot.game.ready()
        global wins
        wins +=1  
        print(Fore.YELLOW + f"Сервер: [{s}] Время игры: [{datetime.now().strftime('%H:%M:%S')}] Количество сделанных побед: [{wins}]")
        for card_index in range(4):
            main_cards = main._get_data("hand")["cards"]
            bot_cards = bot._get_data("hand")["cards"]
            if len(main_cards) <= 0 and len(bot_cards) <= 0:
                continue
            mode = bot._get_data("mode")
            if mode["0"] == 1:
                bot.game.turn(bot_cards[0])
                time.sleep(.1)
                main.game.take()
                time.sleep(.1)
                bot.game._pass()
            else:
                main.game.turn(main_cards[0])
                time.sleep(.1)
                bot.game.take()
                time.sleep(.1)
                main.game._pass()       
        bot.game.surrender()
        bot._get_data("game_over")

def start_thread(server: str) -> None:  
    main = durakonline.Client(MAIN_TOKEN, server_id = server, tag = "[MAIN]", debug =False, pl="android")
    bot = durakonline.Client(BOT_TOKEN, server_id = server, tag = "[BOT]", debug =False, pl="android")
    start_game(main, bot, server)
    
for server in servers:
    drain_Thread = Thread(target = start_thread, args=(server,)).start()
