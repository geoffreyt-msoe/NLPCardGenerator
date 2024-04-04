import json
from name_generator import Name_Generator

cards_json = open('./cards.json')
cards_dict = json.load(cards_json)
card_name_generator = Name_Generator(cards=cards_dict, context_length=2)

card_name_generator.train_model(validation_split=0.2, batch_size=2, epochs=10)

#card_name_generator.load_model("./models/of_isnt_divine.h5")

user_prompt = ""
user_num_predictions = ""
while(user_prompt != "q" and user_prompt != "Q" and user_num_predictions != "q" and user_num_predictions != "Q"):
    predictions = []
    user_prompt = input("\n\n\nEnter prompt: ")
    if user_prompt == "q" or user_prompt == "Q":
        break
    user_num_predictions = input("Enter the number of words to predict: ")
    if user_num_predictions == "q" or user_num_predictions == "Q":
        break
    if user_prompt == "r" or user_prompt == "R":
        predictions = card_name_generator.predict(prompt="", num_predictions=int(user_num_predictions), random_prompt=True, random_prompt_length=2)
    else:
        predictions = card_name_generator.predict(prompt=user_prompt, num_predictions=int(user_num_predictions))

    print("\nResult: ", end="")
    for word in predictions:
        print(word, end=" ")

