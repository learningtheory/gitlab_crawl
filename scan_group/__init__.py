import requests
from requests.cookies import cookiejar_from_dict

cookie_dict = {
    '_gitlab_session': '',
}

session = requests.Session()
session.cookies = cookiejar_from_dict(cookie_dict=cookie_dict, overwrite=True)
