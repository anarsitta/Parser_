
# Импорт библиотек
import asyncio
import websockets
import json
import sqlite3

from FonBetParser import fonBetData


connect = sqlite3.connect('matches.db')
cursor = connect.cursor()

# Функция сбора данных DexSport
async def dexSpoData(url):
    cursor.execute("""CREATE TABLE IF NOT EXISTS DexSpoTable(match_id INTEGER PRIMARY KEY, turnir_name TEXT, team1\
            TEXT, team2 TEXT, team1_koef REAL, team2_koef REAL, time_game Text, time_now Text )""") 

    # Подключение к веб сокету
    async with websockets.connect(url) as client:
  
        # Отправка нужных ключей, для получения начальных данных
        await client.send('["join","line",["2"]]')
        await client.send('["join","count",["football"]]')
        await client.send('["join","discipline",["2.football"]]')
        
        while True:
            ret_data = json.loads(await client.recv())

            if ret_data[0] == "batch" and ret_data[1][0][0] == "discipline":
                ret_data = ret_data[1][0][3]['tournamentIds']
                print('Выход')
                break


        await client.send(f'["join","tournament",{ret_data}]'.replace("'", '"'))
        
        # Получение и отсеивание не нужных данных
        events_ids = json.loads(await client.recv())[1][0][3]['eventIds']

        # Новый запрос с ключами
        await client.send(f'["join","event",{events_ids}]'.replace("'", '"'))

        # Получение списка с данными
        events_list = json.loads(await client.recv())[1]
        print(events_list)

        # Перебор списка с данными, а также вызов и запись одной игры(3 ключа и 3 ответа) в 1 список 
        for i in events_list:
            j = i[3]['mainMarketIds']
            print(j)
            await client.send( f'["join", "market",{j}]'.replace("'", '"') )
            print(json.loads(await client.recv()))

            # cursor.execute(f"""INSERT INTO FonBetTable(turnir_name, team1, team2, team1_koef, team2_koef, time_game, time_now) VALUES("{}",\
            #         "{}", "{}", {}, {}, '{}', '{}');""")
        



# async def main():
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    


# Главная функция
if __name__ == '__main__':


    loop = asyncio.get_event_loop()
    
    
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    # loop.run_until_complete(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=0&scopeMarket=1600', connect))
    
    loop.run_until_complete(dexSpoData('wss://prod.dexsport.work/ws?lang=en&cid=DexSport'))


