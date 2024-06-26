# Apartment for Rent Price Predictor

This project builds prototype of a rent price recommender for properties added in the classifieds portal. The recommender takes inputs from the renter and recommends an ideal rent price.

## ML Project Lifecycle

### Scoping

A regression problem with `price` as target.

### Data

A dataset of classified for apartments for rent in USA.
[Link](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified)

There are data quality issues need to be fixed first. Handled in

[src/utils/dataloader.py](src/utils/dataloader.py)

Data quality issue examples:

- some column types are not correct
- some categorical values are not correct or rare
- some columns contain missing value including `price`
- some numerical columns have extreme outliers like `price` and `square_feet`
- `price`, `bedrooms` can be not accurate according to property description `body`.
  e.g. Index 99824
- studio have `bedrooms` 1 or 0.

### Modeling

After experiments, considering both accuracy on RMSE and running time, **XGBoost** (n_estimators=1500) is the best performed model chosen for production.

Model and model performance during training phase are logged with MLflow. See in [src/main.py](src/main.py)

### Deployment

The model is served with a Flask app which takes in the user input as a POST request with `curl`.

### Feedback loop and continuous improvement

1. **User Feedback Collection**:

   - When users input property information, the model generates a recommended rent price.
   - Allow users to adjust the recommended price based on their expectations or market insights.
   - Collect the user-modified rent price as feedback to gauge the model's performance.

1. **Performance Evaluation**:

   - Apply statistical tests such as the paired t-test to compare the model's predictions against the user-adjusted prices.
   - Assess if there are significant differences between the predicted and adjusted prices.

1. **Model Improvement**:

   - **Retraining**: Regularly retrain the model with new data that includes user-adjusted prices to improve its accuracy and relevance.
   - **Residual Learning**: Train a secondary model to predict the residuals (the differences between predicted and actual prices). Integrate this model to adjust the primary model's predictions, effectively reducing the prediction error over time.

**Implementation Steps**

1. **Data Collection**:

   - Store both the initial model predictions and the user-adjusted prices in a database.
   - Ensure proper data handling and privacy measures are in place.

1. **Statistical Analysis**:

   - Periodically perform paired t-tests or other relevant statistical analyses to evaluate model performance.
   - Use the insights gained to identify patterns or biases in the model's predictions.

1. **Model Retraining**:

   - Set up a pipeline for regular model retraining using the latest collected data.
   - Use version control for the models to track improvements and changes over time.

1. **Residual Model Integration**:

   - Develop a residual model to learn from the differences between the predicted and adjusted prices.
   - Combine the predictions from both the primary and residual models to provide more accurate recommendations. Can consider using advanced ensemble methods like stacking, where the primary model and residual model predictions are combined using another model to improve overall accuracy.

## Project Directory Structure

```
apartment-for-rent/
├── notebooks/                     # Jupyter notebooks for exploration and experimentation
├── data/                          # Directory for storing datasets
│   └── test_data.json             # Sample test data in JSON format
├── src/                           # Source code directory
│   ├── config/                    # Configuration files
│   │   └── configuration.py       # Configuration settings
│   ├── model/                     # Model-related code
│   │   └── preprocessor.py        # Data preprocessing class
│   ├── utils/                     # Utility scripts
│   │   └── dataloader.py          # Data loading utilities
│   └── main.py                    # Main script to train and save the model
├── app.py                         # Flask application for serving the model
├── rental_price_model.pkl         # Serialized model file
├── run_app_and_test.sh            # Script to run the Flask app and test it
├── poetry.lock                    # Poetry lock file for dependencies
├── pyproject.toml                 # Poetry configuration file
├── Dockerfile                     # Instructions to build a Docker image
├── .pre-commit-config.yaml        # Configuration for pre-commit hooks
└── README.md                      # Project documentation
```

## Feature Engineering

The features used are listed in [src/config/configuration.py](src/config/configuration.py)

```
OTHER_FEATURES = ['amenities', 'time']
CATEGORICAL_FEATURES = ['state']
NUMERIC_FEATURES = ['bathrooms', 'bedrooms', 'square_feet', 'latitude', 'longitude']
```

To build a proper application, features from other or external dataset might be helpful, such as per each state/city

- population
- average income
- cost of living index
- number of current available properties for rent
- search frequency

Feature engineering is done in [src/model/preprocessor.py](src/model/preprocessor.py).

Feature importance can be viewed in [notebooks/4_feature_importance.ipynb](notebooks/4_feature_importance.ipynb).

Detailed explanations regarding some features are as below.

**state**

- Region Grouping: A common way of referring to regions in the United States is grouping them into 5 regions according to their geographic position on the continent: the Northeast, Southwest, West, Southeast, and Midwest. [Ref.](https://education.nationalgeographic.org/resource/united-states-regions/)

**amenities**

- Vectorizing to binary feature matrix

**time**

- Unix timestamp `time` will be transformed into 5 other features: 'year', 'month', 'day', 'day_of_year', 'week_of_year'.

## Usage

### Poetry

Poetry is used for dependency management and packaging.

1. **Install Poetry**: Follow the instructions [here](https://python-poetry.org/docs/#installation).
1. **Install Dependencies**: Run the following command to install dependencies:
   ```bash
   poetry install
   ```
1. **Train the model**: Use Poetry to train the model.
   ```bash
   poetry run python src/main.py
   ```

### MLflow

MLflow is used for tracking experiments, logging metrics, and saving models.

**Run MLflow UI**: Start the MLflow UI to visualize experiments.

```bash
poetry run mlflow ui
```

The UI will be accessible at `http://127.0.0.1:5000` to view logged metrics and models.

### Flask App

The Flask app serves the rent price recommender model. The command to run the Flask app and test endpoint is in a shell script [run_app_and_test.sh](run_app_and_test.sh)

1. Make sure the script is executable
   ```bash
   chmod +x run_app_and_test.sh
   ```
1. Run the script with:
   ```bash
   ./run_app_and_test.sh
   ```
   This script will start the Flask app, send a test request, and then stop the Flask app. You can change the json data input for POST request in this file by referring to [data/test_data.json](data/test_data.json).

### Pre-commit

Pre-commit hooks are used to ensure code quality and consistency before committing changes.

1. **Install pre-commit**: Ensure pre-commit is installed via Poetry.
   ```bash
   poetry add pre-commit --dev
   ```
1. **Install Git Hooks**: Install the pre-commit hooks.
   ```bash
   poetry run pre-commit install
   ```
1. **Run Pre-commit Hooks**: Manually run pre-commit hooks on all files.
   ```bash
   poetry run pre-commit run --all-files
   ```

## License

This project is licensed under the MIT License.
Feel free to customize this `README.md` as per your project details and requirements.
