import re,random,os
import json

def main():
    # opening files
    train_reviews = None
    with open("./final_dataset/train/reviews.json", 'r') as f:
        train_reviews = json.load(f)
    print "Train file loaded."

    test_reviews = None
    with open("./final_dataset/test/reviews.json", 'r') as f:
        test_reviews = json.load(f)
    print "Test file loaded."

    # getting samples
    small_train_data = []
    small_test_data = []
    for name in train_reviews:
        for review in train_reviews[name]:
            small_train_data.append(review)

    for name in test_reviews:
        for review in test_reviews[name]:
            small_test_data.append(review)
    print "Data loaded."

    # writing vocab to files
    fout_train = open('./final_dataset/train/all_reviews.json', 'w')
    json.dump(small_train_data,fout_train)
    fout_test = open('./final_dataset/test/all_reviews.json', 'w')
    json.dump(small_test_data,fout_test)

    fout_train.close()
    fout_test.close()


if __name__ == '__main__':
    main()