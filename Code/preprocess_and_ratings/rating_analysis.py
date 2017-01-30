import numpy as np
from sklearn.externals import joblib
import json

def main():
    #opening files
    ratings = None
    with open("./ratings.json", 'r') as f:
        ratings = json.load(f)
    print "Ratings file loaded."

    """for name in ratings:
        if len(ratings[name]) == 2:
            ratings[name].append(abs(ratings[name][1] - ratings[name][0]))

    ratings_file = open('./ratings.json', 'w')
    json.dump(ratings, ratings_file)
    ratings_file.close()"""
    nums = {}
    for i in range(1,25):
        nums[float(i)/5] = 0

    count = 0
    for name in ratings:
        if count < 5:
            print name,ratings[name]
            bucket = float(int((ratings[name][2])/0.2) + 1)/5
            count += 1
        else:
            break

    for name in ratings:
        bucket = float(int((ratings[name][2])/0.2) + 1)/5
        try:
            nums[bucket] += 1
        except:
            print bucket

    for i in nums:
        print i
    print
    for i in nums:
        print nums[i]

if __name__ == '__main__':
    main()