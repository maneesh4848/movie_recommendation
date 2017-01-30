from __future__ import  division
import nltk
import pickle
from sklearn.externals import joblib
import json
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier


def get_output_tags_list(data):
    output_tags = []
    for i in data:
        for j in data[i][1]:
            if j not in output_tags:
                output_tags.append(j)
            else:
                pass
    output_tags.sort()
    return output_tags


def get_y_vector_by_tag(data, tag):

    print "Generating the output vector for tag: ", tag
    y = []
    for i in data:
        if tag in data[i][1]:
            y.append(1)
        else:
            y.append(0)
    y = np.array(y)
    return y



vectorizer= TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')

ob = open("train/movies2.json")
data = json.load(ob)

x_list=[]
count=0

######################Text Preprocessing#######################
for i in data:
#     count+=1
#     if count%1000==0:
#         print count
#
#     l = nltk.word_tokenize(data[i][2])
#     vocab = {}
#     filtered_vocab = []
#
#     l = [k.lower() for k in l]
#     for v in l:
#         if v in vocab:
#             vocab[v] += 1
#         else:
#             vocab[v] = 1
#     for v in vocab.keys():
#         if len(v) < 2:  # removing words that has less than 3 characters
#             del vocab[v]
#
#     for j in vocab:
#         if vocab[j] > 1:  # removing words with freq less than 5
#             filtered_vocab.append(j)
#
#     nstr = " ".join(filtered_vocab)
    x_list.append(data[i][2])

X_train_counts = vectorizer.fit_transform(x_list)
#joblib.dump(vectorizer,"model/"+'vectorizer.pkl')

print "Shape of training data", X_train_counts.shape


tob = open("test/movies2.json")
tdata = json.load(tob)

p_list=[]
for i in tdata:
    p_list.append(tdata[i][2])



X_new_counts = vectorizer.transform(p_list)

print "Shape of testing data",X_new_counts.shape

feature_names = vectorizer.get_feature_names()

target_names = get_output_tags_list(data)
print 'length of all total possible tags: ', len(target_names), 'Tags:', target_names

target_dic = {}
for tag in target_names:            # Generating y vector for each tag
    target_dic[tag] = get_y_vector_by_tag(data, tag)



predicted_data={}
movies_tagged=[]
for i in tdata:
    predicted_data[tdata[i][0]]=[]


op=[]

#Primary Classifier
###############################################################################

for tag in target_dic:
    print "New shape of training data", X_train_counts.shape
    print "New shape of testing data", X_new_counts.shape
    clf = LinearSVC(loss='l2', penalty='l2', dual=False, tol=1e-3)

    y = target_dic[tag]
    clf.fit(X_train_counts, y)
    index=clf.predict(X_new_counts)

    print "index:", index, "tag:",tag,"target vector",y
    counter = 0

    for i in tdata:
        if index[counter]==1:
            movies_tagged.append(tdata[i][0])
            predicted_data[tdata[i][0]].append(tag)
        counter+=1


#Secondary Classifier
##########################################
predicted_data2={}
movies_tagged2=[]
for i in tdata:
    predicted_data2[tdata[i][0]]=[]


#####Genrating seprate classifier for each tag#############

for tag in target_dic:
    print "New shape of training data", X_train_counts.shape
    print "New shape of testing data", X_new_counts.shape
    clf2 = Perceptron(n_iter=50)   #Secondary Classifer

    y2 = target_dic[tag]
    clf2.fit(X_train_counts, y2)
    index2=clf2.predict(X_new_counts)

    print "index2:", index2, "tag:",tag,"target vector",y
    counter = 0

    for i in tdata:
        if index2[counter]==1:
            movies_tagged2.append(tdata[i][0])
            predicted_data2[tdata[i][0]].append(tag)
        counter+=1



counter=0

################################################# Adding the results of the secondary classfier to the results of primary classifer for movies for which no genres were predicted************
for i in tdata:
    if len(predicted_data[tdata[i][0]])==0:
        counter+=1
        print counter
        predicted_data[tdata[i][0]]=predicted_data2[tdata[i][0]]
print "*****************************"
counter=0
for i in tdata:
    if len(predicted_data[tdata[i][0]])==0:
        counter+=1
movies_with_no_tags=counter
#########################################################################Checking the performance of the classifer ###########################################################################################3
counter = 0
correctly_tagged_genres = 0
incorrectly_tagged_genres=0
total_predicted_genres = 0
correctly_missed_nongenres=0
wrongly_missed_genres=0

for i in tdata: #Checking accuracy
    incorrectly_tagged_genres_i=0
    correctly_tagged_genres_i=0
    for j in predicted_data[tdata[i][0]]:
        total_predicted_genres+=1
        if j in tdata[i][1]:
            correctly_tagged_genres += 1
            correctly_tagged_genres_i += 1
        else:
            incorrectly_tagged_genres_i += 1
    wrongly_missed_genres += len(tdata[i][1])- correctly_tagged_genres_i
    correctly_missed_nongenres += len(target_names)-len(tdata[i][1]) - incorrectly_tagged_genres_i

true_positives = correctly_tagged_genres
false_positives = total_predicted_genres-correctly_tagged_genres
false_negatives = wrongly_missed_genres
true_negatives = correctly_missed_nongenres
print "*****Classifier Evaluation*****"
print "total predicted,", total_predicted_genres
print "True Positives", true_positives
print "False Positives", false_positives
print "False Negatives", false_negatives
print "True Negatives", true_negatives
print"************************"
precision = true_positives/(true_positives+false_positives)
recall = true_positives/(true_positives+false_negatives)
print "Precision:", precision
print "Recall:", recall
print "Acurracy",(true_positives+true_negatives)/(true_positives+true_negatives+false_positives+false_negatives)
print "F_Measure",2*(precision*recall)/(precision+recall)

movies_tagged=set(movies_tagged)
print"Number of movies with no tags", movies_with_no_tags

