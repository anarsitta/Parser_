
import asyncio
import websockets
import json
import time


# Функция сбора данных DexSport
async def dexSpoData(url, connect):
    try:
        # Определение курсора
        cursor = connect.cursor()

        # Созднаие таблицы
        cursor.execute("""CREATE TABLE IF NOT EXISTS DexSpoTable(match_id INTEGER PRIMARY KEY, team1\
                TEXT, team2 TEXT, team1_koef REAL, team2_koef REAL, time_game Text, time_now Text )""") 

        # Подключение к веб сокету
        async with websockets.connect(url) as client:

            # Отправка нужных ключей, для получения начальных данных
            await client.send('["join","line",["2"]]')
            await client.send('["join","count",["dota2"]]')
            await client.send('["join","discipline",["2.dota2"]]')
            
            # перебор данных
            for i in range(10):
                # Получение данных
                ret_data = json.loads(await client.recv())

                # Проверка наличия матчей
                if ret_data[0] == "batch" and ret_data[1][0][0] == 'count':
                    if ret_data[1][0][3]['dota2']['live'] == 0:
                        raise Exception('Матчи отсутствуют')

                # Получение номеров игр
                if ret_data[0] == "batch" and ret_data[1][0][0] == "discipline":
                    ret_data = ret_data[1][0][3]['tournamentIds']
                    break

            # Отправка ключа
            await client.send(f'["join","tournament",{ret_data}]'.replace("'", '"'))
            
            # Получение и отсеивание не нужных данных
            events_ids = json.loads(await client.recv())[1][0][3]['eventIds']

            # Новый запрос с ключами
            await client.send(f'["join","event",{events_ids}]'.replace("'", '"'))

            # Получение списка с данными
            events_list = json.loads(await client.recv())[1]

            # Перебор списка с данными, а также вызов и запись одной игры(3 ключа и 3 ответа) в 1 список 
            for i in events_list:
                
                # Получение нынешнего времени
                time_now = time.time()

                # Получение ид маркета
                j = i[3]['mainMarketIds']

                # Отправка данных
                await client.send( f'["join", "market",{j}]'.replace("'", '"') )

                # Получение данных
                data = json.loads(await client.recv())

                # Добавление данных в БД
                cursor.execute(f"""INSERT INTO DexSpoTable(team1, team2, team1_koef, team2_koef, time_game, time_now) VALUES("{data[1][0][3]['outcomes'][0]['name']}",\
                        "{data[1][0][3]['outcomes'][1]['name']}", {data[1][0][3]['outcomes'][0]['price']}, {data[1][0][3]['outcomes'][1]['price']},\
                            '{i[3]['startTime']}', '{time_now}');""")
                
                # Обновление таблицы
                connect.commit()
            
            # Сообщение о том что считывание выполнено
            print('DexSport Success')

    except Exception as ex:
        # Вывод ошибки
        print(ex)