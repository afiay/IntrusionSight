# model_training.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, explained_variance_score
import numpy as np

# Assuming you have a function in data_preprocessing.py that properly loads and preprocesses the data,
# including the new features.
from data_preprocessing import load_data, preprocess_data, get_features_labels


def train_and_evaluate():
    # Load and preprocess the data
    df = load_data()  # Make sure this path is correct
    # Ensure preprocess_data now calculates and includes the new features
    df = preprocess_data(df)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = get_features_labels(df)

    # Instantiate and train the model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    evs = explained_variance_score(y_test, predictions)

    # Print evaluation metrics
    print(f"Model MSE: {mse}")
    print(f"Model RMSE: {rmse}")
    print(f"Model MAE: {mae}")
    print(f"Model R-squared: {r2}")
    print(f"Model Explained Variance Score: {evs}")


# Save the trained model to a file only if it doesn't already exist
# model_filename = 'saved_model.pkl'
# if not os.path.exists(model_filename):
#     dump(model, model_filename)
#     print(f"Model saved to {model_filename}")
# else:
#    print(f"Model file {model_filename} already exists. Skipping save.")

if __name__ == '__main__':
    train_and_evaluate()
