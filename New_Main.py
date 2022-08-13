
# Импорт библиотек
from ast import While
import asyncio
import requests

import websockets
import json




# Функция сбора данных FonBet
async def fonBetData(url):
    # Гет запрос к нужным данным
    fonbet_data = requests.get(url).json()["events"]

    # Перебор полученных данных и выборка из них данных с киберспортом
    for element in fonbet_data:
        if element['skName'] == 'Киберспорт':
            print(element)

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
                print('br')
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
            
        # Вывод списка с играми
        print(events)


      
# Главная функция
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dexSpoData('wss://prod.dexsport.work/ws?lang=en&cid=DexSport'))
    # fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600')