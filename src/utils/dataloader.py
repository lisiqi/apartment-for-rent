import pandas as pd
from ucimlrepo import fetch_ucirepo

from config.configuration import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
)


def load_data():
    # fetch dataset
    apartment_for_rent_classified = fetch_ucirepo(id=555)

    # data (as pandas dataframes)
    df = apartment_for_rent_classified.data.features

    df = _select_quality_data(df)

    return df


def _select_quality_data(df):
    """
    Select only good quality data from the raw dataset.
    This should be done on the data engineering side when ingesting dataset to comsumption layer.
    """

    # Correct data type
    cols_to_numeric = ["bathrooms", "bedrooms", "price_display", "square_feet"]
    df[cols_to_numeric] = df[cols_to_numeric].apply(pd.to_numeric, errors="coerce")

    # Remove the rows where the count of category value is very low (<=100)
    cols_to_filter = [
        "category",
        "currency",
        "fee",
        "has_photo",
        "pets_allowed",
        "price_type",
    ]
    for col in cols_to_filter:
        df = _remove_rows_low_cat_value(df, col)

    # Remove rows with NaNs in specified columns
    df = df.dropna(subset=TARGET + NUMERIC_FEATURES + CATEGORICAL_FEATURES)

    # Filter out extreme outliers for specific columns
    df = df[df["price"] <= df["price"].quantile(0.99)]
    df = df[df["square_feet"] <= df["square_feet"].quantile(0.99)]

    return df


def _remove_rows_low_cat_value(df, col):
    """
    Function to remove the rows where the count of category value is very low (<=100)
    """

    # Step 1: Get the value counts
    value_counts = df[col].value_counts(dropna=False)

    # Step 2: Identify values with small counts (e.g., counts less than or equal to 100)
    small_count_values = value_counts[value_counts <= 100].index

    # Step 3: Filter out the rows with small count values
    df = df[~df[col].isin(small_count_values)]

    return df
