#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#

import os
from test_utils import fixture_path


def load_data(path):
    # Load input file
    input_file = os.path.join(fixture_path("nmt"), path)
    with open(input_file, "r") as f:
        data = f.read()

    return data.split("\n")


from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import GRU, Dense, TimeDistributed, Dropout
from keras.models import load_model


import numpy as np


# Build the RNN layers
def simple_model(input_shape, french_vocab_size):
    """
    Build and train a basic RNN on x and y
    :param input_shape: Tuple of input shape
    :param output_sequence_length: Length of output sequence
    :param english_vocab_size: Number of unique English words in the dataset
    :param french_vocab_size: Number of unique French words in the dataset
    :return: Keras model built, but not trained
    """
    model = Sequential()
    model.add(GRU(128, input_shape=input_shape[1:], return_sequences=True))
    model.add(Dropout(0.5))
    model.add(GRU(128, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(256, activation="relu")))
    model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(french_vocab_size + 1, activation="softmax")))

    model.compile(
        loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    return model


# Load English data
english_sentences = load_data("small_vocab_en")
# Load French data
french_sentences = load_data("small_vocab_fr")

french_tokenizer = Tokenizer()
english_tokenizer = Tokenizer()

# --------------------------------------------
# INPUT PROCESSING
# x: list of strings (English sentences)
# y: list of strings (French translations)
# --------------------------------------------


# STEP 1: Preprocessing Steps
#    1a: Call function to tokenize and pad (define later in Step 2)
#    1b: pad English data to have same sentence length as French
#    1c: Adjust the dimensions to fit the Keras loss function
def preprocess(x, x_tokenizer, y, y_tokenizer):
    """
    Preprocess the sentences in x and y
    :param x: list of sentence strings
    :param x_tokenzier: tokenizer for x
    :param y: list of sentence strings
    :param: y_tokenizer: tokenizer for y
    :return: Tuple of (Preprocessed x, Preprocessed y)
    """
    # 1a: Tokenize and Pad x any y (Go to definition in Step 2)
    raw_x = tokenize_and_pad(x_tokenizer, x)
    raw_y = tokenize_and_pad(y_tokenizer, y)

    # 1b: pad English data to have same sentence length as French
    print("X Raw Shape: %s" % (raw_x.shape,))
    print("Y Raw Shape: %s" % (raw_y.shape,))
    raw_x = pad_sequences(raw_x, padding="post", maxlen=raw_y.shape[1])

    # 1c: Adjust the dimensions to fit the Keras loss function
    return raw_x.reshape(*raw_x.shape, 1), raw_y.reshape(*raw_y.shape, 1)


# Step 2: Tokenize and Pad Function
#   2a: Initialize tokenizer
#   2b: Convert sentences to lists of integer word identifiers
#   2c: Pad sequences: convert data to 2D ndarray (sentence number, word number)
#         by adding 0s to fill in blanks
def tokenize_and_pad(tokenizer, x):
    """
    Tokenize and pad x
    :param tokenizer: Tokenizer object from Keras
    :param x: list of sentences/strings to be tokenized and padded
    :return: tokenized and padded x data with pads added to end
    """
    # 2a: Initialize tokenizer with input texts
    tokenizer.fit_on_texts(x)

    # 2b: Convert to integers
    # 2c: Pad sequences
    return pad_sequences(tokenizer.texts_to_sequences(x), padding="post")


# --------------------------------------------
# OUTPUT PROCESSING
# Once we remove the extra dimension needed by the loss function,
# the output shape is (word number in sentence, French vocabulary items)
# --------------------------------------------


# Step 3: Convert a single output from the NN into a sentence
#   3a: Create lookup table for words from indices (define later)
#   3b: Convert output into words
def output_to_text(output_logits, tokenizer):
    """
    Turn output from neural network into text using the tokenizer
    :param output: output from the neural network with the extra dimension removed
    :param tokenizer: Keras Tokenizer for the output language
    :return: String that represents the text of the output
    """
    # 3a:Create lookup table for words (Go to Function Definition below)
    # Returns: {int index : str 'word' }
    index_to_words = create_word_lookup_dict(tokenizer.word_index)

    # 3b: Convert output to words
    return " ".join(
        [index_to_words[prediction] for prediction in np.argmax(output_logits, 1)]
    )


# Step 3a: Create lookup table for words from indices (define later)
def create_word_lookup_dict(word_index):
    """
    :param word_index: Tokenizer dictionary mapping words to integer identifiers {'str' : int}
    :return dictionary mapping integer to words or '<PAD>' {int : 'str'}
    """
    index_to_words = {id: word for word, id in word_index.items()}
    index_to_words[0] = ""
    return index_to_words


# VALIDATION:
preproc_english_sentences, preproc_french_sentences = preprocess(
    english_sentences, english_tokenizer, french_sentences, french_tokenizer
)
# VERIFY: Look at types and shapes of the preprocessed Data
print("English")
print(" * preproc_english_sentences_type", str(type(preproc_english_sentences)))
print(" * preproc_english_sentences_shape", str(preproc_english_sentences.shape))
print("French")
print(" * preproc_french_sentences_type", str(type(preproc_french_sentences)))
print(" * preproc_french_sentences_shape", str(preproc_french_sentences.shape))
# load the pre-trainined network
french_vocab_size = len(french_tokenizer.word_index)
model = load_model(os.path.join(fixture_path("nmt"), "translation.tf"))
# TEST: This translates a single sentence from English to French
pred = model.predict(
    preproc_english_sentences[:1], verbose=0
)  # Predict the French sentence from NN
# OUTPUT SHAPE: (extra dimension of size 1, word number in sentence, French vocabulary items)
pred = pred[0]  # Remove Keras-required 3rd dimension
translation = output_to_text(
    pred, french_tokenizer
)  # To human readable French sentence
print("Test Case - English to French")
print(" * English sentence:", english_sentences[0])
print(" * Actual translation:", french_sentences[0])
print(" * Predicted translation:", translation)

result = "nmt complete"
