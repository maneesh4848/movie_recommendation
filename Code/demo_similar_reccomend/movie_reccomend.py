# this script combines algorithms for genre classification, finding similar movies
# and rating predicton to recomend movies to a user
import sys
sys.path.append('./Genre_Classification')
sys.path.append('./rating_prediction')

import improved_clustering
import sys
import movie_search
import SVCclassifier
import sgd_interface
import load_data
from collections import defaultdict

# movie search functions
search = movie_search.movie_search_engine()

# load data needed for KNN similar movie finding
print 'Loading similar plot data'
genres, plots, names, name_index, index_name, X = improved_clustering.knn_data()

# movie asins
names_and_asins = load_data.all_names_and_asins()
print "Loading Review Data..."
sgd, train_reviews, test_reviews, vocab, vocab_pos = sgd_interface.load_data()
print "Done loading data!"

# step (1) find the 20 closest movies to the query movie
# step (2) predict the generes of those movies, and remove movies with different genre
# step (3) predict the ratings of the remaining movies and return the movie with the highest rating
def recomend_based_on_movie(movie_name):
	# get the 20 movies with the closest plots
	print "Finding the 20 most similar movies to ",movie_name
	mlist = improved_clustering.closest_k_cosign_sims_2(movie_name, 20, name_index, index_name, X)
	# get the genre predictions for all 20 movies
	predicted_generes = {}
	# get the rating predictions for all 20 movies
	predicted_ratings = {}
	
	for m in mlist:
		# plot for movie
		m_1, p = search.exact_name_search(m)
		# predict genre for movie
		predicted_generes[m_1] = SVCclassifier.predict_genre(p)
		#predict rating for movie
		asin = names_and_asins[m_1]
		act, pred = sgd_interface.predict_rating(sgd, train_reviews, test_reviews, vocab, vocab_pos, asin)
		predicted_ratings[m_1] = pred


	movie_genre = genres[name_index[movie_name]]


	# filter movies based on genre 
	# (return list of movies that share the most ammount of genres)
	genre_scores = defaultdict(list)
	for m in predicted_generes:
		cur_g = predicted_generes[m]
		count= 0
		for g in cur_g:
			if g in movie_genre:
				count = count + 1
		genre_scores[count].append(m)
	max_count = -1
	genre_list = None
	for c in genre_scores:
		if c > max_count and len(genre_scores[c]) > 1:
			max_count = c
			genre_list = genre_scores[c]
	if movie_name in genre_list:
		genre_list.remove(movie_name)
	print "original mlist:\n ", mlist
	print "G Score: ", max_count, "Filtered genres \n", genre_list
	
	# find the remaining movie with the highest predicted rating
	# this movie will be the recomendation
	max_rating = -1
	best_movie = None
	for m in genre_list:
		if predicted_ratings[m] > max_rating:
			max_rating = predicted_ratings[m]
			best_movie = m
	print "For query movie: ", movie_name 
	print "With genre: ", genres[name_index[movie_name]]
	print "Recomended movie is: ", best_movie
	print " 	With predicted genre: ", predicted_generes[best_movie]
	print "	With predicted rating: ", max_rating 
	print "Tony"

	return best_movie

	# return top movie

	#print mlist
	#print predicted_generes
	#print predicted_ratings

recomend_based_on_movie("saving private ryan")