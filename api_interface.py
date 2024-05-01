import requests
import random
import json
import time

class api_interface:
    def __init__(self, port: int, auto_load_card_file: bool):
        self.port = port
        if auto_load_card_file:
            api_url = f"https://localhost:{self.port}/api/Magic/load_file/en_card_file"
            response = requests.get(api_url, verify=False, timeout=1000)
        self.delay = 0.10

    def make_get_request(self, api_url):
        """
        Makes a request to the specified API URL.

        Args:
            api_url (str): The URL of the API.

        Returns:
            requests.Response: The response object.
        """
        time.sleep(self.delay)
        response = requests.get(api_url, verify=True)
        return response
    
    def make_post_request(self, api_url):
        """
        Makes a request to the specified API URL.

        Args:
            api_url (str): The URL of the API.

        Returns:
            requests.Response: The response object.
        """
        time.sleep(self.delay)
        response = requests.post(api_url, verify=True)
        return response

    def get_all_card_names_scryfall(self) -> list:
        """
        Retrieves all card names from the Scryfall API.

        Returns:
            list: A list of card names.
        """
        api_url = "https://api.scryfall.com/catalog/card-names"
        response = self.make_get_request(api_url)
        all_names: dict = response.json()
        return all_names["data"]

    def get_all_creature_types_scryfall(self) -> list:
        """
        Retrieves all creature types from the Scryfall API.

        Returns:
            list: A list of creature types.
        """
        api_url = "https://api.scryfall.com/catalog/creature-types"
        response = self.make_get_request(api_url)
        creature_types: dict = response.json()
        return creature_types["data"]

    def get_all_land_types_scryfall(self) -> list:
        """
        Retrieves all land types from the Scryfall API.

        Returns:
            list: A list of land types.
        """
        api_url = "https://api.scryfall.com/catalog/land-types"
        response = self.make_get_request(api_url)
        land_types: dict = response.json()
        return land_types["data"]

    def get_all_artifact_types_scryfall(self) -> list:
        """
        Retrieves all artifact types from the Scryfall API.

        Returns:
            list: A list of artifact types.
        """
        api_url = "https://api.scryfall.com/catalog/artifact-types"
        response = self.make_get_request(api_url)
        artifact_types: dict = response.json()
        return artifact_types["data"]

    def get_all_enchantment_types_scryfall(self) -> list:
        """
        Retrieves all enchantment types from the Scryfall API.

        Returns:
            list: A list of enchantment types.
        """
        api_url = "https://api.scryfall.com/catalog/enchantment-types"
        response = self.make_get_request(api_url)
        enchantment_types: dict = response.json()
        return enchantment_types["data"]

    def get_all_spell_types_scryfall(self) -> list:
        """
        Retrieves all spell types from the Scryfall API.

        Returns:
            list: A list of spell types.
        """
        api_url = "https://api.scryfall.com/catalog/spell-types"
        response = self.make_get_request(api_url)
        spell_types: dict = response.json()
        return spell_types["data"]

    def get_all_powers_scryfall(self) -> list:
        """
        Retrieves all powers from the Scryfall API.

        Returns:
            list: A list of powers.
        """
        api_url = "https://api.scryfall.com/catalog/powers"
        response = self.make_get_request(api_url)
        powers: dict = response.json()
        return powers["data"]

    def get_all_toughnesses_scryfall(self) -> list:
        """
        Retrieves all toughnesses from the Scryfall API.

        Returns:
            list: A list of toughnesses.
        """
        api_url = "https://api.scryfall.com/catalog/toughnesses"
        response = self.make_get_request(api_url)
        toughnesses: dict = response.json()
        return toughnesses["data"]

    def get_all_keyword_abilities_scryfall(self) -> list:
        """
        Retrieves all keyword abilities from the Scryfall API.

        Returns:
            list: A list of keyword abilities.
        """
        api_url = "https://api.scryfall.com/catalog/keyword-abilities"
        response = self.make_get_request(api_url)
        keywords: dict = response.json()
        return keywords["data"]

    def get_all_keyword_actions_scryfall(self) -> list:
        """
        Retrieves all keyword actions from the Scryfall API.

        Returns:
            list: A list of keyword actions.
        """
        api_url = "https://api.scryfall.com/catalog/keyword-actions"
        response = self.make_get_request(api_url)
        keywords: dict = response.json()
        return keywords["data"]

    def get_all_keyword_words_scryfall(self) -> list:
        """
        Retrieves all keyword words from the Scryfall API.

        Returns:
            list: A list of keyword words.
        """
        api_url = "https://api.scryfall.com/catalog/keyword-words"
        response = self.make_get_request(api_url)
        keywords: dict = response.json()
        return keywords["data"]

    def get_all_supertypes_scryfall(self) -> list:
        """
        Retrieves all supertypes from the Scryfall API.

        Returns:
            list: A list of supertypes.
        """
        api_url = "https://api.scryfall.com/catalog/supertypes"
        response = self.make_get_request(api_url)
        supertypes: dict = response.json()
        return supertypes["data"]

    def get_word_bank_scryfall(self) -> list:
        """
        Retrieves the word bank from the Scryfall API.

        Returns:
            list: A list of words.
        """
        api_url = "https://api.scryfall.com/catalog/word-bank"
        response = self.make_get_request(api_url)
        word_bank: dict = response.json()
        return word_bank["data"]

    def get_symbology_scryfall(self) -> list:
        """
        Retrieves the symbology from the Scryfall API.

        Returns:
            list: A list of symbology.
        """
        api_url = "https://api.scryfall.com/symbology"
        response = self.make_get_request(api_url)
        symbology = response.json()
        return symbology["data"]

    def get_scryfall_interpretation_manacost(self, manacost: str) -> dict:
        """
        Retrieves the Scryfall interpretation of a mana cost.

        Args:
            manacost (str): The mana cost to interpret.

        Returns:
            dict: The interpretation of the mana cost.
        """
        api_url = f"https://api.scryfall.com/symbology/parse-mana?cost={manacost}"
        response = self.make_get_request(api_url)
        scryfall_response = response.json()
        return scryfall_response

    def get_all_unique_major_card_types_request(self):
        """
        Retrieves all unique major card types from the API.

        Returns:
            list: A list of all unique major card types.
        """
        api_url = f"http://localhost:{self.port}/api/Magic/all_unique_major_card_types"
        response = requests.get(api_url, verify=False)
        json = response.json()
        types = []
        for i in range(len(json)):
            types.append(json[i]["type"])
        return types
    
    def get_flavor_text(self):
        api_url = f"http://localhost:{self.port}/api/Magic/all_flavor_text"
        response = requests.get(api_url, verify=False)
        json_list = response.json()
        return json_list

    def get_all_oracle_text_api(self, separate_clause: bool, separate_cause_effect: bool):
        """
        Retrieves all oracle text from the API.

        Args:
            separate_clause (bool): Separates the clause from the effect.
            separate_cause_effect (bool): Separates the cause from the effect.

        Returns:
            list: A list of all oracle text.
        """
        api_url = "https://localhost:7000/api/Magic/stats"
        response = requests.get(api_url, verify=False)
        print(response.content)

        api_url = f"https://localhost:{self.port}/api/Magic/all_oracle_text/{separate_clause}/{separate_cause_effect}"
        print(api_url)
        with requests.Session() as s:
            response = s.get(api_url, verify=False, timeout=1500)
            response.raise_for_status()

        json_list = response.json()
        return json_list["separated"], json_list["causes"], json_list["effects"]
    
    def random_manacost_scryfall(self):
        """
        Retrieves a random mana cost from the Scryfall API.

        Returns:
            list: A list of symbols representing the mana cost.
        """
        api_url = "https://api.scryfall.com/symbology"
        response = requests.get(api_url)
        json = response.json()
        data = json["data"]
        symbols = []
        for i in range(len(data)):
            if data[i]["symbol"] is not None:
                symbols.append(data[i]["symbol"])
            else:
                print("API Error: No symbols found")
        return symbols

    def random_manacost_local(self, include_x: bool = False, verbose: bool = False) -> str:
        """
        Generates a random mana cost for a magic card.

        Args:
            include_x (bool, optional): Includes the option of X appearing in the mana cost. Defaults to False.
            verbose (bool, optional): Prints additional information during generation. Defaults to False.

        Returns:
            str: A string representing the mana cost.
        """
        main_mana_colors_dict = {"white": "W", "blue": "U", "black": "B", "red": "R", "green": "G"}
        main_mana_colors_list = ['W', 'U', 'B', 'R', 'G']  # White, Blue, Black, Red, Green

        # incomplete, doesn't have all definitions
        aux_mana_symbols = {"X_generic_mana": "X", "white_blue": "W/U", "black_red": "B/R", "white_black": "W/B",
                            "black_green": "B/G"}

        mana_cost = ""
        determine_multicolorness = random.randint(a=0, b=len(main_mana_colors_list))
        if verbose == True:
            print(f"number of colors that this card will be: {determine_multicolorness}")

        for i in range(0, determine_multicolorness):
            determine_color = random.randint(a=0, b=len(main_mana_colors_list))
            if verbose == True:
                print(f"random number generated: {determine_color}")
            color = main_mana_colors_list.pop(determine_color - 1)
            if verbose == True:
                print(f"next color of card will be: {color}, remaining options: {main_mana_colors_list}")
            mana_cost += "{" + color + "}"

        # max generic mana cost is 15, and is reduced in cost the more colored
        # mana it takes to cast the spell
        generic_cost_upper_limit: int = 15 - (2 * (5 - len(main_mana_colors_list)))
        determine_generic_cost = random.randint(a=0, b=generic_cost_upper_limit)
        if verbose == True:
            print(f"amount of generic mana that this card will cost to cast in addition to colored mana is: {determine_generic_cost}")
        if determine_generic_cost != 0:
            mana_cost += "{" + str(determine_generic_cost) + "}"

        return mana_cost

    def get_mana_symbol_key() -> dict:
        """
        Retrieves the key-value pairs of mana symbols.

        Returns:
            dict: A dictionary of mana symbols.
        """
        return {"white": "W", "blue": "U", "black": "B", "red": "R", "green": "G"}

    def get_mana_symbol_list() -> list:
        """
        Retrieves a list of mana symbols.

        Returns:
            list: A list of mana symbols.
        """
        return ['W', 'U', 'B', 'R', 'G']  # White, Blue, Black, Red, Green


#api = api_interface()
#names = api.get_all_card_names_scryfall()
#print(names[0])

#creature_types = api.get_all_creature_types_scryfall()
#print(creature_types[0])

#symbology = api.get_symbology_scryfall()
#print(symbology[0])
#print(symbology[0]["symbol"])
#print(type(symbology[0]["symbol"]))

#reponse = api.get_scryfall_interpretation_manacost("RUx")
#print(reponse)
