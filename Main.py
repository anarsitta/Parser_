
# Импорт библиотек
import asyncio
import requests

import websockets
import json




# Функция сбора данных FonBet
async def fonBetData(url):
    fonbet_data = requests.get(url).json()["events"]

    for element in fonbet_data:
        if element['skName'] == 'Киберспорт':
            print(element)

async def dexSpoData(url):
    # try:
    async with websockets.connect(url) as client:

        await client.send('["join","count",["dota2"]]')
        await client.send('["join","discipline",["4.dota2"]]')
        
        while True:
            try:
                data_id =  json.loads(await client.recv())[1][0][3]['tournamentIds']
                break
            except:
                continue

        await client.send(f'["join","tournament",{data_id}]'.replace("'", '"'))

        events = json.loads(await client.recv())
        print(events)

            # while True:
            #     events = json.dumps(await client.recv())
            #     break
    # except:
    #     print("Игры отсутствуют")


      
        

         


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dexSpoData('wss://prod.dexsport.work/ws?lang=en&cid=DexSport'))
    # fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600')
    pass