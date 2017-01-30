import json

def main():
    train_input = "./final_dataset/train/vocab_logistics.json"
    test_input = "./final_dataset/test/vocab_logistics.json"

    train_vocab = None
    with open(train_input, 'r') as f:
        train_vocab = json.load(f)
    print "Train vocab loaded."

    test_vocab = None
    with open(test_input, 'r') as f:
        test_vocab = json.load(f)
    print "Test vocab loaded."

    new_train = {}
    count = 0
    for word in train_vocab:
        flag = 1
        for num in train_vocab[word][1]:
            if train_vocab[word][1][num] > 1:
                flag = 0
                break
        if flag == 1:
            count += 1
        else:
            new_train[word] = train_vocab[word]
    print "Train vocab cleaned.", float(count)/len(train_vocab)

    new_test = {}
    count = 0
    for word in test_vocab:
        flag = 1
        for num in test_vocab[word][1]:
            if test_vocab[word][1][num] > 1:
                flag = 0
                break
        if flag == 1:
            count += 1
        else:
            new_test[word] = test_vocab[word]
    print "Test vocab cleaned.", float(count)/len(test_vocab)

    fout_train = open('./final_dataset/train/review_vocab.txt', 'w')
    for word in new_train:
        fout_train.write(word + '\n')
    fout_test = open('./final_dataset/test/review_vocab.txt', 'w')
    for word in new_test:
        fout_test.write(word + '\n')


if __name__ == '__main__':
    main()