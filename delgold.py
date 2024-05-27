import requests
import asyncio
import random
import os
import base64
import datetime

ACCESS_TOKEN = ""
if not ACCESS_TOKEN:
    ACCESS_TOKEN = input("Paste access token here: ")
    if not ACCESS_TOKEN:
        print("No access token provided, exiting...")
        exit()
HEADER = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "authorization": f"Bearer {ACCESS_TOKEN}",
    "content-type": "application/x-www-form-urlencoded",
    # ... (other headers - update if needed)
}
API_URL = "https://api.quackquack.games/"
API = {
    "getBalance": API_URL + "balance/get",
    "getEggs": API_URL + "nest/list-reload",
    "collectEgg": API_URL + "nest/collect",
    "layEgg": API_URL + "nest/lay-egg",
    # Removed golden duck related endpoints
    "ufoCollect": API_URL + "egg/harvester-collect",
}
ducks = []
eggs = []

def getTime(addSeconds:int = 0):
    """Tính thời gian hiện tại cộng thêm số giây nếu có."""
    now = datetime.datetime.now()
    exam_time = now + datetime.timedelta(seconds=addSeconds)
    return exam_time.strftime("%H:%M:%S")  # Định dạng theo mong muốn

async def APIRequest(url, isPOST=False, data=None):
    response = None
    method = requests.post if isPOST else requests.get
    while response is None:
        try:
            response = await asyncio.to_thread(method, url, headers=HEADER, data=data)
        except:
            await asyncio.sleep(5)
            print("Connection error, retrying...")
            continue

    return response

async def getBalances():
    response = await APIRequest(API["getBalance"])
    data = response.json()
    balances = [[i.get("symbol"), f"{float(i.get('balance')):.2f}"] for i in data.get("data").get("data")]
    os.system("clear||cls")
    maxLen = sum([len(item) for sublist in balances for item in sublist]) + len(balances) + 20
    LenPerItem = int(maxLen / len(balances)) - 1
    printer = [
        "╔" + "Balance".center(maxLen, '=') + "╗",
        "║" + " " * maxLen + "║",
        "║" + "║".join([token[0].center(LenPerItem, '_') for token in balances]) + "_║",
        "║" + "║".join([token[1].center(LenPerItem, '_') for token in balances]) + "_║",
        "║" + " " * maxLen + "║",
        "╚" + "═" * maxLen + "╝",
        base64.b64decode("RGV2IGJ5IDogQmxhY2tmb3hpdjk5").decode(),
        "Last Update: " + datetime.datetime.now().strftime("%H:%M:%S")
    ]
    for line in printer:
        print(line)

async def collectEgg():
    global eggs, ducks
    while len(eggs) > 0:
        egg = random.choice(eggs)
        response = await APIRequest(API["collectEgg"], True, {'nest_id': egg})
        if response.status_code == 200:
            eggs.remove(egg)
            print("Collected:", egg)
        else:
            print(f"Failed to collect egg {egg}. Status code: {response.status_code}")
    await getBalances()

async def get_list_reload():
    global eggs, ducks  # Indicate you're modifying global variables
    response = await APIRequest(API["getEggs"])
    data = response.json()
    if not ducks:
        ducks = [item["id"] for item in data["data"]["duck"]]
    eggs = [item["id"] for item in data["data"]["nest"] if item["type_egg"]]
    if len(eggs) > 0:
        print("Eggs available:", len(eggs))
        await collectEgg()

async def main():
    while True:
        await getBalances()
        await asyncio.sleep(10)  # Update list every 10 seconds
        await get_list_reload()

asyncio.run(main())
