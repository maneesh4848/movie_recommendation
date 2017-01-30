from __future__ import division
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec



def pie(predictions, labels, unique_genres):
	print ''
	clusters = defaultdict(list)
	for i in xrange(0, len(predictions)):
		for j in xrange(0, len(labels[i])):
			clusters[predictions[i]].append(labels[i][j])
	
	counts = {}
	for c in clusters:
		genre_counts = defaultdict(float)
		genre_lists = clusters[c]
		for i in xrange(0, len(genre_lists)):
			genre_counts[genre_lists[i]] += 1
		counts[c] = genre_counts

	i = 0
	cols = 4
	rows = (len(counts) // cols) + 1
	the_grid = GridSpec(cols, rows)
	plt.clf()
	for c in counts:
		col = i % cols
		row = i // cols
		plt.subplot(the_grid[col, row], aspect=1)

		print "CLUSTER : ",c
		d_view = [ (v,k) for k,v in counts[c].iteritems() ]
		d_view.sort(reverse=True)
	
		
		
		#colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'purple', 'red']
		label_counts = []
		for l in unique_genres:
			num = counts[c][l]
			label_counts.append(num)

		# label_counts.append(total)
		# labels.append('other')
		# Plot
		#plt.pie(label_counts, labels=unique_genres,autopct='%1.1f%%', shadow=True, startangle=140)
		plt.pie(label_counts, shadow=True, startangle=140)
 		tit = str(c)
 		plt.title(tit)
		plt.axis('equal')
		print '\n\n'
		i = i +1
	plt.show()

		