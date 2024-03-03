import requests
import pickle
import re
from bs4 import BeautifulSoup

session = requests.session()
with open("cookies", "rb") as f:
    session.cookies.update(pickle.load(f))


resp = session.get("http://moodle.hku.hk")
soup = BeautifulSoup(resp.content, "lxml")
print("Courses List:")
for link in soup.select("#inst476784 > div > div > ul > li > div > a"):
    print(f'- {link["title"]}')
