import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import BernoulliNB

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt



df = pd.read_csv("get_out_cleaned.csv")
df.drop(columns=["Unnamed: 0"],inplace=True)
print(df.head())


# STOPWORDS
stop_words = set(stopwords.words('english')) # eng stopwords

df['tokenized_reviews'] = df.apply(lambda row: word_tokenize(row['Review']), axis=1) # Tokenizing reviews

df["filtered"] = df['tokenized_reviews'].apply(lambda x: [item for item in x if item not in stop_words]) #Removing stopwrods from tokenized data

print(df.dtypes)

# COUNT VECTORIZER
df['filtered']=df['filtered'].apply(str)

cv = CountVectorizer(lowercase=False,stop_words='english',binary=True)
cv.fit(df["filtered"])
X = cv.transform(df["filtered"])
#df["filtered_reviews"] = cv.fit_transform(df["filtered"])
#print(cv.vocabulary_)
#df.drop(columns=["tokenized_reviews"],inplace=True)


# LOGISTIC REGRESSION
#X = df["filtered_reviews"]
y = df["Rating"]
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
logModel = LogisticRegression(penalty='l2',max_iter=1000,C=0.3)
logModel.fit(X_train,y_train)
print(accuracy_score(y_test, logModel.predict(X_test)))


# K-NEAREST NEIGBHOURS

knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(X_train,y_train)
print(accuracy_score(y_test, knn.predict(X_test)))

# NLP
print("BAYES")
MNB = MultinomialNB()
MNB.fit(X_train,y_train)
print(accuracy_score(y_test, MNB.predict(X_test)))

CNB = ComplementNB()
CNB.fit(X_train,y_train)
print(accuracy_score(y_test, CNB.predict(X_test)))

BNB = BernoulliNB()
BNB.fit(X_train,y_train)
print(accuracy_score(y_test, BNB.predict(X_test)))





# WORD CLOUD
stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = stopwords,
                      min_font_size = 10).generate(' '.join(df['filtered']))

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

#plt.show()


