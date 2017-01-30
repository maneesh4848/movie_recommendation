from sklearn import linear_model
import json
from sklearn.externals import joblib

def main():
    BATCH_SIZE = 2000
    percep = linear_model.Perceptron()
    #opening files
    train_reviews = None
    with open("./final_dataset/train/all_reviews.json",'r') as f:
        train_reviews = json.load(f)
    print "Train file loaded."

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
    #y: class of each review
    X = []
    y = []
    count = 0
    for review in train_reviews:
        temp_vocab = {}
        text = review['reviewText'].split()
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
        X.append(temp)
        y.append(int(review['overall']))
        count += 1
        if count%BATCH_SIZE == 0:
            if count > BATCH_SIZE:
                percep.partial_fit(X,y)
            else:
                percep.partial_fit(X,y,[1.0,2.0,3.0,4.0,5.0])
            print "Fitted batch ", count/BATCH_SIZE, "of", len(train_reviews)/BATCH_SIZE
            X = []
            y = []

    if len(X) != 0:
        if len(train_reviews) < BATCH_SIZE:
            percep.partial_fit(X, y, [1.0, 2.0, 3.0, 4.0, 5.0])
        else:
            percep.partial_fit(X, y)
    print "Model Fitted."

    joblib.dump(percep, 'percep_train_data.pkl')
    print "Training Model Saved."


if __name__ == '__main__':
    main()