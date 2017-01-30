import json

TRAIN_MOVIES_PATH = '../NLP_Dataset/final_dataset/train/movies.json'
TEST_MOVIES_PATH =  '../NLP_Dataset/final_dataset/test/movies.json'

TRAIN_LESS_GENRE_PATH = '../NLP_Dataset/less_genre_dataset/train/movies2.json'
TEST_LESS_GENRE_PATH = '../NLP_Dataset/less_genre_dataset/test/movies2.json'

# loads genre, plots, and names into 3 different arrays from the file passed as param
def load_data_fields(FILE_PATH):
	plots = None
	with open(FILE_PATH, 'r') as f:
		plots = json.load(f)
	genre_data = []
	plot_data = []
	name_data = []
	
	for p in plots:
		for i in xrange(len(plots[p][1])):
			plots[p][1][i] =  plots[p][1][i].encode('ASCII', 'ignore')
		plots[p][2] =  plots[p][2].encode('ASCII', 'ignore')


	#filter_plots(plots)
	for p in plots:
		genre_data.append(plots[p][1])
		plot_data.append(plots[p][2])
		name_data.append(plots[p][0])

	return genre_data, plot_data, name_data

# loads genre, plots, and names into 3 different arrays from the file passed as param
def load_data_fields_2(FILE_PATH, FILE_PATH_2):
	plots = None
	with open(FILE_PATH, 'r') as f:
		plots = json.load(f)
	genre_data = []
	plot_data = []
	name_data = []
	
	for p in plots:
		for i in xrange(len(plots[p][1])):
			plots[p][1][i] =  plots[p][1][i].encode('ASCII', 'ignore')
		plots[p][2] =  plots[p][2].encode('ASCII', 'ignore')


	#filter_plots(plots)
	for p in plots:
		genre_data.append(plots[p][1])
		plot_data.append(plots[p][2])
		name_data.append(plots[p][0])

	plots = None
	with open(FILE_PATH_2, 'r') as f:
		plots = json.load(f)
	
	for p in plots:
		for i in xrange(len(plots[p][1])):
			plots[p][1][i] =  plots[p][1][i].encode('ASCII', 'ignore')
		plots[p][2] =  plots[p][2].encode('ASCII', 'ignore')


	#filter_plots(plots)
	for p in plots:
		genre_data.append(plots[p][1])
		plot_data.append(plots[p][2])
		name_data.append(plots[p][0])



	return genre_data, plot_data, name_data

# loads both the testing / training names and plots into a python dict
def all_names_and_plots():
	plots = None
	with open(TRAIN_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	name_and_plots = {}
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
		plots[p][2] =  plots[p][2].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = plots[p][2]
	plots = None
	with open(TEST_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
		plots[p][2] =  plots[p][2].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = plots[p][2]
	return name_and_plots

def all_names_and_genres():
	plots = None
	with open(TRAIN_LESS_GENRE_PATH, 'r') as f:
		plots = json.load(f)
	name_and_plots = {}
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
		for i in xrange(len(plots[p][1])):
			plots[p][1][i] =  plots[p][1][i].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = plots[p][1]
	plots = None
	with open(TEST_LESS_GENRE_PATH, 'r') as f:
		plots = json.load(f)
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
		for i in xrange(len(plots[p][1])):
			plots[p][1][i] =  plots[p][1][i].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = plots[p][1]
	return name_and_plots


def all_names_and_asins():
	plots = None
	with open(TRAIN_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	name_and_asins = {}
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
		name_and_asins[plots[p][0]] = p
	plots = None
	with open(TEST_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
	for p in plots:
		name_and_asins[plots[p][0]] = p
	return name_and_asins

def all_names_test_or_train():
	plots = None
	with open(TRAIN_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	name_and_plots = {}
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = 'TRAIN'
	plots = None
	with open(TEST_MOVIES_PATH, 'r') as f:
		plots = json.load(f)
	for p in plots:
		plots[p][0] =  plots[p][0].encode('ASCII', 'ignore')
	for p in plots:
		name_and_plots[plots[p][0]] = 'TEST'
	return name_and_plots

