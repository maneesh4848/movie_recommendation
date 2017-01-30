import json

def main():
    # opening files
    train_reviews = None
    train_input = "./final_dataset/train/toy_reviews.json"
    test_input = "./final_dataset/test/toy_reviews.json"
    with open(train_input, 'r') as f:
        train_reviews = json.load(f)
    print "Train file loaded."

    test_reviews = None
    with open(test_input, 'r') as f:
        test_reviews = json.load(f)
    print "Test file loaded."

    train_vocab = {}
    with open('./final_dataset/train/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            train_vocab[word] = []
            train_vocab[word].append(0)
            train_vocab[word].append({1: 0, 2: 0, 3: 0, 4: 0, 5: 0})
    print "Train vocab loaded."
    test_vocab = {}
    with open('./final_dataset/test/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            test_vocab[word] = []
            test_vocab[word].append(0)
            test_vocab[word].append({1: 0, 2: 0, 3: 0, 4: 0, 5: 0})
    print "Test vocab loaded."
    print len(train_vocab), len(test_vocab)


    for review in train_reviews:
        text = review['reviewText'].split()
        for word in text:
            try:
                train_vocab[word][0] += 1
                train_vocab[word][1][int(review['overall'])] += 1
            except KeyError:
                pass
    print "Train vocab logistics loaded."
    for review in test_reviews:
        text = review['reviewText'].split()
        for word in text:
            try:
                test_vocab[word][0] += 1
                test_vocab[word][1][int(review['overall'])] += 1
            except KeyError:
                pass
    print "Test vocab logistics loaded."

    fout_train = open('./final_dataset/train/vocab_logistics.json', 'w')
    json.dump(train_vocab, fout_train)
    fout_test = open('./final_dataset/test/vocab_logistics.json', 'w')
    json.dump(test_vocab, fout_test)
    print "Logistics written."

    fout_train.close()
    fout_test.close()

if __name__ == '__main__':
    main()