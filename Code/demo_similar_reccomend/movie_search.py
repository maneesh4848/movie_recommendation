import load_data
from collections import defaultdict

class movie_search_engine:
    def __init__(self):
        self.names_and_plots = load_data.all_names_and_plots()

    def exact_name_search(self, movie_query):
    	if movie_query in self.names_and_plots:
    		return movie_query, self.names_and_plots[movie_query]
    	else:
    		return None

    def closest_k_name_search(self, movie_query, k):
    	exact = None
    	counts = defaultdict(list)
    	query_tokens = movie_query.split()
    	results = []
    	for m in self.names_and_plots:
    		cur_count = 0
    		cur_tokens = m.split()
    		for qt in query_tokens:
    			if qt in cur_tokens:
    				#print qt, m, query_tokens, cur_tokens
    				cur_count = cur_count + 1
    		if cur_count > 0:
    			counts[cur_count].append(m) 	
    	i = len(query_tokens)
    	while i > 0:
    		if (i in counts) and (len(results) < k):
    			for j in xrange(0, len(counts[i])):
    				if len(results) < k:
    					results.append(counts[i][j])
    				else:
    					break
    		i = i-1
    	return results



# search = movie_search_engine()
# print search.closest_k_name_search('good will hunting', 10)
