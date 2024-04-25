import requests
import random

class API_Interface:

    #def __init__(self):
        #api_url = "http://localhost:5013/api/Magic/save_and_download_file/en_card_file"
        #self.response = requests.get(api_url, verify=False)
    
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
    
    def get_all_card_names_request(self):
        api_url = "http://localhost:5013/api/Magic/all_card_names"
        response = requests.get(api_url, verify=False)
        json = response.json()
        names = []
        for i in range(len(json)):
            names.append(json[i]["name"])
        return names
    
    def get_all_unique_major_card_types_request(self):
        api_url = "http://localhost:5013/api/Magic/all_unique_major_card_types"
        response = requests.get(api_url, verify=False)
        json = response.json()
        types = []
        for i in range(len(json)):
            types.append(json[i]["type"])
        return types
    
    def get_oracle_text(self, params: list = None):
        api_url = ""
        if params is None:
            api_url = "http://localhost:5013/api/Magic/all_card_names"
        else:
            string: str = "" 
            string = ','.join(self=string, iterable=params)
            api_url = f"http://localhost:5013/api/Magic/all_card_names/{string}"
            
        pass
    
    def random_manacost_scryfall(self):
        api_url = "https://api.scryfall.com/symbology"
        response = requests.get(api_url)
        json = response.json()
        data = json["data"]
        print(data)
        print("-----------------------------------------------------")
        print(data[1])
        print("-----------------------------------------------------")
        print(data[0]["symbol"])
        for i in range(len(data)):
            if json[i]["symbol"] is not None:
                symbols = json[i]["symbol"]
            else:
                print("API Error: No symbols found")
        symbols = json["data"]
        return symbols
        
    def random_manacost_local(self, include_x: bool = False) -> str:
        main_mana_colors_dict = {"white":"W", "blue":"U", "black":"B", "red":"R", "green":"G"}
        main_mana_colors_list = ['W', 'U', 'B', 'R', 'G']  # White, Blue, Black, Red, Green
        
        # incomplete, doesn't have all definitions
        aux_mana_symbols = {"X_generic_mana":"X", "white_blue":"W/U", "black_red": "B/R", "white_black":"W/B", "black_green":"B/G"}
        
        mana_cost = ""
        determine_multicolorness = random.randint(a=0, b=len(main_mana_colors_list))
        print(f"number of colors that this card will be: {determine_multicolorness}")
        
        for i in range(0, determine_multicolorness):
            determine_color = random.randint(a=0, b=len(main_mana_colors_list))
            print(f"random number generated: {determine_color}")
            #color = main_mana_colors_list[determine_color]
            color = main_mana_colors_list.pop(determine_color - 1)
            print(f"next color of card will be: {color}, remaining options: {main_mana_colors_list}")
            mana_cost += "{"
            mana_cost += f"{color}"
            mana_cost += "}"
        
        # max generic mana cost is 15, and is reduced in cost the more colored 
        # mana it takes to cast the spell
        generic_cost_upper_limit: int = 15 - (2 * (5 - len(main_mana_colors_list)))
        determine_generic_cost = random.randint(a=0, b=generic_cost_upper_limit)
        print(f"amount of generic mana that this card will cost to cast in addition to colored mana is: {determine_generic_cost}")
        if determine_generic_cost != 0:
            mana_cost += "{"
            mana_cost += f"{determine_generic_cost}"
            mana_cost += "}"
            
        return mana_cost


api = API_Interface()
print(api.random_manacost_local())