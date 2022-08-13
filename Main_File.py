
# Импорт библиотек
from bs4 import BeautifulSoup as BS
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pandas as pd
from pprint import pprint




# Функций получения данных
def get_data(url, file_name):

    # Проверка ошибки
    try:
        # Объявление опций
        options = Options()
        options.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36]")
        options.page_load_strategy = 'normal'

        # Создание драйвера
        driver = webdriver.Chrome(
            executable_path= "chromedriver.exe",
            options=options)

        driver.get(url=url)
        time.sleep(10)

        # Запись в файл
        with open(file_name + ".html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        return driver.page_source

    # Вывод ошибки
    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit() 

# Функция обработки данных сайта FonBet
def print_fon_bet(data):
    soup = BS(data, "lxml")

    # Таблица полных игр
    live_elements = (soup.find("div", class_ = "sport-section-virtual-list--6lYPY").__dict__)['contents']

    # Определения наличия игр
    if live_elements[0].find("div", class_ = "sport-section__caption--7bUR8").text == "Киберспорт":
        
        # Перебор онлайновых матчей
        for element in live_elements[1:]:

            # Обработка и определение игры
            if element.find("div", class_ = "table-component-text--5BmeJ") != None:
                if (((element.find("div", class_ = "table-component-text--5BmeJ").text).split('.')[0]).upper()) in games:
                    game = (element.find("div", class_ = "table-component-text--5BmeJ").text).split('.')[0]
                    continue

            # Определение названия игры(команд) (Если названия нет, то это разделитель TRAP)
            if element.find("a", class_ = "sport-event__name--HefZL") != None:
                game_name = element.find("a", class_ = "sport-event__name--HefZL").text
                link = element.find("a", class_ = "sport-event__name--HefZL").get('href')

            elif element.find("div", class_ = "sport-sub-event__name--3fwZy") != None:
                game_name = element.find("div", class_ = "sport-sub-event__name--3fwZy").text

            else:
                continue
            
            # Коэффициенты, 0 - 1 коэф, 1 - '-', 2 - 2 коэф
            koef = element.findAll("div", class_ = "table-component-factor-value_single--6nfox")

            # пока просто принт
            print(game + "\t" + game_name +"\t"+koef[0].text+"\t"+koef[2].text +"\thttps://www.fon.bet/" + link)    

    # Матчей нет - F
    else:
        return ('Нету матчей в прямом эфире.')

# Функция обработки данных сайта DexSport
def print_dex_sport(data):
    pass

games = ["DOTA 2", "LOL", "KOG", "ROCKET LEAGUE", "CALL OF DUTY", "RAINBOW SIX SIEGE", "VALORANT", "COUNTER-STRIKE"]

# Запуск скрипта
if __name__ == '__main__':

    # Получение данных
    fonBet_data = get_data('https://www.fon.bet/live/esports/', 'fonbet')
    # dexSport_data = get_data('https://mainnet.dexsport.io/sports?setIframePath=%2Fdota2', 'dexsport') 

    # Обработка полученных данных
    print_fon_bet(fonBet_data)
    
    # with open("dexsport.html", encoding="utf-8") as file:
    #     dexSport_data = file.read()

    # soup = BS(dexSport_data, "lxml")

    # print(soup.text)

    # Не могу на них зайти
    # pinnacle_data = get_data('http://pinnacle.com/')
    # bet365_data = get_data('https://www.bet365.com/')
    
    
