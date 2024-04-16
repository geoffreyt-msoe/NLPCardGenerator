import requests

class API_Interface:

    def __init__(self):
        api_url = "http://localhost:5013/api/Magic/save_and_download_file/en_card_file"
        self.response = requests.get(api_url, verify=False)
    
    def get_cards(self, num_cards):
        json = self.response.json()
        if num_cards > len(json) or num_cards == -1:
            num_cards = len(json)
        cards = []
        for i in range(num_cards):
            cards.append(json[i])
        return cards
    
    def get_names(self, num_names):
        json = self.response.json()
        if num_names > len(json) or num_names == -1:
            num_names = len(json)
        names = []
        for i in range(num_names):
            names.append(json[i]["name"])
        return names


#api = API_Interface()
#print(api.get_names(50))