import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

plt.style.use('ggplot')


def load_data(csv_file):
    """Load and validate the CSV dataset."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Dataset not found: {csv_file}. Please ensure the file exists in the working directory.")

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")

    if 'Attack_Type' not in df.columns:
        raise ValueError("Dataset must contain 'Attack_Type' column")

    print(f"\nDataset columns: {list(df.columns)}")
    return df


def engineer_features(data):
    df_feat = data.copy()
    df_feat['Attack_Type'] = df_feat['Attack_Type'].apply(
        lambda x: 'Cross-site Scripting (XSS)' if str(x).strip() == 'Cross-site Scripting (XSS)' else 'Other'
    )

    numeric_features = ['Severity', 'Damage_Estimate(USD)', 'Affected_Systems']
    for feature in numeric_features:
        if feature not in df_feat.columns:
            raise ValueError(f"Required column missing: {feature}")
        df_feat[feature] = pd.to_numeric(df_feat[feature], errors='coerce')

    df_feat = df_feat.dropna(subset=numeric_features + ['Attack_Type'])

    X = df_feat[numeric_features]
    y = df_feat['Attack_Type']

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder


def plot_confusion_matrix(cm, labels, file_name='confusion_matrix.png'):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()


def plot_feature_importance(importances, feature_names, file_name='feature_importances.png'):
    importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    importance_df = importance_df.sort_values('importance', ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='importance', y='feature', data=importance_df, palette='viridis')
    plt.title('Random Forest Feature Importances')
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()


def main(csv_file='cyber_attacks_dataset.csv'):
    print(f"Loading dataset from: {csv_file}")
    df = load_data(csv_file)

    print(f"\nUnique Attack Types before grouping: {df['Attack_Type'].unique()}")
    df_filtered = df.copy()
    df_filtered['Attack_Type'] = df_filtered['Attack_Type'].apply(
        lambda x: 'Cross-site Scripting (XSS)' if str(x).strip() == 'Cross-site Scripting (XSS)' else 'Other'
    )

    print(f"\nUnique Attack Types after grouping: {df_filtered['Attack_Type'].unique()}")
    print("\nClass Distribution:")
    print(df_filtered['Attack_Type'].value_counts())

    X, y, label_encoder = engineer_features(df_filtered)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(cm, label_encoder.classes_)
    print("Saved confusion matrix to confusion_matrix.png")

    plot_feature_importance(model.feature_importances_, X.columns.tolist())
    print("Saved feature importances to feature_importances.png")


if __name__ == '__main__':
    import sys

    dataset = sys.argv[1] if len(sys.argv) > 1 else 'cyber_attacks_dataset.csv'
    main(dataset)
