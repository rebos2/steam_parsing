import requests

url = 'https://steamcommunity.com/market/priceoverview/?'
params = {'market_hash_name':'★ Classic Knife | Stained (Minimal Wear)',
'appid':'730',
'currency':'5',
}

r = requests.get(url, params = params)

print(r.json())



"""
#Собираем инфу о ценах
t = 0
price_list = []
for m in range(0,len(classid)):
    print(f"Проверка {m+1}-го предмета")
    req_price = requests.get(f"https://steamcommunity.com/market/priceoverview/?country=RU&currency=5&appid={appid[n]}&market_hash_name={market_hash_name_list[m]}")

    price = req_price.text.split("price\":\"")
    price = price[-1].split(" ")
    price_list.append(price[0])
    t = t + 1
    if t == 20:
        time.sleep(60)
        t = 0 
print(price_list)
"""