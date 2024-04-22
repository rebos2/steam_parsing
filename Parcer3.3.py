#Парсинг URl-ссылок на ИНВЕНТАРЬ Steam (из Мастерской из коментариев)
import requests, time, json
from types import NoneType
from bs4 import BeautifulSoup as BS

def get_data(urls,p,filename):

    i = 1
    inventory_urls = []
    for url in urls:
        #Преобразование URL-ссылки
        req = requests.get(url)
        soup = BS(req.content, 'lxml')
        el = soup.find("div", class_='commentthread_area').get("id")
        el = el.split('_')[-3:-1]
        url = f"https://steamcommunity.com/comment/PublishedFile_Public/render/{el[0]}/{el[1]}"
        
        #Парсинг URL-ссылок из комментов
        print(f'Сбор URL-ссылок c {i}-й карты:')
        for page in range(1,p[i-1]+1):
            inventory_urls_onepage = []
            print(f'с {page}-й стрыницы')
            req = requests.get(url + f"?start={(page-1)*10}")
            find = req.text.split("<a href=")
            for a in find:
                b = a.split(" data-miniprofile=")
                inventory_urls_onepage.append(b[0].replace('\\','').replace('\"','')+'/inventory')
            del inventory_urls_onepage[0]
            inventory_urls.extend(inventory_urls_onepage)
        i = i+1
    L=len(inventory_urls)

    #Удаление повторяющихся URL-ссылок
    inventory_urls=list(set(inventory_urls))
    Ldel=L-len(inventory_urls)
    
    #Проверка на закрытый инвентарь и удаление из списка URL-ссылок
    print('\nПроверка на закрытый инвентарь:')
    i = 0
    t = 0
    inventory_urls.sort()
    for links in inventory_urls:
        print(f'{inventory_urls.index(links)+1}-й ссылки')
        req = requests.get(links)
        soup = BS(req.content, 'lxml')
        #Проверка на ошибки
        try:
            Err = soup.find("div", class_="error_ctn").find("h3").text
            if Err == "You've made too many requests recently. Please wait and try your request again later.":
                Err = "Сделано слишком много запросов"
                break
            elif Err == "The specified profile could not be found.":
                inventory_urls[inventory_urls.index(links)]="closedinventory"
                i = i + 1
                t = t + 1
            else:
                with open(f"JsonFiles/Error.json", "w", encoding="utf-8") as file:
                    json.dump(Err, file, indent=4, ensure_ascii=False)
                Err = "Неизвестная ошибка"
                break
        except Exception:
            Err = 'Просканировано без ошибок'
            check_inventory = soup.find("div", class_="tabitems_ctn")
            if type (check_inventory) == NoneType:
               inventory_urls[inventory_urls.index(links)]="closedinventory"
               i = i + 1
            t = t + 1
        #Сон против превышения запросов
        if t == 29:
          time.sleep(120)
          t = 0      
    inventory_urls.sort()
    del inventory_urls[:i]
    
    print(f'\nВсего собрано: {L} ссылок')
    print(f'Удалено: {Ldel} повторяющихся ссылок')
    print(f'Удалено: {i} ссылок с закрытым инвентарем')
    print(f'\nОсталось: {len(inventory_urls)} ссылок')
    print(f'\n{Err}\n')

    #Создание списка URL-ссылок на ивентарь
    with open(f"JsonFiles/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(inventory_urls, file, indent=4, ensure_ascii=False)

#Ввод ссылок на карты из Мастерской
URLs = [
    "https://steamcommunity.com/sharedfiles/filedetails/?id=243702660",
]

#Ввод количества считываемых старниц комментариев
pages = [450]

#Список Выполненного
info = []
for n in range(0,len(URLs)):
    info.append(
        {
            "Ссылка": URLs[n],
            "Колличество страниц": pages[n]
        }
    )
oldinfo = []
with open(f"JsonFiles/Info.json", "r", encoding="utf-8") as file:
    oldinfo = json.load(file)
info.extend(oldinfo)
with open(f"JsonFiles/Info.json", "w", encoding="utf-8") as file:
    json.dump(info, file, indent=4, ensure_ascii=False)

#Ссылки на карту из Мастерской, Количество считываемых старниц, название файла для записи
get_data(URLs,pages,"URL inventory 9")