import os, asyncio, requests, time, random

from bs4 import BeautifulSoup
from pyrogram import Client


def clear():
	if os.name == "posix":
		a = os.system("clear")
	elif os.name == "nt":
		a = os.system("cls")
	else:
		pass
     
clear()

def request_tg_code_get_random_hash(input_phone_number):
    """ requests Login Code
    and returns a random_hash
    which is used in STEP TWO """

    request_url = "https://my.telegram.org/auth/send_password"
    request_data = {"phone": input_phone_number}
    
    response_c = requests.post(request_url, data=request_data)
    json_response = response_c.json()

    return json_response["random_hash"]


def login_step_get_stel_cookie(input_phone_number,tg_random_hash,tg_cloud_password):
    """Logins to my.telegram.org and returns the cookie,
    or False in case of failure"""

    request_url = "https://my.telegram.org/auth/login"
    request_data = {"phone": input_phone_number,"random_hash": tg_random_hash,"password": tg_cloud_password}
    response_c = requests.post(request_url, data=request_data)

    re_val = None
    re_status_id = None
    
    if response_c.text == "true":
        re_val = response_c.headers.get("Set-Cookie")
        re_status_id = True
    else:
        re_val = response_c.text
        re_status_id = False

    return re_status_id, re_val


def scarp_tg_existing_app(stel_token):
    """scraps the web page using the provided cookie,
    returns True or False appropriately"""

    request_url = "https://my.telegram.org/apps"
    custom_header = {"Cookie": stel_token}
    response_c = requests.get(request_url, headers=custom_header)
    response_text = response_c.text

    soup = BeautifulSoup(response_text, features="html.parser")
    title_of_page = soup.title.string

    re_dict_vals = {}
    re_status_id = None

    if "configuration" in title_of_page:
        g_inputs = soup.find_all("span", {"class": "input-xlarge"})

        app_id = g_inputs[0].string

        api_hash = g_inputs[1].string

        test_configuration = g_inputs[4].string

        production_configuration = g_inputs[5].string

        _a = "It is forbidden to pass this value to third parties."

        hi_inputs = soup.find_all("p", {"class": "help-block"})

        test_dc = hi_inputs[-2].text.strip()

        production_dc = hi_inputs[-1].text.strip()

        re_dict_vals = {"App Configuration": {"app_id": app_id,"api_hash": api_hash},"Available MTProto Servers": {"test_configuration": {"IP": test_configuration,"DC": test_dc},"production_configuration": {"IP": production_configuration,"DC": production_dc}},"Disclaimer": _a}

        re_status_id = True
    else:
        tg_app_hash = soup.find("input", {"name": "hash"}).get("value")
        re_dict_vals = {"tg_app_hash": tg_app_hash}
        re_status_id = False

    return re_status_id, re_dict_vals


def create_new_tg_app(stel_token,tg_app_hash,app_title,app_shortname,app_url,app_platform,app_desc):
    # pylint: disable-msg=too-many-arguments

    """ creates a new my.telegram.org/apps
    using the provided parameters """

    request_url = "https://my.telegram.org/apps/create"
    custom_header = {"Cookie": stel_token}
    request_data = {"hash": tg_app_hash,"app_title": app_title,"app_shortname": app_shortname,"app_url": app_url,"app_platform": app_platform,"app_desc": app_desc}

    response_c = requests.post(request_url,data=request_data,headers=custom_header)
    print(str(response_c.text))

    return response_c


def start():
    print("""

 _  _  _       _                        

| || || |     | |                       

| || || | ____| | ____ ___  ____   ____ 

| ||_|| |/ _  ) |/ ___) _ \|    \ / _  )

| |___| ( (/ /| ( (__| |_| | | | ( (/ / 

\______|\____)_|\____)___/|_|_|_|\____)                                  

""")

    input("Press ENTER to continue...")


async def fill_api():
    clear()

    while True:
        input_phone_number = input("Send your phone number : ").replace(" ","")
        random_hash = request_tg_code_get_random_hash(input_phone_number)
        if random_hash:

            provided_code = input("Send the code you recived : ")
            # name = input("Send your app name :")

            status_r, cookie_v = login_step_get_stel_cookie(input_phone_number, random_hash, provided_code)

            if status_r:

                status_t, response_dv = scarp_tg_existing_app(cookie_v)

                if not status_t:
                    print(response_dv.get("tg_app_hash"))
                    create_new_tg_app(
                        cookie_v,
                        response_dv.get("tg_app_hash"),
                        f"TestApp1",
                        f"testapp{random.randint(3,99999)}",
                        "",
                        "desktop",
                        ""
                    )

                status_t, response_dv = scarp_tg_existing_app(cookie_v)
                if status_t:

                    user_api_id = response_dv["App Configuration"]["app_id"]

                    user_api_hash = response_dv["App Configuration"]["api_hash"]

                    session_name = f"{input_phone_number.replace('+','')}-{time.time()}"

                    ses = session_name.replace("+","") + ".session"

                    sestxt = session_name.replace("+","") + ".txt"

                    userClient = Client(session_name,user_api_id,user_api_hash,phone_number=input_phone_number)

                    await userClient.start()

                    session = await userClient.export_session_string()

                    print(f"\nPhone Number : {input_phone_number}\nAPI ID : {user_api_id}\nAPI HASH : {user_api_hash}\nSESSION STRING : {session}\n\nSession string will be saved as {sestxt}, Also you can copy {ses} to session dir.\nNever share this to anyone!")

                    open(sestxt, "w").write(str(session))

                    break
                else:
                    print("creating APP ID caused error %s", response_dv)
        else:
            print("Cannot send code to this number!")

start()

asyncio.get_event_loop().run_until_complete(fill_api())
