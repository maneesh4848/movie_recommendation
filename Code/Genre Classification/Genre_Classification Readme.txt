Most of the documentation has been done within the code using comments. The folowing describes elements that are not so obvious from the code
Please note that train/movies2.json and test/movies2.json are the datasets generated after reducing the 319 genres to 22. So before running this classfier model, please create the testing and training data by running the combining_tags python file. 


Function and objects				Description
		
get_output_tags_list(data)             	Input: Daictionary containing Movie Name, Gnere and plot
					Output:Returns a list of genres

get_y_vector_by_tag(data, tag)		Input: Daictionary containing Movie Name, Gnere and plot
					Output:Returns a target vector of the form [1,0,1,1,0,0...]. The ith element in the target will be 1 if the i'th element in dictionary has the 'tag' in its genre sublist. Else 0

Text Preprocessing  			The text preprocessing part has been commented out for performing a quick test run of the classifier.

X_train_counts				Training feature Vector

X_new_counts 				Testing feature Vector

clf					Primary classifier

clf2					Secondary classifier

index					Target vector of primary classifier

index2					Target vector of secondary classifier

predicted_data				Movie and their respective genres predicted by the primary classifier 

predicted_data2				Movie and their respective genres predicted by the secondary classifier


Thank You!