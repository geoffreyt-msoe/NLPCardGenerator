import json
import random
from name_generator import Name_Generator
from oracle_text_generator import Oracle_Text_Generator
from flavor_text_generator import Flavor_Text_Generator
from api_interface import API_Interface

name = False
oracle = False
flavor = False

class Card_Generator:

    def __init__(self):
        self.initialize_models()

    def initialize_models(self):
        print("Getting card data...")
        self.api = API_Interface()

        name_documents = self.api.get_all_card_names_scryfall()
        self.card_name_generator = Name_Generator(documents=name_documents, context_length=2, verbose=False)

        #TODO get cause data
        #self.oracle_text_generator_cause = Oracle_Text_Generator(documents=None, context_length=4, verbose=False)
        #TODO get effect data
        #self.oracle_text_generator_effect = Oracle_Text_Generator(documents=None, context_length=4, verbose=False)

        flavor_documents = open('data/flavor_text.json', encoding="utf8")
        flavor_documents = json.load(flavor_documents)
        self.flavor_text_generator = Flavor_Text_Generator(documents=flavor_documents, context_length=4, verbose=False)
        
        self.card_name_generator.load_model("models/name.h5")
        #TODO load other models
        #self.oracle_text_generator_cause.load_model(".h5")
        #self.oracle_text_generator_effect.load_model(".h5")
        self.flavor_text_generator.load_model("models/flavor.h5")

    def get_random_prediction_lengths(self):
        rand = random.Random()
        lengths = {}
        lengths["name_length"] = int(rand.random() * 4) + 1
        lengths["oracle_cause_length"] = int(rand.random() * 10) + 1
        lengths["oracle_effect_length"] = int(rand.random() * 10) + 1
        lengths["flavor_length"] = int(rand.random() * 15) + 1
        return lengths

    def generate_card(self):
        lengths = self.get_random_prediction_lengths()

        card_name = self.card_name_generator.predict(prompt="", num_predictions=lengths["name_length"], random_prompt=True, random_prompt_length=2)
        mana_cost = self.api.random_manacost_local()
        #TODO generate card type
        #TODO predict oracle text cause
        #TODO predict oracle text effect
        flavor_text = self.flavor_text_generator.predict(prompt="", num_predictions=lengths["flavor_length"], random_prompt=True, random_prompt_length=1, max_word_occurance=1)
        #TODO generate power/toughness


        print("Card name:", end=" ")
        for word in card_name:
            print(word, end=" ")
        print()

        print("Mana cost:", mana_cost)
        #TODO print card type
        #TODO print oracle text
        print("Flavor text:", end=" ")
        for word in flavor_text:
            print(word, end=" ")
        print()
        #TODO print power/toughness

def do_card_generation():
    card_generator = Card_Generator()
    print("Press enter to generate card. Enter q to quit.")
    user_input = input()
    while(user_input != "q" and user_input != "Q"):
        card_generator.generate_card()
        user_input = input()

do_card_generation()

if name:
    use_api = False

    if(use_api):
        print("Getting card data...")
        api = API_Interface()
        names = api.get_cards(-1)
        card_name_generator = Name_Generator(cards=names, context_length=2, verbose=False)

    else:
        print("Getting card data...")
        cards_json = open('./data/en_card_file.json')
        cards_dict = json.load(cards_json)
        card_name_generator = Name_Generator(cards=cards_dict, context_length=2, verbose=False)

    user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")
    while user_in != "load" and user_in != "train" and user_in != "q":
        print("Please try again.")
        user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")

    if user_in == "train":
        card_name_generator.train_model(validation_split=0.1, batch_size=2, epochs=10)

    elif user_in == "load":
        user_in = input("Enter the name of the model you would like to load.\nIt must be located within the 'models' folder: ")
        try:
            print("Loading model...")
            card_name_generator.load_model("./models/" + user_in)
            print("Done loading!")
        except:
            print("Could not find model.")
            user_in = "q"

    if user_in != "q":
        print("\nRegarding generating names:" +
            "\nYou will be asked for a prompt and the number of additional words to predict." + 
            "\nFor the user prompt, enter at least 2 words that are a part of the model's vocabulary." + 
            "\nTo view random parts of the model's vocabulary, enter 'v' at any time."
            "\nTo generate a random prompt, enter 'r' for the user prompt.")
        user_prompt = ""
        user_num_predictions = ""
        while(user_prompt != "q" and user_prompt != "Q" and user_num_predictions != "q" and user_num_predictions != "Q"):
            prompt_user_for_num_predictions = True
            predictions = []
            user_prompt = input("\n\nEnter prompt: ")
            if user_prompt == "q" or user_prompt == "Q":
                break
            elif user_prompt == "v":
                prompt_user_for_num_predictions = False
                print(card_name_generator.get_vocabulary(50))
            if prompt_user_for_num_predictions:
                user_num_predictions = input("Enter the number of words to predict: ")
                if user_num_predictions == "q" or user_num_predictions == "Q":
                    break
                elif user_num_predictions == "v":
                    prompt_user_for_num_predictions = False
                    print(card_name_generator.get_vocabulary(50))
                elif user_prompt == "r" or user_prompt == "R":
                    predictions = card_name_generator.predict(prompt="", num_predictions=int(user_num_predictions), random_prompt=True, random_prompt_length=2)
                else:
                    try:
                        predictions = card_name_generator.predict(prompt=user_prompt, num_predictions=int(user_num_predictions))
                    except:
                        prompt_user_for_num_predictions = False
                        print("Not enough words in model vocabulary. Try Again.")

                if prompt_user_for_num_predictions:
                    print("\nResult: ", end="")
                    for word in predictions:
                        print(word, end=" ")

    print("Exiting...")

