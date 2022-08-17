
# Импорт библиотек
import asyncio
import requests

import websockets
import json

import sqlite3



connect = sqlite3.connect('matches.db')
cursor = connect.cursor()



# Функция сбора данных FonBet
async def fonBetData(url):

    # Создание таблицы ФонБета
    cursor.execute("""CREATE TABLE IF NOT EXISTS FonBetTable(match_id INTEGER PRIMARY KEY, turnir_name TEXT, team1\
         TEXT, team2 TEXT, team1_koef REAL, team2_koef REAL)""")  #Добавить время, пригодится в будущем

    # Гет запрос к нужным данным
    fonbet_data = requests.get(url).json()["events"]

    # Перебор полученных данных и выборка из них данных с киберспортом
    for element in fonbet_data:

        # Определение киберспортивных турниров
        if element['skName'] == 'Киберспорт':
            
            # Разбиение имени турнира
            compName = (element['competitionName']).split('.')

            # Отсеивание игры Dota 2
            if(compName[0] == "Dota 2"):

                # Запрос в БД
                cursor.execute(f"""INSERT INTO FonBetTable(turnir_name, team1, team2, team1_koef, team2_koef)\
                    VALUES("{compName[0]+"."+compName[1]}", "{element['team1']}", "{element['team2']}",\
                        {element['markets'][0]['rows'][1]['cells'][1]['value']}, {element['markets'][0]['rows'][1]['cells'][3]['value']});""")
                
                # Обновление таблицы
                connect.commit()
    
    print("FonBet success")


# Функция сбора данных DexSport
async def dexSpoData(url):

    # Подключение к веб сокету
    async with websockets.connect(url) as client:

        # Отправка нужных ключей, для получения начальных данных
        await client.send('["join","count",["dota2"]]')
        await client.send('["join","discipline",["4.dota2"]]')

        # Скип не нужных данных
        while True:
            try:
                data_id =  json.loads(await client.recv())[1][0][3]['tournamentIds']
                break
            except:
                continue

        # Отправка новых ключей, из полученных ключей
        await client.send(f'["join","tournament",{data_id}]'.replace("'", '"'))

        # Получение и отсеивание не нужных данных
        events_ids = json.loads(await client.recv())[1][0][3]['eventIds']

        # Новый запрос с ключами
        await client.send(f'["join","event",{events_ids}]'.replace("'", '"'))

        # Получение списка с данными
        events_list = json.loads(await client.recv())[1]
        events = []

        # Перебор списка с данными, а также вызов и запись одной игры(3 ключа и 3 ответа) в 1 список 
        for i in events_list:
            j = i[3]['mainMarketIds']
            await client.send( f'["join", "market",{j}]'.replace("'", '"') )
            events.append(json.loads(await client.recv())[1])
        
        print(events)



# async def main():
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    


# Главная функция
if __name__ == '__main__':

    


    loop = asyncio.get_event_loop()
    
    
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    loop.run_until_complete(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    
    # loop.run_until_complete(dexSpoData('wss://prod.dexsport.work/ws?lang=en&cid=DexSport'))


