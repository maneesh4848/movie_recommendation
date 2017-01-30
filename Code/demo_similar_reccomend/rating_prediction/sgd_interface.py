from __future__ import division
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
        word = word.encode('ASCII', 'ignore')
        word = word.replace('\r', '')
        vocab_pos[word] = i
        i += 1

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
                word = word.encode('ASCII', 'ignore').replace('\r', '')
                try:
                    temp_vocab[word] += 1
                except KeyError:
                    temp_vocab[word] = 1
            temp = np.zeros(len(vocab_pos))
            temp.flags.writeable=True
            for word in temp_vocab:
                try:
                    #print vocab_pos
                    temp[vocab_pos[word]] = temp[vocab_pos[word]] + 1

                except KeyError:
                    #temp[vocab_pos[word]] = 1
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
                word = word.encode('ASCII', 'ignore').replace('\r', '')
                try:
                    temp_vocab[word] += 1.0
                except KeyError:
                    temp_vocab[word] = 1.0
            temp = np.zeros(len(vocab_pos))
            temp.flags.writeable=True
            for word in temp_vocab:
                try:
                    
                    temp[vocab_pos[word]] =temp[vocab_pos[word]] + 1.0
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
        return float(sum(real))/len(real), float(sum(preds))/len(preds)





# def main():
    # name = raw_input("Give movie name: ")
    # #name = name.lower()
    # #opening files
    # sgd = joblib.load('sgd_train_data.pkl')
    # #print "Training model loaded."

    # train_reviews = None
    # with open("./final_dataset/train/all_reviews.json", 'r') as f:
    #     train_reviews = json.load(f)
    # #print "Train file loaded."

    # test_reviews = None
    # with open("./final_dataset/test/all_reviews.json", 'r') as f:
    #     test_reviews = json.load(f)
    # #print "Test file loaded."

    # # getting vocab
    # vocab = set()
    # with open('./final_dataset/train/review_vocab.txt', 'r') as f:
    #     for line in f.readlines():
    #         word = line[:-1]
    #         vocab.add(word)
    # with open('./final_dataset/test/review_vocab.txt', 'r') as f:
    #     for line in f.readlines():
    #         word = line[:-1]
    #         vocab.add(word)
    # #print "Vocab Loaded.", len(vocab)
    # vocab_pos = {}
    # i = 0
    # for word in vocab:
    #     vocab_pos[word] = i
    #     i += 1

    #predicting rating
    # preds = []
    # real = []
    # flag = 1
    # if name in train_reviews:
    #     print "Number of reviews of:", name, "=", len(train_reviews[name])
    #     for review in train_reviews[name]:
    #         temp_vocab = {}
    #         text = review['reviewText'].lower().split()
    #         for word in text:
    #             try:
    #                 temp_vocab[word] += 1
    #             except KeyError:
    #                 temp_vocab[word] = 1
    #         temp = np.zeros(len(vocab_pos))
    #         for word in temp_vocab:
    #             try:
    #                 temp[vocab_pos[word]] += 1
    #             except KeyError:
    #                 pass
    #         pred_class = sgd.predict([temp])
    #         preds.append(int(pred_class))
    #         real.append(int(review['overall']))
    # elif name in test_reviews:
    #     print "Number of reviews of:", name, "=", len(train_reviews[name])
    #     for review in train_reviews[name]:
    #         temp_vocab = {}
    #         text = review['reviewText'].lower().split()
    #         for word in text:
    #             try:
    #                 temp_vocab[word] += 1
    #             except KeyError:
    #                 temp_vocab[word] = 1
    #         temp = np.zeros(len(vocab_pos))
    #         for word in temp_vocab:
    #             try:
    #                 temp[vocab_pos[word]] += 1
    #             except KeyError:
    #                 pass
    #         pred_class = sgd.predict([temp])
    #         preds.append(int(pred_class))
    #         real.append(int(review['overall']))
    # else:
    #     flag = 0
    #     print "Movie Not Found in database"

    # if flag == 1:
    #     print "Real Rating:", float(sum(real))/len(real), "Predicted Rating: ", float(sum(preds))/len(preds)

# if __name__ == '__main__':
#     main()