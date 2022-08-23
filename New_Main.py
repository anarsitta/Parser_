
# Импорт библиотек
import asyncio
import sqlite3

from DexSpoParser import dexSpoData
from FonBetParser import fonBetData


connect = sqlite3.connect('matches.db')
cursor = connect.cursor()



# async def main():
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    


# Главная функция
if __name__ == '__main__':


    loop = asyncio.get_event_loop()
    # print(time.ctime(time_now))
    # print(time.ctime(element['startTimeTimestamp']))
    
    # loop.create_task(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=4&scopeMarket=1600'))
    # loop.run_until_complete(fonBetData('https://line52w.bk6bba-resources.com/line/desktop/topEvents3?place=live&sysId=1&lang=ru&salt=10qg1pg6bg0l6hq07hp&supertop=0&scopeMarket=1600', connect))
    loop.run_until_complete(dexSpoData('wss://prod.dexsport.work/ws?lang=en&cid=DexSport', connect))


