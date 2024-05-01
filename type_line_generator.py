from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Embedding
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import SparseCategoricalCrossentropy
from keras.models import load_model
from keras.metrics import SparseCategoricalAccuracy, MeanSquaredError, RootMeanSquaredError, MeanAbsoluteError, CosineSimilarity
import numpy as np
import random


magic_number_for_context_length_and_batch_size = 4

class Type_Line_Generator:

    def __init__(self, documents, context_length, verbose=True):

        self.verbose = verbose

        print("Getting documents...")
        #documents = self.get_documents(texts)
        if(self.verbose and documents is not None):
            print("Documents:", documents)

        print("Getting sequences...")
        self.tokenizer = Tokenizer(num_words=None)
        
        sequences = self.get_sequences(documents, self.tokenizer)
        
        if(self.verbose):
            print("Sequences:", sequences)

        print("Getting vocabulary...")
        self.vocabulary = self.tokenizer.index_word
        if(self.verbose):
            print("Vocabulary:", self.vocabulary)

        print("Getting features and labels...")
        self.features, self.labels = self.get_features_and_labels(sequences, context_length)
        if(self.verbose):
            print("Features:", self.features)
            print("Labels:", self.labels)
        self.features = np.array(self.features)
        self.labels = np.array(self.labels)

        #self.encoded_labels = self.get_encoded_labels(self.features, self.labels, vocabulary)
        #print("One-Hot Encoded Labels:", self.encoded_labels)
        self.model = Sequential()
        self.model.add(
            Embedding(input_dim = len(self.vocabulary) + 1,
                      input_length = context_length,
                      output_dim = 100,
                      #weights=<insert_pre_trained_embeddings_here>,
                      trainable = True,
                      mask_zero = False)
        )
        self.model.add(
            LSTM(64, 
                 return_sequences = False,
                 #dropout = 0.1,
                 #recurrent_dropout = 0.1
                 dropout = 0.01,
                 recurrent_dropout = 0.01
                 )
        )
        self.model.add(
            Dense(64,
                  activation = 'relu')
        )
        self.model.add(
            #Dropout(0.5)
            Dropout(0.1)
        )
        self.model.add(
            Dense(len(self.vocabulary) + 1, 
                  activation = 'softmax')
        )
        self.model.compile(optimizer = 'adam',
                           loss = SparseCategoricalCrossentropy(),
                           metrics = [
                               'accuracy',
                               SparseCategoricalAccuracy(name="SCA"),
                               MeanSquaredError(name="MSE"),
                               RootMeanSquaredError(name="RMSE"),
                               MeanAbsoluteError(name="MAE"),
                               CosineSimilarity(name="CS")
                            ]
        )
        print("Done loading!")


    def train_model(self, validation_split=0.2, batch_size=magic_number_for_context_length_and_batch_size, epochs=1):
        callbacks = [EarlyStopping(monitor = 'val_loss',
                                   patience = 5),
                    ModelCheckpoint('./models/model.h5', 
                                    save_best_only = True, 
                                    save_weights_only = False)]
        self.history = self.model.fit(x = self.features,
                                 y = self.labels,
                                 batch_size = batch_size,
                                 epochs = epochs,
                                 callbacks = callbacks,
                                 validation_split = validation_split,
                                 shuffle = False)
        #self.display_metrics()
        print(self.model.summary())
        
        
        
    def predict(self, prompt, num_predictions, random_prompt=False, random_prompt_length=magic_number_for_context_length_and_batch_size):
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
            x.append([])
            for sequence in sequences:
                if len(sequence) != 0:
                    x[0].append(sequence[0])
            if(self.verbose):
                print("Prompt Sequence:", x)
            prediction = self.model.predict(x, batch_size=magic_number_for_context_length_and_batch_size)[0]
            probabilities = list(prediction)
            index = probabilities.index(max(probabilities))
            prediction = self.vocabulary[index]
            predictions.append(prediction)
            user_input.append(prediction)
        return(user_input)
    
    def display_metrics(self):
        print(self.history)


    def get_documents(self, cards):
        documents = []
        for card in cards:
            documents.append(card['oracle_text'])
        return documents


    def get_sequences(self, documents, tokenizer):
        tokenizer.fit_on_texts(documents)
        return tokenizer.texts_to_sequences(documents)
    

    def get_features_and_labels(self, sequences, context_length = magic_number_for_context_length_and_batch_size):
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

    def get_vocabulary(self, num_values):
        vocab = []
        keys = list(self.vocabulary.values())
        for i in range(num_values):
            vocab.append(keys[int(random.random() * len(keys))])
        return vocab