
import requests
import time
import asyncio

# Функция сбора данных FonBet
async def fonBetData(url, connect):

    # Определение курсора
    cursor = connect.cursor()

    # Создание таблицы ФонБета
    cursor.execute("""CREATE TABLE IF NOT EXISTS FonBetTable(match_id INTEGER PRIMARY KEY, turnir_name TEXT, team1\
         TEXT, team2 TEXT, team1_koef REAL, team2_koef REAL, time_game Text, time_now Text )""") 

    # Гет запрос к нужным данным
    fonbet_data = requests.get(url).json()["events"]

    # Перебор полученных данных и выборка из них данных с киберспортом
    for element in fonbet_data:
        
        # Определение киберспортивных турниров
        if element['skName'] == 'Киберспорт':

            # Разбиение имени турнира
            compName = (element['competitionName']).split('.')

            time_now = time.time()
            # print(time.ctime(time_now))
            # print(time.ctime(element['startTimeTimestamp']))

            # Отсеивание игры Dota 2
            if(compName[0] == "Dota 2"):

                # Запрос в БД
                cursor.execute(f"""INSERT INTO FonBetTable(turnir_name, team1, team2, team1_koef, team2_koef, time_game, time_now) VALUES("{compName[0]+"."+compName[1]}",\
                    "{element['team1']}", "{element['team2']}", {element['markets'][0]['rows'][1]['cells'][1]['value']},\
                        {element['markets'][0]['rows'][1]['cells'][3]['value']}, '{element['startTimeTimestamp']}', '{time_now}');""")
                    
                # Обновление таблицы
                connect.commit()
    
    print("FonBet success")