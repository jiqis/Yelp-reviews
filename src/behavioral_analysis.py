import numpy as np
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer#TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

meta_path = '../data/YelpChi/output_meta_yelpResData_NRYRcleaned.txt'
review_path = '../data/YelpChi/output_review_yelpResData_NRYRcleaned.txt'

def main():
    reviewer_dict = defaultdict(list)
    product_ratings = defaultdict(list)
    print("Parsing through Chicago file")
    with open(meta_path, 'r') as meta_file, open(review_path, 'r') as review_file:
        review_lines = review_file.read().splitlines()
        meta_reader = csv.reader(meta_file, delimiter = ' ')
        idx = 0
        for review, meta in zip(review_lines, meta_reader):
            date, reviewID, reviewerID, productID, label, _, _, _, rating = meta
            reviewer_dict[reviewerID].append([date, reviewID, productID, 1 if label == 'Y' else 0, rating, review])
            product_ratings[productID].append(int(rating))
            idx+=1

    avg_product_scores = {}
    for productID, scores in product_ratings.items():
        avg_product_scores[productID] = np.mean(scores)

    reviewer_stats = {}
    fakeSimil = []
    realSimil = []
    fakeLength = []
    realLength = []
    fakeMax = []
    realMax = []
    fakePositive = []
    realPositive = []
    fakeDeviation = []
    realDeviation = []
    for reviewer, reviews in reviewer_dict.items():
        reviews = np.array(reviews)

        # Calculating maximum_number_of_reviews
        counter = Counter(reviews[:, 0])
        reviewer_stats[reviewer] = []
        maximum_number_of_reviews = counter.most_common(1)[0][1]

        # Calculating percentage_of_positive_reviews
        ratings = reviews[:, 4]
        ratings = np.array(list(map(int, ratings)))
        percentage_of_positive_reviews = len(ratings[ratings>=4])/len(ratings)

        # Calculating avg_review_length
        reviews_text = reviews[:, 5]
        avg_review_length = np.mean([len(sentence.split()) for sentence in reviews_text])

        # Calculate avg_deviation
        deviation = []
        for review_info in reviews:
            deviation.append(np.abs(avg_product_scores[review_info[2]] - int(review_info[4])))
        avg_deviation = np.mean(deviation)

        # Calculate maimum_content_similarity
        maximum_content_similarity = 0
        if len(reviews_text) > 1:
            vectorizer = CountVectorizer()
            counts_matrix = vectorizer.fit_transform(reviews_text)
            cosine_similarities = cosine_similarity(counts_matrix)
            np.fill_diagonal(cosine_similarities, 0)
            maximum_content_similarity = np.max(cosine_similarities)
        np.array(list(map(int, reviews[:,3])))
        if np.max(np.array(list(map(int, reviews[:,3])))) == 1:
            fakeSimil.append(maximum_content_similarity)
            fakeLength.append(avg_review_length)
            fakeMax.append(maximum_number_of_reviews)
            fakePositive.append(percentage_of_positive_reviews)
            fakeDeviation.append(avg_deviation)
        else:
            realSimil.append(maximum_content_similarity)
            realLength.append(avg_review_length)
            realMax.append(maximum_number_of_reviews)
            realPositive.append(percentage_of_positive_reviews)
            realDeviation.append(avg_deviation)
        reviewer_stats[reviewer] = [maximum_number_of_reviews, percentage_of_positive_reviews, avg_review_length, avg_deviation, maximum_content_similarity]
        
if __name__ == '__main__':
    main()
