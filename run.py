import json
from name_generator import Name_Generator
from oracle_text_generator import Oracle_Text_Generator
from api_interface import API_Interface

name = False
oracle = True
flavor = False

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