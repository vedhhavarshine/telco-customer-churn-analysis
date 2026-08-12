# Telco Customer Churn Analysis

## Project Overview

This project analyzes customer churn data to identify patterns and factors associated with customer attrition.

The analysis uses Python to explore customer demographics, services, contract types, tenure, monthly charges, and other factors related to customer churn.

## Dataset

The dataset contains customer-level information including:

- Customer demographics
- Customer services
- Contract information
- Tenure
- Monthly charges
- Total charges
- Churn information

## Data Analysis

The project performs:

- Data inspection
- Missing-value analysis
- Data type conversion
- Duplicate detection and removal
- Numerical summary
- Outlier analysis
- Churn analysis
- Churn analysis by contract
- Churn analysis by internet service

## Visualizations

The project generates six visualizations:

1. Customer Churn Distribution
2. Customer Churn by Contract Type
3. Tenure Distribution by Churn
4. Monthly Charges by Churn
5. Customer Churn by Internet Service
6. Correlation Heatmap

## Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Microsoft Excel
- Git
- GitHub

## Project Structure

```text
telco-customer-churn-analysis/
│
├── data/
├── visualizations/
├── data_analysis.py
├── .gitignore
└── README.md

# Week 2 - Predictive Modeling Using Machine Learning

## Project Overview

This week focuses on building machine learning models to predict customer churn using the Telco Customer Churn dataset.

## Objective

The objective is to apply supervised machine learning algorithms and evaluate their performance in predicting customer churn.

## Machine Learning Models

- Decision Tree Classifier
- Random Forest Classifier

## Workflow

- Loaded the Telco Customer Churn dataset
- Prepared and cleaned the data
- Handled missing values and duplicate records
- Prepared the churn target variable
- Separated features and target
- Split the data into training and testing sets
- Encoded categorical features
- Trained Decision Tree and Random Forest models
- Evaluated model performance
- Compared the machine learning models

## Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- ROC Curve

## Visualizations

The Week 2 project generated:

- Decision Tree Confusion Matrix
- Random Forest Confusion Matrix
- ROC Curve
- Model Performance Comparison
- Feature Importance

## Files

- `predictive_modeling.py` — Machine learning implementation
- `week2_predictive_modeling.ipynb` — Notebook containing the predictive modeling workflow
- `visualization_week2/` — Machine learning evaluation visualizations

## Conclusion

The project provided practical experience in supervised learning, model training, model evaluation, and visualization of machine learning performance for customer churn prediction.