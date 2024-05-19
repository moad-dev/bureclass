import requests

def request_to_api(name):
    r = requests.get('https://danil.moad.dev/api/search', params={'object_name': name, 'limit': 1})
    return r.json()[0]['object_name']

print(request_to_api('анкер забивной м10'))
