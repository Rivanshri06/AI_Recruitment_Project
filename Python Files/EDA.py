#!/usr/bin/env python
# coding: utf-8

# In[73]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from transformers import pipeline
nltk.download('stopwords')


# In[93]:


# Specify the folder path where your datasets are located
folder_path = 'recruitment_data'  # Update this to the folder where the datasets are located

# Initialize an empty list to store cleaned DataFrames
cleaned_dataframes = []

# List all Excel files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]


# In[95]:


# Cell 3: Convert text columns to lowercase
text_columns = ['Transcript', 'Resume', 'Job Description', 'Reason for decision']

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].str.lower()

print("Dataset after converting text to lowercase:")
print(df[text_columns].head())


# In[97]:


# Cell 4: Handle null values
df.drop_duplicates(inplace=True)
df.fillna('Not Specified', inplace=True)

# Print null values count after handling
print("Null values in the dataset:")
print(df.isnull().sum())


# In[99]:


# Cell 5: Remove stop words
stop_words = set(stopwords.words('english'))

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: ' '.join(word for word in str(x).split() if word not in stop_words))

print("Dataset after removing stop words:")
print(df[text_columns].head())


# In[101]:


# Cell 6: Tokenize text data
from nltk.tokenize import word_tokenize
nltk.download('punkt')

for col in text_columns:
    if col in df.columns:
        df[f'{col}_tokens'] = df[col].apply(word_tokenize)

print("Sample tokenized text:")
print(df[[f'{col}_tokens' for col in text_columns]].head())


# In[102]:


# Cell 7: Generate Bag of Words
bow_vectorizer = CountVectorizer(max_features=100)
bow_matrix = bow_vectorizer.fit_transform(df['Transcript'])

# Convert BoW to DataFrame
bow_df = pd.DataFrame(bow_matrix.toarray(), columns=bow_vectorizer.get_feature_names_out())
print("Bag of Words Representation (First 5 Rows):")
print(bow_df.head())


# In[105]:


# Cell 8: Generate TF-IDF Features
tfidf_vectorizer = TfidfVectorizer(max_features=100)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Transcript'])

# Convert TF-IDF to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
print("TF-IDF Representation (First 5 Rows):")
print(tfidf_df.head())


# In[107]:


# Cell 9: Text length statistics
df['Transcript_Length'] = df['Transcript'].apply(lambda x: len(str(x)))
df['Resume_Length'] = df['Resume'].apply(lambda x: len(str(x)))

print("Mean Transcript Length:", df['Transcript_Length'].mean())
print("Median Transcript Length:", df['Transcript_Length'].median())
print("Std Transcript Length:", df['Transcript_Length'].std())

print("Mean Resume Length:", df['Resume_Length'].mean())
print("Median Resume Length:", df['Resume_Length'].median())
print("Std Resume Length:", df['Resume_Length'].std())


# In[109]:


# Cell 10: Divide data by unique roles
if 'Role' in df.columns:
    roles = df['Role'].unique()
    print(f"Unique Roles: {roles}")
    for role in roles:
        role_df = df[df['Role'] == role]
        print(f"Role: {role}, Data Points: {len(role_df)}")
else:
    print("Role column not found in the dataset.")


# In[115]:


# Cell 12: Visualize Decision Distribution
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

if 'Decision' in df.columns:
    sns.countplot(data=df, x='Decision', palette='viridis')
    plt.title('Decision Distribution', fontsize=16)
    plt.xlabel('Decision', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




