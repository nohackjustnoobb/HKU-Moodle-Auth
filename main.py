import requests
import re
import pickle
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_cookies(email, password):
    # Create the session
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:123.0) Gecko/20100101 Firefox/123.0"
        }
    )

    # Get the cookies
    resp = session.get("https://moodle.hku.hk/login/index.php?authCAS=CAS")
    resp.raise_for_status()

    # Redirect to hku portal login page
    resp = session.get("https://moodle.hku.hk/login/index.php?authCAS=CAS")
    resp.raise_for_status()

    # Redirect to microsoft login page
    resp = session.post(resp.url, data={"email": email})
    resp.raise_for_status()

    # Login with email and password
    resp = session.post(
        resp.url,
        data={
            "UserName": email,
            "Password": password,
            "AuthMethod": "FormsAuthentication",
        },
    )
    resp.raise_for_status()

    # Get the data for the next redirection
    soup = BeautifulSoup(resp.content, "lxml")
    url = soup.form["action"]
    data = {}
    for i in soup.find_all("input"):
        if i["type"] != "submit":
            data[i["name"]] = i["value"]
    resp = session.post(url, data=data)
    resp.raise_for_status()

    # Skip the "stay signed in" page
    config = json.loads(re.search("\$Config=({.*});", resp.text).group(1))
    url = urlparse(resp.url)._replace(path=config["urlPost"]).geturl()
    data = {
        "LoginOptions": 1,
        "type": 28,
        "DontShowAgain": True,
        config["sFTName"]: config["sFT"],
        "ctx": config["sCtx"],
        config["sCanaryTokenName"]: config["canary"],
        "hpgrequestid": config["sessionId"],
    }
    resp = session.post(url, data=data)
    resp.raise_for_status()

    # Skip the "stay signed in" page
    config = json.loads(re.search("\$Config=({.*});", resp.text).group(1))
    url = urlparse(resp.url)._replace(path=config["urlPost"]).geturl()
    data = {
        "LoginOptions": 1,
        "type": 28,
        "DontShowAgain": True,
        config["sFTName"]: config["sFT"],
        "ctx": config["sCtx"],
        config["sCanaryTokenName"]: config["canary"],
        "hpgrequestid": config["sessionId"],
    }
    resp = session.post(url, data=data)
    resp.raise_for_status()

    with open("cookies", "wb") as file:
        pickle.dump(session.cookies, file)


if __name__ == "__main__":
    # Get the email and password
    try:
        with open("config.json") as file:
            config = json.load(file)
            email = config["email"]
            password = config["password"]
            print("Config file detected.")
    except:
        print(
            "Config file not found or invalid. Please enter the information manually."
        )
        email = input("Email: ")
        password = input("Password: ")

    print("Getting the Cookies...")
    try:
        get_cookies(email, password)
        print("Successfully saved the cookies.")
    except:
        print("Failed to save the cookies.")
