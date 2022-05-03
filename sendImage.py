import requests


# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
    # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_aks():
    url = ""
    req = requests.get('https://axoltlapi.herokuapp.com/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
    # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url
# -----------------------------------------------------------------------


def get_duckURL():
    url = ""
    req = requests.get('https://random-d.uk/api/v2/random')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json["url"]
    return url
