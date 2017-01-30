import json,nltk

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
    print len(train_reviews), len(test_reviews)

    # getting vocab and re-writing files
    train_vocab = set()
    new_train = []
    new_test = []
    train = open(train_input,'w')
    test = open(test_input,'w')
    for review in train_reviews:
        temp = {}
        temp['asin'] = review['asin']
        text = nltk.word_tokenize(review['reviewText'].lower())
        temp['reviewText'] = ' '.join(text)
        temp['helpful'] = review['helpful']
        temp['overall'] = review['overall']
        temp['summary'] = review['summary']
        new_train.append(temp)
        for word in text:
            train_vocab.add(word)
    print "Train vocab loaded."
    test_vocab = set()
    for review in test_reviews:
        temp = {}
        temp['asin'] = review['asin']
        text = nltk.word_tokenize(review['reviewText'].lower())
        temp['reviewText'] = ' '.join(text)
        temp['helpful'] = review['helpful']
        temp['overall'] = review['overall']
        temp['summary'] = review['summary']
        new_test.append(temp)
        for word in text:
            test_vocab.add(word)
    print "Test vocab loaded."
    print len(train_vocab), len(test_vocab)

    json.dump(new_train, train)
    json.dump(new_test, test)
    print "Files re-written."

    # writing vocab to files
    fout_train = open('./final_dataset/train/review_vocab.txt','w')
    for word in train_vocab:
        fout_train.write(word + '\n')
    fout_test = open('./final_dataset/test/review_vocab.txt', 'w')
    for word in test_vocab:
        fout_test.write(word + '\n')

    fout_train.close()
    fout_test.close()
    train.close()
    test.close()

if __name__ == '__main__':
    main()