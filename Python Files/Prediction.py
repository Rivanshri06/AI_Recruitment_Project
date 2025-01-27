# -*- coding: utf-8 -*-
"""Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HtvYudKXhbnRN4iOK4-4qS6FynTj0qdZ
"""

# Import required libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# Load the dataset
predict_df = pd.read_excel('prediction_data.xlsx')

# Display the first few rows of the dataset
print("Initial Dataset:\n")
predict_df.head()

# Define text columns for preprocessing
text_columns = ['Transcript', 'Resume', 'Job Description', 'Reason for decision']

# Convert text to lowercase
for col in text_columns:
    if col in predict_df.columns:
        predict_df[col] = predict_df[col].str.lower()

# Handle duplicates and missing values
predict_df.drop_duplicates(inplace=True)
predict_df.fillna('Not Specified', inplace=True)

# Check for null values
print("Null values in combined dataset:")
predict_df.isnull().sum()

prediction_df['Role'].unique()

unique_count = prediction_df.groupby('Role')['ID'].count()
unique_count

# Initialize and train TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()
all_text = pd.concat([predict_df[col] for col in text_columns if col in predict_df.columns])
tfidf_vectorizer.fit(all_text) # Fit on all text data

# Transform text columns
tfidf_transcript = tfidf_vectorizer.transform(predict_df['Transcript'])
tfidf_resume = tfidf_vectorizer.transform(predict_df['Resume'])
tfidf_job_desc = tfidf_vectorizer.transform(predict_df['Job Description'])

# Calculate cosine similarities
predict_df['resume_job_similarity'] = [cosine_similarity(tfidf_resume[i], tfidf_job_desc[i])[0][0] for i in range(len(predict_df))]
predict_df['transcript_job_similarity'] = [cosine_similarity(tfidf_transcript[i], tfidf_job_desc[i])[0][0] for i in range(len(predict_df))]

# Prepare features and target variable
features = ['resume_job_similarity', 'transcript_job_similarity']
# If you have a 'decision' column (ground truth), use it.
# Otherwise, you'll need a way to assign labels for training.
# Here, I'm creating a dummy target if you don't have one:
predict_df['decision'] = np.random.choice(['selected', 'rejected'], size=len(predict_df))

# Split data into training and testing sets
X = predict_df[features]
y = predict_df['decision']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize, train, and save the Random Forest model
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
random_forest.fit(X_train, y_train)

# Save the trained models
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(random_forest, f)

# Make predictions on the entire dataset (or a subset)
X_new = predict_df[features]
predictions = random_forest.predict(X_new)
predict_df['predicted_decision'] = predictions

# Display or save the predictions
predict_df[['ID', 'predicted_decision']]
# predict_df.to_excel('predictions_output.xlsx', index=False)

selected_count = predict_df['predicted_decision'].value_counts()['selected']
rejected_count = predict_df['predicted_decision'].value_counts()['rejected']

print(f"Selected: {selected_count}")
print(f"Rejected: {rejected_count}")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials - REPLACE THESE WITH YOUR OWN
sender_email = "uppariupendra@gmail.com"  # Your email address
sender_password = "eseuxrzxutsyjwse"  # App Password from your email account

def send_email(receiver_email, subject, body):
    """
    Sends an email to the given receiver.
    Args:
        receiver_email: Email address of the recipient.
        subject: Subject of the email.
        body: Body text of the email.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login to Gmail
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)  # Send the email
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")

# Example Usage
if __name__ == "__main__":
    receiver_email = "21r21a66k0@mlrinstitutions.ac.in"
    subject = "Congratulations! You're selected for the next round."
    body = """Dear Candidate,

We are pleased to inform you that you have been selected for the next round of the interview process for the Software Engineer role.

Further instructions will be provided shortly.

Sincerely,
[Your Name/Company]
"""
    send_email(receiver_email, subject, body)

import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials - **REPLACE WITH YOUR CREDENTIALS**
sender_email = "uppariupendra@gmail.com"
sender_password = "eseuxrzxutsyjwse"

def send_email(receiver_email, subject, body):
    """Sends an email to the given receiver."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        # Removed server.quit() from here to avoid premature closing
        pass  # or you can handle any necessary cleanup without closing the connection

# Assuming 'predict_df' contains your data
for index, row in predict_df.iterrows():
    resume_text = row['Resume']

    # Extract email using regular expression
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
    if email_match:
        candidate_email = email_match.group(0)
    else:
        print(f"Email not found for ID: {row['ID']}, skipping...")
        continue

    decision = row['predicted_decision']

    if decision == 'selected':
        subject = "Congratulations! You're selected for the next round."
        body = f"Dear {row['Name']},\n\nWe are pleased to inform you that you have been selected for the next round of the interview process for the {row['Role']} role. [Provide further instructions here].\n\nSincerely,\n[Your Name/Company]"
    elif decision == 'rejected':
        subject = "Update on your application"
        body = f"Dear {row['Name']},\n\nThank you for your interest in the {row['Role']} role. We appreciate you taking the time to apply. While your qualifications were impressive, we have decided to move forward with other candidates. We wish you the best in your job search.\n\nSincerely,\n[Your Name/Company]"
    else:
        continue

    send_email(candidate_email, subject, body)


