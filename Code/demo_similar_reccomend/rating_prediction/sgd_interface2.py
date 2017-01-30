import numpy as np
from sklearn.externals import joblib
import json


def load_data():
    train_reviews = None
    test_reviews = None
    sgd = joblib.load('./rating_prediction/sgd_train_data.pkl')
    with open("../NLP_Dataset/final_dataset/train/reviews.json", 'r') as f:
        train_reviews = json.load(f)
    with open("../NLP_Dataset/final_dataset/test/reviews.json", 'r') as f:
        test_reviews = json.load(f)
    vocab = set()
    with open('./rating_prediction/final_dataset/train/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            vocab.add(word)
    with open('./rating_prediction/final_dataset/test/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            vocab.add(word)
    vocab_pos = {}
    i = 0
    for word in vocab:
        vocab_pos[word] = i
        i += 1
    print "Data Loaded"
    return sgd, train_reviews, test_reviews, vocab, vocab_pos

def predict_rating(sgd, train_reviews, test_reviews, vocab, vocab_pos, name):
    preds = []
    real = []
    flag = 1
    if name in train_reviews:
        print "Number of reviews of:", name, "=", len(train_reviews[name])
        for review in train_reviews[name]:
            temp_vocab = {}
            text = review['reviewText'].lower().split()
            for word in text:
                try:
                    temp_vocab[word] += 1
                except KeyError:
                    temp_vocab[word] = 1
            temp = np.zeros(len(vocab_pos))
            for word in temp_vocab:
                try:
                    temp[vocab_pos[word]] += 1
                except KeyError:
                    pass
            pred_class = sgd.predict([temp])
            preds.append(int(pred_class))
            real.append(int(review['overall']))
    elif name in test_reviews:
        print "Number of reviews of:", name, "=", len(test_reviews[name])
        for review in test_reviews[name]:
            temp_vocab = {}
            text = review['reviewText'].lower().split()
            for word in text:
                try:
                    temp_vocab[word] += 1
                except KeyError:
                    temp_vocab[word] = 1
            temp = np.zeros(len(vocab_pos))
            for word in temp_vocab:
                try:
                    temp[vocab_pos[word]] += 1
                except KeyError:
                    pass
            pred_class = sgd.predict([temp])
            preds.append(int(pred_class))
            real.append(int(review['overall']))
    else:
        flag = 0
        print "Movie Not Found in database"

    if flag == 1:
        print "Real Rating:", float(sum(real))/len(real), "Predicted Rating: ", float(sum(preds))/len(preds)




def main():
    name = raw_input("Give movie name: ")
    sgd, train_reviews, test_reviews, vocab, vocab_pos = load_data()
    predict_rating(sgd, train_reviews, test_reviews, vocab, vocab_pos,name)

if __name__ == '__main__':
    main()