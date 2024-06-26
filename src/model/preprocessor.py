import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config.configuration import NUMERIC_FEATURES


def split_tokenizer(text):
    return text.split()


class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = StandardScaler()
        self.vectorizer = CountVectorizer(tokenizer=split_tokenizer, binary=True)
        self.onehot = OneHotEncoder(
            drop="first", sparse_output=False, handle_unknown="ignore"
        )
        self.state_to_region = {
            "AL": "Southeast",
            "AK": "West",
            "AZ": "Southwest",
            "AR": "Southeast",
            "CA": "West",
            "CO": "Southwest",
            "CT": "Northeast",
            "DE": "Southeast",
            "FL": "Southeast",
            "GA": "Southeast",
            "HI": "West",
            "ID": "West",
            "IL": "Midwest",
            "IN": "Midwest",
            "IA": "Midwest",
            "KS": "Midwest",
            "KY": "Southeast",
            "LA": "Southeast",
            "ME": "Northeast",
            "MD": "Southeast",
            "MA": "Northeast",
            "MI": "Midwest",
            "MN": "Midwest",
            "MS": "Southeast",
            "MO": "Midwest",
            "MT": "West",
            "NE": "Midwest",
            "NV": "West",
            "NH": "Northeast",
            "NJ": "Northeast",
            "NM": "Southwest",
            "NY": "Northeast",
            "NC": "Southeast",
            "ND": "Midwest",
            "OH": "Midwest",
            "OK": "Southwest",
            "OR": "West",
            "PA": "Northeast",
            "RI": "Northeast",
            "SC": "Southeast",
            "SD": "Midwest",
            "TN": "Southeast",
            "TX": "Southwest",
            "UT": "West",
            "VT": "Northeast",
            "VA": "Southeast",
            "WA": "West",
            "WV": "Southeast",
            "WI": "Midwest",
            "WY": "West",
            "DC": "Southeast",
        }

    def fit(self, X, y=None):

        # Fit vectorizer on amenities
        amenities_str = (
            X["amenities"].fillna("").apply(lambda x: " ".join(x.split(",")))
        )
        self.vectorizer.fit(amenities_str)

        # Fit scaler on numerical features
        self.scaler.fit(X[NUMERIC_FEATURES])

        # Fit onehot encoder on categorical features
        X = self._feature_engineering_state(X)
        self.onehot.fit(X[["region"]])

        return self

    def transform(self, X):
        # Apply all preprocessing steps
        X = self._feature_engineering_state(X)
        X = self._feature_engineering_amenities(X)
        X = self._feature_engineering_time(X)

        # Scale numerical features
        X[NUMERIC_FEATURES] = self.scaler.transform(X[NUMERIC_FEATURES])

        # One-hot encode categorical features
        onehot_encoded = self.onehot.transform(X[["region"]])
        onehot_encoded_df = pd.DataFrame(
            onehot_encoded, columns=self.onehot.get_feature_names_out(["region"])
        )
        X = pd.concat(
            [X.reset_index(drop=True), onehot_encoded_df.reset_index(drop=True)], axis=1
        ).drop(columns=["region"])

        return X

    def _feature_engineering_state(self, df):
        # Map state to region
        df["region"] = df["state"].map(self.state_to_region)
        return df.drop(columns=["state"])

    def _feature_engineering_amenities(self, df):
        # Convert amenities to binary feature matrix
        df["amenities"] = df["amenities"].fillna("")
        amenities_str = df["amenities"].apply(lambda x: " ".join(x.split(",")))
        amenities_matrix = self.vectorizer.transform(amenities_str)
        amenities_df = pd.DataFrame(
            amenities_matrix.toarray(), columns=self.vectorizer.get_feature_names_out()
        )
        return pd.concat(
            [df.reset_index(drop=True), amenities_df.reset_index(drop=True)], axis=1
        ).drop(columns=["amenities"])

    def _feature_engineering_time(self, df):
        # Extract datetime features
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df["year"] = df["time"].dt.year
        df["month"] = df["time"].dt.month
        df["day"] = df["time"].dt.day
        df["day_of_year"] = df["time"].dt.dayofyear
        df["week_of_year"] = df["time"].dt.isocalendar().week
        return df.drop(columns=["time"])