if oracle:
    use_api = False

    if(use_api):
        print("Getting card data...")
        api = API_Interface()
        names = api.get_cards(-1)
        oracle_text_generator = Oracle_Text_Generator(cards=names, context_length=4, verbose=True)

    else:
        print("Getting card data...")
        cards_json = open('cards.json')
        cards_dict = json.load(cards_json)
        oracle_text_generator = Oracle_Text_Generator(cards=cards_dict, context_length=4, verbose=True)

    user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")
    while user_in != "load" and user_in != "train" and user_in != "q":
        print("Please try again.")
        user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")

    if user_in == "train":
        oracle_text_generator.train_model(validation_split=0.1, batch_size=4, epochs=10)

    elif user_in == "load":
        user_in = input("Enter the name of the model you would like to load.\nIt must be located within the 'models' folder: ")
        try:
            print("Loading model...")
            oracle_text_generator.load_model("./models/" + user_in)
            print("Done loading!")
        except:
            print("Could not find model.")
            user_in = "q"

    if user_in != "q":
        print("\nRegarding generating oracle text:" +
            "\nYou will be asked for a prompt and the number of additional words to predict." + 
            "\nFor the user prompt, enter at least 1 word that is a part of the model's vocabulary." + 
            "\nTo view random parts of the model's vocabulary, enter 'v' at any time."
            "\nTo generate a random prompt, enter 'r' for the user prompt.")
        user_prompt = ""
        user_num_predictions = ""
        while(user_prompt != "q" and user_prompt != "Q" and user_num_predictions != "q" and user_num_predictions != "Q"):
            prompt_user_for_num_predictions = True
            predictions = []
            user_prompt = input("\n\nEnter prompt: ")
            if user_prompt == "q" or user_prompt == "Q":
                break
            elif user_prompt == "v":
                prompt_user_for_num_predictions = False
                print(oracle_text_generator.get_vocabulary(50))
            if prompt_user_for_num_predictions:
                user_num_predictions = input("Enter the number of words to predict: ")
                if user_num_predictions == "q" or user_num_predictions == "Q":
                    break
                elif user_num_predictions == "v":
                    prompt_user_for_num_predictions = False
                    print(oracle_text_generator.get_vocabulary(50))
                elif user_prompt == "r" or user_prompt == "R":
                    predictions = oracle_text_generator.predict(prompt="", num_predictions=int(user_num_predictions), random_prompt=True, random_prompt_length=1)
                else:
                    try:
                        predictions = oracle_text_generator.predict(prompt=user_prompt, num_predictions=int(user_num_predictions))
                    except:
                        prompt_user_for_num_predictions = False
                        print("Not enough words in model vocabulary. Try Again.")

                if prompt_user_for_num_predictions:
                    print("\nResult: ", end="")
                    for word in predictions:
                        print(word, end=" ")

    print("Exiting...")

if flavor:
    use_api = False

    if(use_api):
        print("Getting card data...")
        api = API_Interface()
        names = api.get_cards(-1)
        flavor_text_generator = Flavor_Text_Generator(cards=names, context_length=4, verbose=True)

    else:
        print("Getting card data...")
        flavor_json = open('data/flavor_text.json', encoding="utf8")
        flavor_dict = json.load(flavor_json)
        flavor_text_generator = Flavor_Text_Generator(documents=flavor_dict, context_length=4, verbose=False)

    user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")
    while user_in != "load" and user_in != "train" and user_in != "q":
        print("Please try again.")
        user_in = input("\nWould you like to load a model, or train a model?\nEnter 'load' to load, 'train' to train, or 'q' to quit: ")

    if user_in == "train":
        flavor_text_generator.train_model(validation_split=0.1, batch_size=4, epochs=10)

    elif user_in == "load":
        user_in = input("Enter the name of the model you would like to load.\nIt must be located within the 'models' folder: ")
        try:
            print("Loading model...")
            flavor_text_generator.load_model("./models/" + user_in)
            print("Done loading!")
        except:
            print("Could not find model.")
            user_in = "q"

    if user_in != "q":
        print("\nRegarding generating flavor text:" +
            "\nYou will be asked for a prompt and the number of additional words to predict." + 
            "\nFor the user prompt, enter at least 1 word that is a part of the model's vocabulary." + 
            "\nTo view random parts of the model's vocabulary, enter 'v' at any time."
            "\nTo generate a random prompt, enter 'r' for the user prompt.")
        user_prompt = ""
        user_num_predictions = ""
        while(user_prompt != "q" and user_prompt != "Q" and user_num_predictions != "q" and user_num_predictions != "Q"):
            prompt_user_for_num_predictions = True
            predictions = []
            user_prompt = input("\n\nEnter prompt: ")
            if user_prompt == "q" or user_prompt == "Q":
                break
            elif user_prompt == "v":
                prompt_user_for_num_predictions = False
                print(flavor_text_generator.get_vocabulary(50))
            if prompt_user_for_num_predictions:
                user_num_predictions = input("Enter the number of words to predict: ")
                if user_num_predictions == "q" or user_num_predictions == "Q":
                    break
                elif user_num_predictions == "v":
                    prompt_user_for_num_predictions = False
                    print(flavor_text_generator.get_vocabulary(50))
                elif user_prompt == "r" or user_prompt == "R":
                    predictions = flavor_text_generator.predict(prompt="", num_predictions=int(user_num_predictions), random_prompt=True, random_prompt_length=1)
                else:
                    try:
                        predictions = flavor_text_generator.predict(prompt=user_prompt, num_predictions=int(user_num_predictions))
                    except:
                        prompt_user_for_num_predictions = False
                        print("Not enough words in model vocabulary. Try Again.")

                if prompt_user_for_num_predictions:
                    print("\nResult: ", end="")
                    for word in predictions:
                        print(word, end=" ")

    print("Exiting...")