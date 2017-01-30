from __future__ import  division
from sklearn.externals import joblib

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

dir_path = './Genre_Classification/'

vectorizer = joblib.load(dir_path +'vectorizer.pkl')

tags=[u'action', u'adventure', u'black-and-white', u'comedy', u'coming of age', u'crime', u'drama', u'family', u'fantasy', u'history', u'horror', u'indie', u'music', u'mystery', u'other category', u'romance', u'science fiction', u'sports', u'thriller', u'war film', u'western', u'world cinema']


# COMMAND LINE VERSION

# genres=[]


# inp= raw_input("Enter plot")
# inp=unicode(inp,errors='ignore')
# counts=[inp]
# counts=vectorizer.transform(counts)

# for tag in tags:
#     clf = joblib.load(str(tag)+'.pkl')
#     classifier_output = clf.predict(counts)
#     if (classifier_output[0]==1):
#         genres.append(tag)
# print "The predicted genres of the movie are: ", genres


# FUNCTION VERSION

def predict_genre(movie_plot):
	#print "STARTING PREDICTION"
	genres=[]
	movie_plot = movie_plot.replace('\n', ' ').replace('\r', ' ')
	inp=unicode(movie_plot,errors='ignore')
	counts=[movie_plot]
	counts=vectorizer.transform(counts)
	for tag in tags:
		clf = joblib.load(dir_path+str(tag)+'.pkl')
		classifier_output = clf.predict(counts)
		if (classifier_output[0]==1):
			genres.append(tag)
	for i in xrange(len(genres)):
			genres[i] =  genres[i].encode('ASCII', 'ignore')

	return genres



