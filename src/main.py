import joblib
import mlflow
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from config.configuration import ALL_SELECTED_FEATURES, TARGET
from model.preprocessor import Preprocessor
from utils.dataloader import load_data


def train_model():
    # Load data
    data = load_data()

    # Split data
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=42)

    X_train = train_df[ALL_SELECTED_FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[ALL_SELECTED_FEATURES]
    y_test = test_df[TARGET]

    # Define the model pipeline with XGBoost
    pipeline = Pipeline(
        steps=[
            ("preprocessor", Preprocessor()),
            ("regressor", xgb.XGBRegressor(n_estimators=1500, random_state=42)),
        ]
    )

    # Start an mlflow run
    with mlflow.start_run():
        # Train the model
        pipeline.fit(X_train, y_train)

        # Save the model
        joblib.dump(pipeline, "rental_price_model.pkl")
        mlflow.sklearn.log_model(pipeline, "model")

        # Predict and evaluate on the test set
        y_pred = pipeline.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        # Log the RMSE
        mlflow.log_metric("rmse", rmse)

        # Save test_df as JSON for testing the Flask app using a POST request with curl
        # test_df.drop(columns=TARGET).to_json('test_data.json', orient='records', lines=True)
        test_df.to_json("data/test_data.json", orient="records", lines=True)

        print(
            f"Model training complete and saved to 'rental_price_model.pkl'. RMSE: {rmse}"
        )
        print("Test data saved to 'data/test_data.json'")


if __name__ == "__main__":
    train_model()
