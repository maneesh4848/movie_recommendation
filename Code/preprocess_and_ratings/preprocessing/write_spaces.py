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

    # re-writing files
    new_train = []
    new_test = []
    train = open(train_input,'w')
    test = open(test_input,'w')
    for review in train_reviews:
        temp = {}
        temp['asin'] = review['asin']
        temp['summary'] = review['summary']
        temp['helpful'] = review['helpful']
        temp['overall'] = review['overall']
        temp['reviewText'] = review['reviewText'].lower().replace('.', '. ').replace(',',', ')
        new_train.append(temp)
    #print "Train vocab loaded."

    for review in test_reviews:
        temp = {}
        temp['asin'] = review['asin']
        temp['summary'] = review['summary']
        temp['helpful'] = review['helpful']
        temp['overall'] = review['overall']
        temp['reviewText'] = review['reviewText'].lower().replace('.', '. ')
        new_test.append(temp)
    #print "Test vocab loaded."

    fout_train = open('./final_dataset/train/toy_reviews.json', 'w')
    json.dump(new_train, fout_train)
    fout_test = open('./final_dataset/test/toy_reviews.json', 'w')
    json.dump(new_test, fout_test)
    print "Files re-written."

    train.close()
    test.close()

if __name__ == '__main__':
    main()