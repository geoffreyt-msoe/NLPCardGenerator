from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import split_dataset
from keras.losses import SparseCategoricalCrossentropy
from keras.models import load_model
import numpy as np
import random

class Name_Generator:
    
    def __init__(self, cards, context_length):

        documents = self.get_documents(cards)
        print("Documents:", documents)

        self.tokenizer = Tokenizer(num_words=None)
        sequences = self.get_sequences(documents, self.tokenizer)
        print("Sequences:", sequences)

        self.vocabulary = self.tokenizer.index_word
        print("Vocabulary:", self.vocabulary)

        self.features, self.labels = self.get_features_and_labels(sequences, context_length)
        print("Features:", self.features)
        print("Labels:", self.labels)
        self.features = np.array(self.features)
        self.labels = np.array(self.labels)

        #self.encoded_labels = self.get_encoded_labels(self.features, self.labels, vocabulary)
        #print("One-Hot Encoded Labels:", self.encoded_labels)
        
        self.model = Sequential()
        self.model.add(
            Embedding(input_dim = len(self.vocabulary),# + 1,
                      input_length = context_length,
                      output_dim = 100,
                      #weights=<insert_pre_trained_embeddings_here>,
                      trainable = True,
                      mask_zero = False)
        )
        #self.model.add(
        #    Masking(mask_value = 0.0)
        #)
        self.model.add(
            LSTM(64, 
                 return_sequences = False,
                 dropout = 0.1,
                 recurrent_dropout = 0.1
                 )
        )
        self.model.add(
            Dense(64,
                  activation = 'relu')
        )
        self.model.add(
            Dropout(0.5)
        )
        self.model.add(
            Dense(len(self.vocabulary) + 1, 
                  activation = 'softmax')
        )
        self.model.compile(optimizer = 'adam',
                      #loss = 'categorical_crossentropy',
                           loss = SparseCategoricalCrossentropy(),
                      metrics = ['accuracy']
        )


    def train_model(self, validation_split=0.2, batch_size=2, epochs=1):
        callbacks = [EarlyStopping(monitor = 'val_loss',
                                   patience = 5),
                    ModelCheckpoint('./models/model.h5', 
                                    save_best_only = True, 
                                    save_weights_only = False)]
        history = self.model.fit(x = self.features,
                                 y = self.labels,
                                 batch_size = batch_size,
                                 epochs = epochs,
                                 callbacks = callbacks,
                                 validation_split = validation_split,
                                 shuffle = False)
        
    def predict(self, prompt, num_predictions, random_prompt=False, random_prompt_length=2):
        user_input = []
        predictions = []
        if(random_prompt):
            vocab_vals = list(self.vocabulary.values())
            for i in range(random_prompt_length):
                user_input.append(vocab_vals[int(random.random() * len(vocab_vals))])
        else:
            user_input = prompt.split(" ")
        for i in range(num_predictions):
            sequences = self.tokenizer.texts_to_sequences(user_input)
            x = []
            token_index = -1
            batch_index = -1
            for sequence in sequences:
                if len(sequence) != 0:
                    if token_index % 2 == 1 or batch_index == -1:
                        x.append([])
                        batch_index += 1
                    x[batch_index].append(sequence[0])
                    token_index += 1
            if len(x[batch_index]) < 2:
                for i in range(batch_index, 0, -1):
                    x[i].insert(0, x[i-1][1])
                    x[i-1].pop(0)
                x.pop(0)
            print("Prompt Sequence:", x)
            probabilities = list(self.model.predict(x, batch_size=2)[0])
            index = probabilities.index(max(probabilities))
            prediction = self.vocabulary[index]
            predictions.append(prediction)
            user_input.append(prediction)
        return(user_input)


    def get_documents(self, cards):
        documents = []
        for card in cards:
            documents.append(card['name'])
        return documents


    def get_sequences(self, documents, tokenizer):
        tokenizer.fit_on_texts(documents)
        return tokenizer.texts_to_sequences(documents)
    

    def get_features_and_labels(self, sequences, context_length = 2):
        features = []
        labels = []
        for sequence in sequences:
            for i in range(context_length, len(sequence)):
                extraction = sequence[i - context_length:i + 1]
                features.append(extraction[:-1])
                labels.append(extraction[-1])
        return (features, labels)
    

    def get_encoded_labels(self, features, labels, vocabulary):
        encoded_labels = np.zeros((len(features), len(vocabulary)), dtype=np.int8)
        for example_index, word_index in enumerate(labels):
            encoded_labels[example_index, word_index] = 1
        return encoded_labels
    
    def load_model(self, filename):
        self.model = load_model(filename)