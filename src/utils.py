# Has the common functionalities that the entire project can use
import os
import sys
import dill
import numpy as np
import pandas as pd
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.logger import logging

def save_object(file_path, obj):
    '''
    Save a Python object to a file using dill as a pickle file.

    Parameters:
    file_path (str): The path where the object should be saved.
    obj: The Python object to be saved.
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i] # Getting every model
            para = params[list(models.keys())[i]]
            
            grid_search = GridSearchCV(model, para, cv=3)
            grid_search.fit(X_train, y_train)
            
            model.set_params(**grid_search.best_params_)
            model.fit(X_train, y_train)
            #model.fit(X_train, y_train) # Train the model
            
            y_train_pred = model.predict(X_train)
            
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            
            test_model_score = r2_score(y_test, y_test_pred)
            
            logging.info(
                f"Model: {model} | "
                f"Train R2: {train_model_score:.2f} |"
                f"Test R2: {test_model_score:.2f} |"
                f"Best Params: {grid_search.best_params_}"
            )
            
            report[list(models.keys())[i]] = test_model_score
        
        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)