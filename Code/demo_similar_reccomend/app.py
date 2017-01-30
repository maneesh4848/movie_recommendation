#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


import sys

sys.path.append('./Genre_Classification')
sys.path.append('./rating_prediction')

import Tkinter
import movie_search
import copy
import SVCclassifier
import load_data
import sgd_interface
import improved_clustering


NUMBER_SEARCH_RESULTS = 10
WINDOW_SIZE = '800x650'

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        print "Loading Data..."
        self.search_frame = None
        self.search = movie_search.movie_search_engine()
        self.current_search = None
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.names_and_genres = load_data.all_names_and_genres()
        self.names_test_or_train = load_data.all_names_test_or_train()
        self.names_and_asins = load_data.all_names_and_asins()

        print 'Loading similar plot data'
        self.genres, self.plots, self.names, self.name_index, self.index_name, self.X = improved_clustering.knn_data()

        print "Loading Review Data..."
        self.sgd, self.train_reviews, self.test_reviews, self.vocab, self.vocab_pos = sgd_interface.load_data()
        
        print "Done loading data!"
        #parent.minsize(500,500);

        self.initialize()

    def initialize(self):
        self.grid()

        # search bar text
        self.entryVariable = Tkinter.StringVar()
        # search bar
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Search For Movie.")

        # search button
        button = Tkinter.Button(self,text=u"Search !", command=self.do_search)
        button.grid(column=1,row=0)

        # frame for search results
        search_width = 500
        self.search_frame = Tkinter.Frame(width=search_width, height=50, bg="gray", colormap="new")
        self.search_frame.grid(column=0, row=2, columnspan=2, sticky='EW')

        self.plot_view = None
        # the grid
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        #self.geometry(self.geometry())
        self.geometry(WINDOW_SIZE)       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        

    def do_search(self):
        query_term = self.entryVariable.get()
        search_results = self.search.closest_k_name_search(query_term.lower(), NUMBER_SEARCH_RESULTS)
        result_string = ""
        # for res in search_results:
        #     result_string = result_string + res + '\n'
        # self.labelVariable.set( result_string )
        for w in self.search_frame.winfo_children():
            w.destroy()
        if self.plot_view != None:
            self.plot_view.destroy()
        rows = 0
        for i in xrange(0, len(search_results)):
            movie_string = '('+self.names_test_or_train[search_results[i]]+') '+search_results[i]
            label = Tkinter.Label(self.search_frame,text=movie_string, anchor="w",fg="black",bg="gray")
            label.grid(column=0,row=rows,sticky='EW')
            plot_but = Tkinter.Button(self.search_frame, text='PLOT', anchor="w", command=lambda x=search_results[i]: self.display_plot(x))
            plot_but.grid(column=1, row=rows, sticky='EW')
            sim_but = Tkinter.Button(self.search_frame, text='Find Similar Movies', anchor="w", command=lambda x=search_results[i]: self.find_similar_movies(x))
            sim_but.grid(column=2, row=rows, sticky='EW')
            genre_but = Tkinter.Button(self.search_frame, text='Predict Genre', anchor="w", command=lambda x=search_results[i]: self.predict_genre(x))
            genre_but.grid(column=3, row=rows, sticky='EW')
            rating_but = Tkinter.Button(self.search_frame, text='Predict Rating', anchor="w", command=lambda x=search_results[i]: self.predict_rating(x))
            rating_but.grid(column=4, row=rows, sticky='EW')
            rows = rows+1

        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def find_similar_movies(self, movie_name):
        mlist = improved_clustering.closest_k_cosign_sims_2(movie_name, 5, self.name_index, self.index_name, self.X)
        print mlist
        mov_plt = {}
        for ml in mlist:
            mov_plt[ml] = self.search.exact_name_search(ml)

        #m, p = self.search.exact_name_search(movie_name)
        #print p

        for w in self.search_frame.winfo_children():
            w.destroy()



        if self.plot_view != None:
            self.plot_view.destroy()
        rows = 0
        for m in mov_plt:
            movie_string = '('+self.names_test_or_train[m]+') '+m
            label = Tkinter.Label(self.search_frame,text=movie_string, anchor="w",fg="black",bg="gray")
            label.grid(column=0,row=rows,sticky='EW')
            plot_but = Tkinter.Button(self.search_frame, text='PLOT', anchor="w", command=lambda x=m: self.display_plot(x))
            plot_but.grid(column=1, row=rows, sticky='EW')
            sim_but = Tkinter.Button(self.search_frame, text='Find Similar Movies', anchor="w", command=lambda x=m: self.find_similar_movies(x))
            sim_but.grid(column=2, row=rows, sticky='EW')
            genre_but = Tkinter.Button(self.search_frame, text='Predict Genre', anchor="w", command=lambda x=m: self.predict_genre(x))
            genre_but.grid(column=3, row=rows, sticky='EW')
            rating_but = Tkinter.Button(self.search_frame, text='Predict Rating', anchor="w", command=lambda x=m: self.predict_rating(x))
            rating_but.grid(column=4, row=rows, sticky='EW')
            rows = rows+1



        #bottom view
        self.plot_view = Tkinter.Text(self,fg="black",bg="gray")
        title = 'Movies with closest cosine similarity to:: '+movie_name+' ('+self.names_test_or_train[movie_name]+' SET)\n\n'
        self.plot_view.insert(Tkinter.END, title)
    
        act_str = "\n\n" + str(mlist)
        self.plot_view.insert(Tkinter.END, act_str)
        self.plot_view.grid(column=0,columnspan=2,row=3,sticky='EW')

        

        #print "Should find similar movies, needs implementing"

    def predict_rating(self, movie_name):
        asin = self.names_and_asins[movie_name]
        print len(self.train_reviews), len(self.test_reviews), len(self.vocab), len(self.vocab_pos)
        act, pred = sgd_interface.predict_rating(self.sgd, self.train_reviews, self.test_reviews, self.vocab, self.vocab_pos, asin)
        if self.plot_view != None:
            self.plot_view.destroy()
        self.plot_view = Tkinter.Text(self,fg="black",bg="gray")
        title = 'RATING PREDICTION FOR: '+movie_name+' ('+self.names_test_or_train[movie_name]+' SET)\n\n'
        self.plot_view.insert(Tkinter.END, title)
        pred_str = "PREDICTED RATING: "+str(pred)
        self.plot_view.insert(Tkinter.END, pred_str)
        act_str = "\n\nACTUAL RATING: " + str(act)
        self.plot_view.insert(Tkinter.END, act_str)
        self.plot_view.grid(column=0,columnspan=2,row=3,sticky='EW')

    def predict_genre(self, movie_name):
        m, p = self.search.exact_name_search(movie_name)
        genre_prediction = SVCclassifier.predict_genre(p)
        if self.plot_view != None:
            self.plot_view.destroy()
        self.plot_view = Tkinter.Text(self,fg="black",bg="gray")
        title = 'GENRE PREDICTION FOR: '+m+' ('+self.names_test_or_train[m]+' SET)\n\n'
        self.plot_view.insert(Tkinter.END, title)
        pred_str = "PREDICTED GENRES: "+str(sorted(genre_prediction))
        self.plot_view.insert(Tkinter.END, pred_str)
        act_str = "\n\nACTUAL GENRES: " + str(sorted(self.names_and_genres[m]))
        self.plot_view.insert(Tkinter.END, act_str)
        self.plot_view.grid(column=0,columnspan=2,row=3,sticky='EW')

    def display_plot(self, movie_name):
        m, p = self.search.exact_name_search(movie_name)
        #print p
        if self.plot_view != None:
            self.plot_view.destroy()
        self.plot_view = Tkinter.Text(self,fg="black",bg="gray")
        title = 'PLOT FOR: '+m+'\n\n'
        self.plot_view.insert(Tkinter.END, title)
        self.plot_view.insert(Tkinter.END, p)
        self.plot_view.grid(column=0,columnspan=2,row=3,sticky='EW')
        
        return p


    def OnPressEnter(self,event):
        self.do_search()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('CS585 Movie Recommendation System')
    app.mainloop()