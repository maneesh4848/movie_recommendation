import numpy as np
from sklearn.externals import joblib
import json

def main():
    #opening files
    sgd = joblib.load('sgd_train_data.pkl')
    print "Training model loaded."

    train_reviews = None
    with open("./final_dataset/train/reviews.json", 'r') as f:
        train_reviews = json.load(f)
    print "Train file loaded."

    test_reviews = None
    with open("./final_dataset/test/reviews.json", 'r') as f:
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

    ratings = {}
    count = 0
    #predicting rating
    for name in train_reviews:
        preds = []
        real = []
        count += 1
        if count % 500 == 0:
            print count, "Movies done"
        #print "Number of reviews of:", name, "=", len(train_reviews[name])
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
            ratings[name] = [float(sum(real))/len(real),float(sum(preds))/len(preds)]
            ratings[name].append(abs(ratings[name][1] - ratings[name][0]))
    print "Train Movies Rated"

    for name in test_reviews:
        preds = []
        real = []
        #print "Number of reviews of:", name, "=", len(train_reviews[name])
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
            ratings[name] = [float(sum(real))/len(real),float(sum(preds))/len(preds)]
            ratings[name].append(abs(ratings[name][1] - ratings[name][0]))
    print "Test Movies Rated", len(ratings)

    ratings_file = open('./ratings.json', 'w')
    json.dump(ratings, ratings_file)
    ratings_file.close()

    nums = {}
    for i in range(1,25):
        nums[float(i)/5] = 0

    count = 0
    for name in ratings:
        if count < 5:
            bucket = float(int((ratings[name][2])/0.2) + 1)/5
            print name,ratings[name],bucket
            count += 1
        else:
            break

    for name in ratings:
        bucket = float(int((ratings[name][2])/0.2) + 1)/5
        try:
            nums[bucket] += 1
        except:
            print bucket

    for i in nums:
        print i
    print
    for i in nums:
        print nums[i]

if __name__ == '__main__':
    main()