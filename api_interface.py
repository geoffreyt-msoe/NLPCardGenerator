import requests
import random
import json
import time

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
    
    def get_all_card_names_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/card-names"
        response = requests.get(api_url, verify=True)
        all_names: dict = response.json()
        return all_names["data"]
    
    def get_all_creature_types_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/creature-types"
        response = requests.get(api_url, verify=True)
        creature_types: dict = response.json()
        return creature_types["data"]
    
    def get_all_land_types_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/land-types"
        response = requests.get(api_url, verify=True)
        land_types: dict = response.json()
        return land_types["data"]
    
    def get_all_artifact_types_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/artifact-types"
        response = requests.get(api_url, verify=True)
        artifact_types: dict = response.json()
        return artifact_types["data"]
    
    def get_all_enchantment_types_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/enchantment-types"
        response = requests.get(api_url, verify=True)
        enchantment_types: dict = response.json()
        return enchantment_types["data"]
    
    def get_all_spell_types_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/spell-types"
        response = requests.get(api_url, verify=True)
        spell_types: dict = response.json()
        return spell_types["data"]
    
    def get_all_powers_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/powers"
        response = requests.get(api_url, verify=True)
        powers: dict = response.json()
        return powers["data"]
    
    def get_all_toughnesses_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/toughnesses"
        response = requests.get(api_url, verify=True)
        toughnesses: dict = response.json()
        return toughnesses["data"]
    
    def get_all_keyword_abilities_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/keyword-abilities"
        response = requests.get(api_url, verify=True)
        keywords: dict = response.json()
        return keywords["data"]
    
    def get_all_keyword_actions_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/keyword-actions"
        response = requests.get(api_url, verify=True)
        keywords: dict = response.json()
        return keywords["data"]
    
    def get_all_keyword_words_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/keyword-words"
        response = requests.get(api_url, verify=True)
        keywords: dict = response.json()
        return keywords["data"]
    
    def get_all_supertypes_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/supertypes"
        response = requests.get(api_url, verify=True)
        supertypes: dict = response.json()
        return supertypes["data"]
    
    def get_word_bank_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/catalog/word-bank"
        response = requests.get(api_url, verify=True)
        word_bank: dict = response.json()
        return word_bank["data"]
    
    def get_symbology_scryfall(self) -> list:
        api_url = "https://api.scryfall.com/symbology"
        response = requests.get(api_url, verify=True)
        symbology = response.json()
        print(type(symbology["data"]))
        return symbology["data"]
    
    def get_scryfall_interpretation_manacost(self, manacost: str) -> dict:
        """_summary_
            https://scryfall.com/docs/api/card-symbols/parse-mana
        Args:
            manacost (str): _description_

        Returns:
            dict: _description_
        """
        api_url = f"https://api.scryfall.com/symbology/parse-mana?cost={str}"
        response = requests.get(api_url, verify=True)
        scryfall_response = response.json()
        return scryfall_response
        
    
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
        
    def random_manacost_local(self, include_x: bool = False, verbose: bool = False) -> str:
        """generates a random mana cost for a magic card
        
        only will generate a mana cost with one of each mana at the moment
        
        maximum casting cost this method will produce is {15}, and starts to scale down as more colors of mana are added to the cost

        Args:
            include_x (bool, optional): includes the option of X appearing in the manacost, doesn't work right now. Defaults to False.

        Returns:
            str: a string that includes what a scryfall output would look like for a mtg cards mana cost. 
        """
        main_mana_colors_dict = {"white":"W", "blue":"U", "black":"B", "red":"R", "green":"G"}
        main_mana_colors_list = ['W', 'U', 'B', 'R', 'G']  # White, Blue, Black, Red, Green
        
        # incomplete, doesn't have all definitions
        aux_mana_symbols = {"X_generic_mana":"X", "white_blue":"W/U", "black_red": "B/R", "white_black":"W/B", "black_green":"B/G"}
        
        mana_cost = ""
        determine_multicolorness = random.randint(a=0, b=len(main_mana_colors_list))
        if verbose == True:
            print(f"number of colors that this card will be: {determine_multicolorness}")
        
        for i in range(0, determine_multicolorness):
            determine_color = random.randint(a=0, b=len(main_mana_colors_list))
            if verbose == True:
                print(f"random number generated: {determine_color}")
            #color = main_mana_colors_list[determine_color]
            color = main_mana_colors_list.pop(determine_color - 1)
            if verbose == True:
                print(f"next color of card will be: {color}, remaining options: {main_mana_colors_list}")
            mana_cost += "{"
            mana_cost += f"{color}"
            mana_cost += "}"
        
        # max generic mana cost is 15, and is reduced in cost the more colored 
        # mana it takes to cast the spell
        generic_cost_upper_limit: int = 15 - (2 * (5 - len(main_mana_colors_list)))
        determine_generic_cost = random.randint(a=0, b=generic_cost_upper_limit)
        if verbose == True:
            print(f"amount of generic mana that this card will cost to cast in addition to colored mana is: {determine_generic_cost}")
        if determine_generic_cost != 0:
            mana_cost += "{"
            mana_cost += f"{determine_generic_cost}"
            mana_cost += "}"
            
        return mana_cost
    
    def get_mana_symbol_key() -> dict:
        return {"white":"W", "blue":"U", "black":"B", "red":"R", "green":"G"}
    
    def get_mana_symbol_list() -> list:
        return ['W', 'U', 'B', 'R', 'G']  # White, Blue, Black, Red, Green

api = API_Interface()
names = api.get_all_card_names_scryfall()
print(names[0])

creature_types = api.get_all_creature_types_scryfall()
print(creature_types[0])

symbology = api.get_symbology_scryfall()
print(symbology[0])
print(symbology[0]["symbol"])
print(type(symbology[0]["symbol"]))

reponse = api.get_scryfall_interpretation_manacost("RUx")
print(reponse)
