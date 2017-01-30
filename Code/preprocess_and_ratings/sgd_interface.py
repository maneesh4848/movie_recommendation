import numpy as np
from sklearn.externals import joblib
import json

def main():
    name = raw_input("Give movie name: ")
    #name = name.lower()
    #opening files
    sgd = joblib.load('sgd_train_data.pkl')
    print "Training model loaded."

    train_reviews = None
    with open("./final_dataset/train/reviews.json", 'r') as f:
        train_reviews = json.load(f)
    #print "Train file loaded."

    test_reviews = None
    with open("./final_dataset/test/reviews.json", 'r') as f:
        test_reviews = json.load(f)
    #print "Test file loaded."

    # getting vocab
    vocab = set()
    with open('./final_dataset/train/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            vocab.add(word)
    with open('./final_dataset/test/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            vocab.add(word)
    #print "Vocab Loaded.", len(vocab)
    vocab_pos = {}
    i = 0
    for word in vocab:
        vocab_pos[word] = i
        i += 1

    #predicting rating
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
    else:
        flag = 0
        print "Movie Not Found in database"

    if flag == 1:
        print "Real Rating:", float(sum(real))/len(real), "Predicted Rating: ", float(sum(preds))/len(preds)

if __name__ == '__main__':
    main()