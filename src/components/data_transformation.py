# main feature of this code is to do feature engineering, data cleaning

import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # Creates the pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        1. Handling missing values
        2. Scaling the features
        3. Encoding categorical features
        4. Returning the preprocessor object

        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # numerical Pipeline is doing 2 tasks: imputing missing values and scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")), # Helps to fill missing values with median
                    ("scaler", StandardScaler(with_mean=False)) # Doing the standard scaling, implemented 'with_mean=False' to avoid negative values after scaling
                ]
            )
            # categorical Pipeline is doing 3 tasks: imputing missing values, one hot encoding and scaling
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")), # Fill missing values with most frequent
                    ("one_hot_encoder", OneHotEncoder()), # One hot encoding
                    ("scaler", StandardScaler(with_mean=False)) # Scaling
                ]
            )

            logging.info("Categorical and Numerical pipelines created")

            # Combining both categorical and numerical pipelines
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train and Test data completed")
            logging.info("Obtaining preprocessor object")

            # Getting the preprocessor object
            preprocessor_obj = self.get_data_transformer_object()

            # Selecting input and target features
            target_column_name = ["math_score"]
            numerical_columns = ["writing_score", "reading_score"]

            # Dividing into input and target features
            input_feature_train_df = train_df.drop(columns=target_column_name, axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Similarly for test data
            input_feature_test_df = test_df.drop(columns=target_column_name, axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes")

            # Transforming the data using preprocessor object
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            # Combining input features and target feature into a single array
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_df_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object")

            # Saving the preprocessor object
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessor_obj
            )

            # Returning the transformed arrays and preprocessor object path
            return(
                train_arr,
                test_df_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)