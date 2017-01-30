from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from sklearn import naive_bayes as NB
import numpy as np
import json,nltk
from sklearn.externals import joblib


def main():
    BATCH_SIZE = 2000
    #opening files
    nb = joblib.load('bigram_nb_train_data.pkl')
    print "Training model loaded."

    test_reviews = None
    with open("./final_dataset/test/all_reviews.json", 'r') as f:
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
    score_fn = BigramAssocMeasures.chi_sq
    bigram_finder = BigramCollocationFinder.from_words(vocab)
    bigrams = bigram_finder.nbest(score_fn, 1000)
    print "Bigrams Loaded.", len(bigrams)


    vocab_pos = {}
    i = 0
    for word in bigrams:
        vocab_pos[word] = i
        i += 1

    #predicting class of test data
    count = 0
    count2 = 0
    for review in test_reviews:
        temp_vocab = {}
        text = nltk.bigrams(review['reviewText'].split())
        for word in text:
            try:
                temp_vocab[word] += 1
            except KeyError:
                temp_vocab[word] = 1
        #temp = [0]*len(vocab_pos)
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
        pred_class =  nb.predict([temp])
        #print 'real class:', int(review['overall']), 'predicted class:', pred_class
        count2 += 1
        if int(review['overall']) == pred_class:
            count += 1
        if count2%BATCH_SIZE == 0:
            print count2, count
    print "Accuracy: ", float(count)/len(test_reviews)

if __name__ == '__main__':
    main()