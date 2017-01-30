from sklearn import linear_model
import numpy as np
from sklearn.externals import joblib
import json

def main():
    BATCH_SIZE = 1000
    #opening files
    sgd = joblib.load('sgd_train_data.pkl')
    print "Training model loaded."

    test_reviews = None
    with open("./final_dataset/test/all_reviews.json", 'r') as f:
        test_reviews = json.load(f)
    print "Test file loaded."

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
    print "Vocab Loaded.", len(vocab)
    vocab_pos = {}
    i = 0
    for word in vocab:
        vocab_pos[word] = i
        i += 1

    #predicting class of test data
    count = 0
    count2 = 0
    for review in test_reviews:
        temp_vocab = {}
        text = review['reviewText'].lower().split()
        for word in text:
            try:
                temp_vocab[word] += 1
            except KeyError:
                temp_vocab[word] = 1
        temp = [0]*len(vocab_pos)
        for word in temp_vocab:
            # word_count = 0
            # try:
            #     word_count = temp_vocab[word]
            # except:
            #     pass
            # temp.append(word_count)
            try:
                temp[vocab_pos[word]] += 1
            except KeyError:
                pass
        pred_class =  sgd.predict([temp])
        #print 'real class:', int(review['overall']), 'predicted class:', pred_class
        count2 += 1
        if int(review['overall']) == pred_class:
            count += 1
        if count2%BATCH_SIZE == 0:
            print count2, count
    print "Accuracy: ", float(count)/len(test_reviews)

if __name__ == '__main__':
    main()