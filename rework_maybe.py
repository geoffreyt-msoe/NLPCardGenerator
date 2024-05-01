from api_interface import api_interface as api_interface
import oracle_text_generator as Oracle_Text_Generator
import flavor_text_generator as Flavor_Text_Generator
import name_generator as Name_Generator
import json

class Card_Generator:

    def __init__(self):
        self.initialize_models()

    def initialize_models(self):
        print("Getting card data...")
        self.api = api_interface(port=7000, auto_load_card_file=True)

        name_documents = self.api.get_all_card_names_scryfall()
        self.card_name_generator = Name_Generator(documents=name_documents, context_length=2, verbose=False)

        #TODO get cause data
        oracle_text = None
        try: 
            oracle_text = self.api.get_all_oracle_text_api(True, False)
        except:
            oracle_text = open('data/oracle_text.json', encoding="utf8")
            oracle_text = json.load(oracle_text)

        self.oracle_text_generator_cause = Oracle_Text_Generator(documents=oracle_text, context_length=4, verbose=False)
        #TODO get effect data
        #self.oracle_text_generator_effect = Oracle_Text_Generator(documents=None, context_length=4, verbose=False)

        flavor_documents = open('data/flavor_text.json', encoding="utf8")
        flavor_documents = json.load(flavor_documents)
        self.flavor_text_generator = Flavor_Text_Generator(documents=flavor_documents, context_length=4, verbose=False)

        self.card_name_generator.load_model("models/name.h5")
        #TODO load other models
        self.oracle_text_generator_cause.load_model(".h5")
        self.oracle_text_generator_effect.load_model(".h5")
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

class runner(object):
    def __init__(self, 
                 generate_name=True, 
                 generate_oracle_text=True, 
                 generate_flavor_text=True,
                 use_cause_effect_oracle_text=True,
                 use_api=True, 
                 verbose=True):
        self.use_api = use_api
        self.use_cause_effect_oracle_text = use_cause_effect_oracle_text
        self.generate_name = generate_name
        self.generate_oracle_text = generate_oracle_text
        self.generate_flavor_text = generate_flavor_text
        self.verbose=verbose
        
    def main(self):
        pass
    
    def get_card_data(self):
        if(self.use_api and self.generate_oracle_text):
            print("Getting card data...")
            api = api_interface(port=7000, auto_load_card_file=True)
            separated, cause, effect = api.get_all_oracle_text_api(True, False) # separates text into clauses, separate clauses into just cause and effect statements
            
            if cause is not None and effect is not None and self.use_cause_effect_oracle_text == True:
                self.cause_oracle_text_generator = Oracle_Text_Generator(documents=cause, context_length=4, verbose=True)
                self.effect_oracle_text_generator = Oracle_Text_Generator(documents=effect, context_length=4, verbose=True)
            else:
                print("Could not get cause and effect oracle text.")
                self.cause_oracle_text_generator = None
                self.effect_oracle_text_generator = None
                self.oracle_text_generator = Oracle_Text_Generator(documents=separated, context_length=4, verbose=True)
        else:
            print("Getting card data...")
            cards_json = open('oracle_text.json')
            cards_dict = json.load(cards_json)
            self.oracle_text_generator = Oracle_Text_Generator(documents=cards_dict, context_length=4, verbose=True)

    def train(self):
        if self.generate_oracle_text:
            if self.cause_oracle_text_generator is not None and 
                self.effect_oracle_text_generator is not None and 
                self.use_full_oracle_text == False:
                self.cause_oracle_text_generator.train_model(validation_split=0.1, batch_size=4, epochs=10)
                self.effect_oracle_text_generator.train_model(validation_split=0.1, batch_size=4, epochs=10)
            else:
                self.oracle_text_generator.train_model(validation_split=0.1, batch_size=4, epochs=10)
                
    def load_models(self, user_in):
        if self.generate_oracle_text:
            try:
                if self.verbose:
                    print("Loading model...")
                
                self.oracle_text_generator.load_model("./models/" + user_in)
                
                if self.verbose:
                    print("Done loading!")
            except:
                if self.verbose:
                    print("Could not find model.")
                user_in = "q"
    
    def generate_text(self):
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
                print(self.oracle_text_generator.get_vocabulary(50))
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



