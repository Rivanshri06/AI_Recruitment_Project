##AI-Driven Recruitment Pipeline

This task is a complete solution created to use AI and data-driven insights to transform hiring procedures. 
From the first candidate screening to the last selection, it effortlessly integrates to automate, optimise, and improve every step of the hiring process.
Important attributes:
AI-Powered Screening: Examine resumes, transcripts, and other applicant data for skill matching and job relevance using cutting-edge natural language processing and machine learning models.
Real-Time Interview Insights: To ensure a deeper comprehension of candidate responses, use sentiment analysis and keyword tracking to offer meaningful comments during interviews.
Cultural Fit Scoring: Use unique scoring algorithms to assess candidates' adherence to company values, encouraging improved teamwork and long-term success.
Data Visualisation: To link important data such as transcript quality, selection results, and resume-job similarities, create clear charts and heatmaps.
Prediciton: Use classification and logistic regression models in predictive analytics to forecast candidate success and enhance decision-making.
Role-Specific Analysis: Personalised suggestions and analysis for different positions, guaranteeing equity and effectiveness in the recruiting procedure.

###The pipeline consists of:

Analysing data to determine how various features relate to one another is known as exploratory data analysis, or EDA.
Model training is the process of using preprocessed data to train a machine learning model (such as XGBoost) to generate predictions.
Resume screening is the process of preprocessing interview transcripts and resumes to extract pertinent information.
Prediction: Making predictions about new resumes and interview transcripts using the trained model.
Emailing the Results: Emailing the designated recipient the prediction results.

###The project cannot be completed without the following Python libraries:

Pandas: For analysing and manipulating data.
For numerical operations, use numpy.
xgboost: For machine learning model training.
scikit-learn: For preprocessing tools and model evaluation.
Seaborn and matplotlib: For visual aids.
For sending emails with attachments, use smtplib, email.
To read and write Excel files, use openpyxl.
pickle: To save and import learnt models.

###Implementation: Feature extraction and preprocessing

Relevant features are extracted from the interview transcripts and resumes by the Resume_screener.py script.

Model Training:
To train a machine learning model on the processed data, run the Training.py script. Pickle is used to preserve the model, which may then be used for future predictions.

Predictions are made by loading the processed data and trained model into the Prediction.py script, which then saves the outcomes in an Excel file. Additionally, it can email the designated recipient the forecast findings.

Exploratory Data Analysis: To examine and display the dataset, run the EDA.py script. This script prepares the data for training and aids in comprehending the connections between various features.


###License
This project is open-source and available under the MIT License.
