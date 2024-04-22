import requests, json, time

def get_info(N):
    with open(f"JsonFiles/Info-Profile-{N}.json", "r", encoding="utf-8") as file:
        all_info = json.load(file)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.2.834 Yowser/2.5 Safari/537.36"
    }

    t = 0
    Err = []
    ErrList = []
    #Добавление информации о шмотках
    print("\nСбор инфы о шмотках:")
    for k in all_info:
        print(f"ID:{k}")
        setsteamid = all_info[k]["setsteamid"]
        games = all_info[k]["games"]
        appid = all_info[k]["appid"]
        contextid = all_info[k]["contextid"]

        for n in range(0,len(appid)):
            #Сон против превышения запросов
            if t > 199:
                print("Сон")
                time.sleep(30)
                t = 0

            print(f"Считывание {n+1}-й инфо-страницы")
            try:
                t = t + 1
                req_assets = requests.get(f"https://steamcommunity.com/inventory/{setsteamid}/{appid[n]}/{contextid[n]}?l=english&count=5000", headers=headers)
            except requests.exceptions.ProxyError:
                ErrList.append(k)
                Err.append(f"ID:{k} | appid:{n} | Ошибка: \"ProxyError\"")
                print("ProxyError\nСон")
                time.sleep(360)
                break

            #Собираем info
            try:
                info = req_assets.text.split("descriptions\":[{\"appid")
                assets_info = info[0]
                descriptions_info = info[1]
            except Exception:
                ErrList.append(k)
                Err.append(f"ID:{k} | appid:{n} | Ошибка:{req_assets.text}")
                print("Ошибка на инфо-странице\nСон")
                time.sleep(360)
                break
                        
            #Нахождение assetid
            assetid_info = assets_info.split("assetid\":\"")
            assetid = []
            for a in assetid_info:
                b = a.split("\"")
                assetid.append(b[0])
            del assetid[0]

            #Нахождение classid
            classid_info = assets_info.split("classid\":\"")
            classid = []
            for a in classid_info:
                b = a.split("\"")
                classid.append(b[0])
            del classid[0]

            #Нахождение instanceid
            instanceid_info = assets_info.split("instanceid\":\"")
            instanceid = []
            for a in instanceid_info:
                b = a.split("\"")
                instanceid.append(b[0])
            del instanceid[0]

            #Нахождение amount
            amount_info = assets_info.split("amount\":\"")
            amount = []
            for a in amount_info:
                b = a.split("\"")
                amount.append(b[0])
            del amount[0]

            #Собираем инфу о каждом предмете
            market_hash_name_list = []
            tradable_list = []
            marketable_list = []
            for m in range(0,len(assetid)):
                item_info = descriptions_info.split(f"classid\":\"{classid[m]}\",\"instanceid\":\"{instanceid[m]}")
                item_info = item_info[1].split(f"appid\":{appid},\"classid")

                #Нахождение market_hash_name
                market_hash_name = item_info[0].split("market_hash_name\":\"")
                market_hash_name = market_hash_name[1].split("\"")
                market_hash_name_list.append(market_hash_name[0])
                #Нахождение значения tradable
                tradable = item_info[0].split("tradable\":")
                tradable = tradable[1].split(",")
                tradable_list.append(tradable[0])
                #Нахождение значения marketable
                marketable = item_info[0].split("marketable\":")
                marketable = marketable[1].split(",")
                marketable_list.append(marketable[0])
            
            #Добавление инфы в словарь
            game_info = []
            for m in range(0,len(assetid)):
                game_info.append(
                    {
                    "appid": f"{appid[n]}",
                    "contextid": f"{contextid[n]}",
                    "assetid": f"{assetid[m]}",
                    "classid": f"{classid[m]}",
                    "instanceid": f"{instanceid[m]}",
                    "amount": f"{amount[m]}",
                    "market hash name": f"{market_hash_name_list[m]}",
                    "tradable": f"{tradable_list[m]}",
                    "marketable": f"{marketable_list[m]}"                 
                    }
                )
            if n == 0:
                all_info[f"{k}"][f"{games[n]}"] = game_info
            else:
                if games[n] == games[n-1]:
                    all_info[f"{k}"][f"{games[n]}"].extend(game_info)
                else:
                    all_info[f"{k}"][f"{games[n]}"] = game_info

        if k != ErrList[-1]:
            del all_info[k]["games"]
            del all_info[k]["appid"]
            del all_info[k]["contextid"]

    #Запись ошибок в файл
    with open(f"JsonFiles/Errors.json", "w", encoding="utf-8") as file:
        json.dump(Err, file, indent=4, ensure_ascii=False)

    #Запись Err профилей в файл
    with open(f"JsonFiles/Err-Profiles.json", "w", encoding="utf-8") as file:
        json.dump(ErrList, file, indent=4, ensure_ascii=False)

    #Запись итогового файла
    with open(f"JsonFiles/Info-Items-{N}.json", "w", encoding="utf-8") as file:
        json.dump(all_info, file, indent=4, ensure_ascii=False)
    
#Порядковый номер
get_info("mix")