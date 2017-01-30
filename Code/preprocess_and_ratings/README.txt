Preprocessing Files
---------------------
1. extract_reviews - extracts all the reviews and and stores them as array in output json file.
2. write_spaces - writes space after full stop and comma in reviews.
3. make_vocab - extracts vocabulary from reviews.
4. remove_stopwords - removes stop words from vocab.
5. get_vocab_logistics - generates vocabulary logistics (logistics used to remove noisy words).
6. analyze_logistics - used to generate data required to set threshold for noisy features.
7. clean_vocab - removes noisy words.

Classifier Files
--------------------
1. NB - nb_train for training and nb_test for testing.
2. Bigram_NB - bigram_nb_train for training and bigram_nb_test for testing.
3. Perceptron - percep_train for training and percep_test for testing.
4. Linear SVM - sgd_train for training and sgd_test for testing.
5. Linear SVM with PCA - run pca.py before training with sgd_train and testing with sgd_test.

Utility Files
--------------------
1. sgd_interface - interface for movie recommendation system. Given movie name, gives actual and predicted ratings of the movie.
2. sgd_rating and rating_analysis were used to generate some logistics for the report including difference between actual rating and predicted rating.


Note: Input data paths might need to be changed appropriately.