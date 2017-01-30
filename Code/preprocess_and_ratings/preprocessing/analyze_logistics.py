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

    log = {}
    for i in range(1,1001):
        log[i] = 0

    print len(train_vocab), len(test_vocab)
    for word in train_vocab:
        try:
            log[train_vocab[word][0]] += 1
        except KeyError:
            pass
            #print word, train_vocab[word][0]
    for i in range(1,1001):
        print i, float(log[i])/len(train_vocab)*100

    for i in range(1,1001):
        log[i] = 0
    for word in test_vocab:
        try:
            log[test_vocab[word][0]] += 1
        except KeyError:
            pass
            #print word, train_vocab[word][0]

    for i in range(1,1001):
        print i, float(log[i])/len(test_vocab)*100

if __name__ == '__main__':
    main()