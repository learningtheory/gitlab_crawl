import requests
from requests.cookies import cookiejar_from_dict

cookie_dict = {
    '_gitlab_session': 'af89df85d245dbe3b32bbb1785a5a374',
}

session = requests.Session()
session.cookies = cookiejar_from_dict(cookie_dict=cookie_dict, overwrite=True)
