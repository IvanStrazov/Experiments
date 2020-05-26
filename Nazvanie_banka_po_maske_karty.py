import requests

def from_card_to_bank(card_mask):
    api_url = 'https://lookup.binlist.net/{}'.format(card_mask)
    res = requests.get(api_url)
    if res.status_code==200:
        data = res.json()
        return data['bank']['name']



car_mask = 45717360
from_card_to_bank(car_mask)

>'Jyske Bank'