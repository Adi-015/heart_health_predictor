from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def build_preprocessing_pipeline(numeric_features, cat_features):
    """
    Returns a ColumnTransformer pipeline for mixed numeric/categorical data.

    Numeric: median imputation + standard scaling.
    Categorical: most-frequent imputation + one-hot encoding.

    Neither fit nor transform is called here — call pipeline.fit_transform()
    on training data and pipeline.transform() on test data.
    """
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer([
        ("num", numeric_pipe, numeric_features),
        ("cat", cat_pipe, cat_features),
    ])
