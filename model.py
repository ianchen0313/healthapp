import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('clean_data.csv')
seed = 20230626
y = df['是否有腎臟病 (Y)']
X = df[['是否有高血壓', '是否有高血脂', '是否有糖尿病', '是否有骨質疏鬆症', '是否有肝臟疾病', '是否有子宮卵巢疾病',
       '是否關節疼痛', '是否下背部疼痛或腰痛', '是否坐骨神經痛', '是否頭痛或偏頭痛', '是否痛風', '是否使用慢性處方籤',
       '是否曾吸菸', '年齡']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=seed)

def log_model():    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling step
        ('classifier', LogisticRegression(C=0.0033, n_jobs=-1, solver='saga', max_iter=100000, class_weight='balanced', penalty='l2'))  # Model training step
    ])
    
    # Fit the pipeline on the training data
    pipeline.fit(X_train, y_train)

    # Make predictions with the trained pipeline
    y_pred = pipeline.predict(X_test)
    
    return pipeline

def rf_model():    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling step
        ('classifier', RandomForestClassifier(class_weight='balanced', n_jobs= -1, random_state=True,max_depth=1, n_estimators=150))])
    
    X_train_sub = X_train[['是否使用慢性處方籤', '年齡', '是否有高血壓', '是否有糖尿病']]
    X_test_sub = X_test[['是否使用慢性處方籤', '年齡', '是否有高血壓', '是否有糖尿病']]
    
    # Fit the pipeline on the training data
    pipeline.fit(X_train_sub, y_train)

    # Make predictions with the trained pipeline
    y_pred = pipeline.predict(X_test_sub)
    
    return pipeline

from sklearn.ensemble import VotingClassifier
def final_model():
    models = [('logreg', log_model()), ('rf', rf_model())]
    voting_clf = VotingClassifier(estimators=models, voting='soft')
    voting_clf.fit(X_train, y_train)
    y_pred = voting_clf.predict(X_test)
    #metic_evaluation(y_test, y_pred)
    y_prob = voting_clf.predict_proba(X_test)
    return voting_clf

final_model = final_model()
