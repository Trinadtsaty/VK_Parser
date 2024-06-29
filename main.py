from Config import tokens, find_params
from code1 import *
from datetime import datetime
from slicers import new_into_data
from MessangeBuilder import write_text_to_file
from telegram_bot import *

if __name__ == '__main__':

    time = datetime.datetime.now()
    path = "players_data"

    old_dataframe = pd.read_json("people_open_with_groups.json") # здесь должна быть последняя версия на текущий момент

    parsed_dataframe = run_parser(path,time) # записывает в папку с игроками 

    diff = new_into_data(parsed_dataframe, old_dataframe) 
    
    if len(diff) > 0:
        text = write_text_to_file(diff)
    else: 
        text = "Новых игроков нет"

    run_tg_bot(massage = text)
    
    pass # write 