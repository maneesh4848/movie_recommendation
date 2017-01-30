from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import load_data
#import cluster_analysis
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise

def names_to_plot_idx(names):
	ids = {}
	i = 0
	for n in names:
		ids[n] = i
		i = i + 1
	return ids

def idx_to_names(names):
	ids = {}
	i = 0
	for n in names:
		ids[i] = n
		i = i + 1
	return ids

# genres, plots, names = load_data.load_data_fields(load_data.TRAIN_LESS_GENRE_PATH)
# name_index = names_to_plot_idx()
# index_name = idx_to_names()


def knn_data():
	genres, plots, names = load_data.load_data_fields_2(load_data.TRAIN_LESS_GENRE_PATH, load_data.TEST_LESS_GENRE_PATH)
	name_index = names_to_plot_idx(names)
	index_name = idx_to_names(names)
	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, ngram_range=(2,2), stop_words='english')
	X = vectorizer.fit_transform(np.asarray(plots))
	return genres, plots, names, name_index, index_name, X

# #TFIDF vector
# vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, ngram_range=(2,2), stop_words='english')
# X = vectorizer.fit_transform(np.asarray(plots))

def closest_k_cosign_sims(movie_name, num_results):
	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, ngram_range=(2,3), stop_words='english')
	X = vectorizer.fit_transform(np.asarray(plots))
	movie_vector = X[name_index[movie_name]]
	sims = {}
	i=0
	for x in X:
		dist = pairwise.cosine_similarity(movie_vector, x)
		#print dist
		sims[dist[0][0]] = i
		i = i+1
	
	top_k = []
	num_res = 0
	for k in sorted(sims, reverse=True):
		top_k.append(index_name[sims[k]])
		#print k
		if len(top_k) == num_results:
			break

	return top_k

def closest_k_cosign_sims_2(movie_name, num_results, name_index, index_name, X):
	
	movie_vector = X[name_index[movie_name]]
	sims = {}
	i=0
	for x in X:
		dist = pairwise.cosine_similarity(movie_vector, x)
		#print dist
		sims[dist[0][0]] = i
		i = i+1
	
	top_k = []
	num_res = 0
	for k in sorted(sims, reverse=True):
		top_k.append(index_name[sims[k]])
		#print k
		if len(top_k) == num_results:
			break

	return top_k

# unique_genres = set()
# for g in genres:
# 	for gg in g:
# 		unique_genres.add(gg)

# print "UNIQUE GENRES: "+str(unique_genres)
# print len(unique_genres)

# print closest_k_cosign_sims('saving private ryan', 5)

def knn():
	print 'fitting knn'
	knn = NearestNeighbors(n_neighbors = 10, metric=pairwise.cosine_similarity)
	knn.fit(X)
	return knn

def knn_predict(model, movie_name, neighbors):
	results = model.kneighbors(X[name_index[movie_name]])
	print X[name_index[movie_name]]
	print results
	result_movies = []
	y = results[1]
	for x in y[0]:
		print x
		result_movies.append(index_name[x])
	return result_movies


# def k_means():
# 	#genres, plots = load_data()
# 	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, ngram_range=(2,2), stop_words='english')
# 	print 'vectorizer'
# 	X = vectorizer.fit_transform(np.asarray(plots))
# 	print 'fitting k means'
# 	km = KMeans(n_clusters=22, random_state=0, max_iter=100, precompute_distances=True)
# 	km.fit(X)
# 	print 'done fitting km'
# 	for k in km.labels_:
# 		print k
# 	cluster_analysis.pie(km.labels_, genres, unique_genres)
# 	return km



# #dont run this it will take forever
# def agglomerative():
# 	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,stop_words='english')
# 	print 'vectorizer'
# 	X = vectorizer.fit_transform(np.asarray(plots))
# 	X = X.toarray()
# 	print 'fitting agglomerative'
# 	ag = AgglomerativeClustering(linkage='ward', n_clusters=5)
# 	ag.fit(X)
# 	print 'done fitting ag'
# 	cluster_analysis.pie(ag.labels_, genres, unique_genres)
# 	return ag


# print 'FITTING MODEL'
# model = knn()
# print 'MAKING PREDICTION'
# print knn_predict(model, 'the godfather', 6)
