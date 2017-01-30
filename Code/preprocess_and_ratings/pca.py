from sklearn import naive_bayes as NB
import numpy as np
import json
from sklearn.externals import joblib
from sklearn.decomposition import incremental_pca as PCA

def main():
    BATCH_SIZE = 500
    #opening files
    pca = PCA.IncrementalPCA(n_components=200)
    train_reviews = None
    with open("./final_dataset/train/all_reviews.json",'r') as f:
        train_reviews = json.load(f)
    print "Train file loaded."
    test_reviews = None
    with open("./final_dataset/train/all_reviews.json", 'r') as f:
        test_reviews = json.load(f)
    print "Test file loaded."

    #getting vocab
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

    #constructing parameters
    #X: for each review list of counts for each word
    X = []
    count = 0
    for review in train_reviews:
        temp_vocab = {}
        text = review['reviewText'].split()
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
        X.append(temp)
        count += 1
        if count%BATCH_SIZE == 0:
            pca.partial_fit(X)
            print "Fitted batch ", count/BATCH_SIZE, "of", len(train_reviews)/BATCH_SIZE
            X = []
            y = []

    if len(X) != 0:
        pca.partial_fit(X)
    print "Train Model Fitted."

    X = []
    count = 0
    for review in test_reviews:
        temp_vocab = {}
        text = review['reviewText'].split()
        for word in text:
            try:
                temp_vocab[word] += 1
            except KeyError:
                temp_vocab[word] = 1
        temp = np.zeros(len(vocab_pos))
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
        X.append(temp)
        count += 1
        if count % BATCH_SIZE == 0:
            pca.partial_fit(X)
            print "Fitted batch ", count / BATCH_SIZE, "of", len(train_reviews) / BATCH_SIZE
            X = []
            y = []

    """if len(X) != 0:
        pca.partial_fit(X)"""
    print "Test Model Fitted."

    joblib.dump(pca, 'pca_data.pkl')
    print "PCA Model Saved."


if __name__ == '__main__':
    main()