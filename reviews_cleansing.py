import pandas as pd
import numpy as np

df = pd.read_csv("get_out_(i)_(2017).csv")
df.rename(columns={"Unnamed: 0" : "Movie_ID"},inplace=True)
print(df.head())

df["Rating"] = df["Review"].apply(lambda x: x.split("|")[0])
df["Review"] = df["Review"].apply(lambda x: x.split("|")[1])

# CLEANSING REVIEW
# Clean text before implementing nlp
df['Review'].replace(" ", np.nan, inplace=True) # replacing space with nan

df.dropna(inplace=True) #drop nan values, coz some of review didn't have actual review
df["Review"] = df["Review"].str.lower() # Converting everything to lower coz "Movie" and "movie" is not the same thing

# Removing special characters from Reviews
spec_chars = ["±","@","#","$","%","^",
                 "&","*","(",")","_","+","=",
                 "-","/",">","<","?",
                 "~","`","'","[","]","|","}",
                 "{",'"', ".",",","!",";"]

for char in spec_chars:
    df["Review"] = df["Review"].str.replace(char, "")

df["Review"].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii')) # getting rid of emojis

df['Review'] = df['Review'].str.replace('\d+', '') # Remove numbers from Reviews


# CLEANSING AND CONVERTING RATING
df["Rate"] = df["Rating"].apply(lambda x: x.split("/")[0])
df["Rate"] = pd.to_numeric(df["Rate"])

for i in range(len(df)):
    if (df["Rate"].iloc[i] < 5):
        df["Rating"].iloc[i] = "negative"
    else:
        df["Rating"].iloc[i] = "positive"



df.to_csv("get_out_cleaned.csv")








