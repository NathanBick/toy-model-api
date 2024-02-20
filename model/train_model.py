# train model 
# target variable is MEDV, we will use all other variables as features for this toy model
# we will use sklearn to do a simple linear regression
# we will use ml flow to log the model and the performance metrics

import mlflow
import pickle

from azureml.core import Workspace
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# globals
TEST_SIZE = 0.2
RANDOM_STATE = 42

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

# Set MLflow tracking URI
mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
mlflow.set_tracking_uri(mlflow_tracking_uri)

# authenticate to azure
ws = Workspace.from_config()

# load data
data = pd.read_csv("data/boston.csv")

# split data
X = data.drop("MEDV", axis=1)
y = data["MEDV"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

# start mlflow run
# note that our ML workspace is public
RUN_NAME = "train_toy_model" 
mlflow.start_run(run_name=RUN_NAME)

print("MLflow run_id:", mlflow.active_run().info.run_id)
print(RUN_NAME)

# log parameters
mlflow.log_param("test_size", TEST_SIZE)
mlflow.log_param("random_state", RANDOM_STATE)

# log data
mlflow.log_artifact(local_path="data/boston.csv")

# train model
model = LinearRegression()
model.fit(X_train, y_train)

# log model
mlflow.sklearn.log_model(model, "toy_model")

# evaluate model using mlflow
y_pred = model.predict(X_test)
mse = ((y_pred - y_test) ** 2).mean()
r2 = model.score(X_test, y_test)
mlflow.log_metric("mse", mse)
mlflow.log_metric("r2", r2)

# end mlflow run
mlflow.end_run()

# save the model in pickle format
pickle.dump (model, open("toy_model.pkl", "wb"))
