import requests, re, json, time
from types import NoneType
from bs4 import BeautifulSoup as BS

def get_info(filename, one, two, newfilename):
    with open(f"JsonFiles/{filename}.json", "r", encoding="utf-8") as file:
        inventory_urls = json.load(file)
    inventory_urls = inventory_urls [one-1:two]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.2.834 Yowser/2.5 Safari/537.36"
    }

    #Добавление информации со страницы инвентаря
    print("Сбор инфы со страниц инвентаря:")
    all_info = {}
    t = 0
    for url in inventory_urls:
        #Сон против превышения запросов
        if t >= 28:
            print("Сон")
            time.sleep(150)
            t = 0 
    
        print(f"{inventory_urls.index(url)+1}-й пользователь")

        req = requests.get(url, headers=headers)
        t = t + 1       
        soup = BS(req.content, 'lxml')

        #Проверка на ошибки
        try:
            Err = soup.find("div", class_="error_ctn").find("h3").text
            if Err == "You've made too many requests recently. Please wait and try your request again later.":
                Err = "Сделано слишком много запросов"
                break
            elif Err == "The specified profile could not be found.":
                Err = "Ошибок нет"
                with open(f"JsonFiles/DeletedProfile-{newfilename}.json", "a", encoding="utf-8") as file:
                    json.dump(url, file, indent=4, ensure_ascii=False)
                    file.write("\n")
                continue
            else:
                with open(f"JsonFiles/Error-{url}.json", "w", encoding="utf-8") as file:
                    json.dump(Err, file, indent=4, ensure_ascii=False)
                Err = "Неизвестная ошибка"
                break
        except Exception:
            Err = "Ошибок нет"
            check_inventory = soup.find("div", class_="tabitems_ctn")
            if type (check_inventory) == NoneType:
                with open(f"JsonFiles/ClosedInventory-{newfilename}.json", "a", encoding="utf-8") as file:
                    json.dump(url, file, indent=4, ensure_ascii=False)
                    file.write("\n")
                continue

        #Получение URL Profile
        url_profile = url.replace("/inventory", "")
        #Получение ID Profile
        id_profile = url_profile.split("/")
        id_profile = id_profile[-1]

        #Получение SetSteamId
        findid = soup.find("div", class_="responsive_page_content").findAll(string=re.compile("UserYou.SetSteamId"))
        setsteamid = findid[0].split("\'")
        setsteamid = setsteamid[1]
        
        #Нахождение appid, contextid, название игр
        gamesforview = []
        games = []
        appid = []
        contextid = []
        checking = findid[0].split("appid\":")
        del checking[0]
        for a in checking:
            g = a.split(f",\"name\":\"")
            g = g[1].split("\"")
            gamesforview.append(g[0])

            b = a.split("\":{\"asset_count\":")
            del b[-1]
            for context in b:
                g = a.split(f",\"name\":\"")
                g = g[1].split("\"")
                games.append(g[0])
                app = a.split(",")
                appid.append(app[0])
                for i in range(1,len(context)):
                    if context[-i] == "\"":
                        context = context[-i+1:]
                        break
                contextid.append(context)

        #Создание шапки в Словарь
        all_info[f"{id_profile}"] = {
            "URL Profile": url_profile,
            "URL Inventory": url,
            "setsteamid": setsteamid,
            "Games": gamesforview,
            "games": games,
            "appid": appid,
            "contextid": contextid
        }

    #Запись инфы в файл
    with open(f"JsonFiles/Info-Profile-{newfilename}.json", "w", encoding="utf-8") as file:
        json.dump(all_info, file, indent=4, ensure_ascii=False)

    print(Err)
    if Err != "Ошибок нет":
        print(f"Последний собранный пользователь: {list(all_info.keys())[-1]}")
     
#Название Json файла с сылками на инвентарь, Номер id с которого начать, Номер id на котором закончить, Номер
get_info("URL inventory", 10009, 10025, "6")