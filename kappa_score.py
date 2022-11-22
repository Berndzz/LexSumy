from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import cohen_kappa_score

vectors = CountVectorizer()

a = []
b = []

scores = cohen_kappa_score(a,b)
print(scores)