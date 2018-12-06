import csv

import os, fnmatch
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn.metrics import precision_recall_fscore_support

def load_yelp_dataset_full(folder):
	reviews = []
	labels = []

	with open(folder + "output_review_yelpResData_NRYRcleaned.txt") as f:
		reviews = f.read().splitlines()

	with open(folder + "output_meta_yelpResData_NRYRcleaned.txt") as f:
		for line in f.readlines():
			metadata = line.split()
			labels.append(int(metadata[4] == "Y"))

	return np.array(reviews), np.array(labels)

def load_review_dataset(folder, folds):
	"""Load the review dataset from a given polarity folder

	Uses the Cornell dataset

	Arg:
		folder: Path to the folder that we want to crawl through
		folds: a list of the folds that we should crawl through to get the reviews

	Returns:
		reviews: A list of string values containing the text of each review
		labels: The binary labels (0 or 1) for each review. 1 indicats fake!
	"""

	reviews = []
	labels = []

	# Now we want to crawl through the folders 
	# - deceptive..
	# - truthful..
	fake = False
	for root, dirs, files in os.walk(folder):
		directory = os.path.basename(root)

		if (directory[-1: ] in folds):
			for file in files:
				with open(os.path.join(root, file)) as f:
					for review in f.readlines():
						reviews.append(review.strip())
						labels.append(1 if fake else 0)
		elif ("deceptive" in directory):
			fake = True
		elif ("truthful" in directory):
			fake = False

	return reviews, np.array(labels)

def load_review_dataset_full(folder):
	reviews = []
	labels = []
	skip_files = ['LICENSE', "README.md", "labeled_reviews.tsv"]
	fake = False
	for root, dirs, files in os.walk(folder):
		directory = os.path.basename(root)
		if ("deceptive" in directory):
			fake = True
		elif ("truthful" in directory):
			fake = False


		for file in files:
			if file in skip_files:
				continue
			with open(os.path.join(root, file)) as f:
				for review in f.readlines():
					reviews.append(review.strip())
					labels.append(1 if fake else 0)

	# Output a file with the reviews
	output_file = True
	if (output_file):
		# Dump the reviews to file
		new_file = "./data/op_spam_v1.4/labeled_reviews.tsv"
		with open(new_file, 'w') as f:
			for i in range(len(reviews)):
				#label = 1 if labels[i] == 'Y' else 0
				print('%s\t%d' % (reviews[i], labels[i]), file=f) 

	return np.array(reviews), np.array(labels)

		

def accuracy_predictor(true_labels, prections):
	return np.mean(prections == test_labels)

def precision_recall_fscore(true_labels, prections, average='binary'):
	precision, recall, fscore, _ = precision_recall_fscore_support(true_labels, prections, average=average)
	return precision, recall, fscore

def write_json(filename, value):
    """Write the provided value as JSON to the given filename"""
    with open(filename, 'w') as f:
        json.dump(value, f)
     
#reviews, labels = load_review_dataset('../op_spam_v1.4/positive_polarity/', ['1'])
#print (reviews)
# load_review_dataset_full('./data/op_spam_v1.4')
	