from nltk.corpus import stopwords

def main():
    # loading stopwords
    stop_words = set(stopwords.words('english')) - set('not')
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    stop_vocab = {}
    for word in stop_words:
        stop_vocab[word] = 1

    # loading files and removing stopwords
    train_vocab = set()
    with open('./final_dataset/train/review_vocab.txt','r') as f:
        for line in f.readlines():
            word = line[:-1]
            try:
                stop_vocab[word]
            except:
                train_vocab.add(word)
    test_vocab = set()
    with open('./final_dataset/test/review_vocab.txt', 'r') as f:
        for line in f.readlines():
            word = line[:-1]
            try:
                stop_vocab[word]
            except:
                test_vocab.add(word)
    print len(train_vocab),len(test_vocab)

    # re-writing vocab files
    fout_train = open('./final_dataset/train/review_vocab.txt', 'w')
    for word in train_vocab:
        fout_train.write(word + '\n')
    fout_test = open('./final_dataset/test/review_vocab.txt', 'w')
    for word in test_vocab:
        fout_test.write(word + '\n')

if __name__ == '__main__':
    main()