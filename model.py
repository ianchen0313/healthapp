import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('clean_data2.csv')
seed = 20230626
y = df['是否有腎臟病 (Y)']
X = df[['是否有同居伴侶', '和去年比較之健康狀況', '是否有高血壓', '是否有高血脂', '是否有心臟病', '是否有糖尿病',
       '是否有骨質疏鬆症', '是否有胃潰瘍或十二指腸潰瘍', '是否有肝臟疾病', '是否有子宮卵巢疾病', '是否關節疼痛',
       '是否下背部疼痛或腰痛', '是否坐骨神經痛', '是否頭痛或偏頭痛', '是否痛風', '是否使用慢性處方籤', '是否曾吸菸',
       '是否曾嚼食檳榔', '平均每週幾天吃水果', '年齡', 'bmi', '失業中']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=seed)


def log_model():    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling step
        ('classifier', LogisticRegression(solver='liblinear', max_iter=100000, class_weight='balanced', penalty='l1', C=0.0033))  # Model training step
    ])
    
    # Fit the pipeline on the training data
    pipeline.fit(X_train, y_train)

    # Make predictions with the trained pipeline
    y_pred = pipeline.predict(X_test)
    
    return pipeline

def rf_model():    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling step
        ('classifier', RandomForestClassifier(class_weight='balanced', n_jobs= -1, random_state=True,max_depth=3, n_estimators=150))])
    
    X_train_sub = X_train[['年齡', '是否使用慢性處方籤', '是否有高血壓', '是否有心臟病']]
    X_test_sub = X_test[['年齡', '是否使用慢性處方籤', '是否有高血壓', '是否有心臟病']]
    
    # Fit the pipeline on the training data
    pipeline.fit(X_train_sub, y_train)

    # Make predictions with the trained pipeline
    y_pred = pipeline.predict(X_test_sub)
    
    return pipeline

from sklearn.svm import LinearSVC

def svc_model():
    # Split the data into training and testing sets
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling step
        ('classifier', LinearSVC(class_weight = 'balanced', penalty='l1', dual=False,C=0.0005))])



    X_train_sub = X_train[['是否有同居伴侶', '和去年比較之健康狀況', '是否有高血壓', '是否有高血脂', '是否有心臟病', '是否有骨質疏鬆症',
       '是否有肝臟疾病', '是否有子宮卵巢疾病', '是否關節疼痛', '是否下背部疼痛或腰痛', '是否頭痛或偏頭痛', '是否痛風',
       '是否使用慢性處方籤', '是否曾吸菸', '是否曾嚼食檳榔', '平均每週幾天吃水果', '年齡']]
    X_test_sub = X_test[['是否有同居伴侶', '和去年比較之健康狀況', '是否有高血壓', '是否有高血脂', '是否有心臟病', '是否有骨質疏鬆症',
       '是否有肝臟疾病', '是否有子宮卵巢疾病', '是否關節疼痛', '是否下背部疼痛或腰痛', '是否頭痛或偏頭痛', '是否痛風',
       '是否使用慢性處方籤', '是否曾吸菸', '是否曾嚼食檳榔', '平均每週幾天吃水果', '年齡']]
    
    # Fit the pipeline on the training data
    pipeline.fit(X_train_sub, y_train)

    # Make predictions with the trained pipeline
    y_pred = pipeline.predict(X_test_sub)
    
    
    return pipeline

from sklearn.ensemble import VotingClassifier
def final_model():
    models = [('logreg', log_model()), ('rf', rf_model()), ('svc', svc_model())]
    voting_clf = VotingClassifier(estimators=models, voting='hard')
    voting_clf.fit(X_train, y_train)
    y_pred = voting_clf.predict(X_test)
    

    return voting_clf

final_model = final_model()
