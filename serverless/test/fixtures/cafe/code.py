import pandas as pd
import nltk, json
from test_utils import fixture_path
import os

nltk.download("wordnet", quiet=True)
nltk.download("stopwords", quiet=True)

REVIEW = "review"

# use smaller set
with open(os.path.join(fixture_path("cafe"), "reviews.json")) as IN:
    data = pd.DataFrame(json.load(IN))

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    data[REVIEW], data["rating"], stratify=data["rating"], random_state=21
)


from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import CountVectorizer


# Preprocess First
def preprocess(docs):
    # Apply some function to each document/review in the pandas series
    # NOTE: Every x document is a sentence, with multiple words
    return docs.apply(lambda x: x)


x_train = preprocess(x_train)
x_test = preprocess(x_test)


# Pick Vectorizer
vectorizer = CountVectorizer(binary=True)
x_train_features = vectorizer.fit_transform(x_train)
x_test_features = vectorizer.transform(x_test)


def train(classifier, x, y):
    classifier.fit(x, y)


# Pick Classifier
classifier = DummyClassifier(strategy="uniform")


# Train
train(classifier, x_train_features, y_train)

y_pred_test = classifier.predict(x_test_features)
y_proba = classifier.predict_proba(x_test_features)

from sklearn.metrics import f1_score

output = []
x_test_list = x_test.to_list()
y_test_list = y_test.to_list()
experiment_size = y_pred_test.size // 5
trial = 0
experiment = []
y_true = []
y_pred = []
f1_scores = []
for i in range(y_pred_test.size + 1):
    if trial == experiment_size:
        output.append(experiment)
        experiment = []
        trial = 0
        f1_scores.append(f1_score(y_true, y_pred))
        y_true = []
        y_pred = []
    if i != y_pred_test.size:
        y_true.append(y_test_list[i])
        y_pred.append(y_pred_test[i])
        experiment.append(
            {
                "inputText": x_test_list[i],
                "realLabel": y_test_list[i],
                "classifierLabel": y_pred_test[i],
                "confidence": max(y_proba[i]),
            }
        )
    trial += 1

result = "cafe notebook complete"
