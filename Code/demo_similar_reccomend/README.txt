
README for current directory… This directory has the implementation code for 
-similar movie searching, 
-the demo app for data & model visualization, 
-integrating all 3 tasks for movie recommendation.

File descriptions:

app.py - This is the Demo app that we showed to Abe at the poster session.  This application allows users to search our data set for a movie, view the plot, predict similar movies, predict genre, and predict rating.  We run it with “python2.7 app.py”, but we have removed the data from submission.  See APP.png to see what it looks like

movie_reccomend.py - This is the code for integrating the three tasks of finding similar movies, genre prediction, and rating prediction to make a movie recommendation.   We run it with: “python2.7 movie_reccomend.py”, but we have removed the data from the submission.
see recommend.png to see what the output looks like.

improved_clustering.py - This file has the code for finding similar movies with KNN, and clustering methods (mainly k-means).  We would have renamed it, but several file paths in our code referred to this file already.

movie_search.py - this file handled all searching for movies in app.py

load_data.py - this file handles loading various parts of our data set (which was removed for submission)

Genre_classiication/ - This directory has code for loading the SVM produced for genre classification.  this code does not show any implementation code, and relies on .PLK files that were removed for submission.

rating_prediction/ - This directory has code for loading the SVM produced for rating prediction.  this code does not show any implementation code, and relies on .PLK files that were removed for submission.




