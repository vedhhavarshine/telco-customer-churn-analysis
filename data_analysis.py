# ============================================================
# TELCO CUSTOMER CHURN - DATA CLEANING & VISUALIZATION
# ============================================================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"
OUTPUT_FOLDER = PROJECT_FOLDER / "visualizations"

OUTPUT_FOLDER.mkdir(exist_ok=True)


# ============================================================
# 2. FIND THE EXCEL DATASET AUTOMATICALLY
# ============================================================

excel_files = list(DATA_FOLDER.glob("*.xlsx"))

if len(excel_files) == 0:
    raise FileNotFoundError(
        "No .xlsx Excel file was found inside the 'data' folder."
    )

INPUT_FILE = excel_files[0]

print("=" * 60)
print("TELCO CUSTOMER CHURN ANALYSIS")
print("=" * 60)

print("\nExcel file found:")
print(INPUT_FILE)


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_excel(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ============================================================
# 4. INITIAL DATA INSPECTION
# ============================================================

print("\n" + "=" * 60)
print("INITIAL DATA INSPECTION")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ============================================================
# 5. MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUE ANALYSIS")
print("=" * 60)

missing_values = df.isnull().sum()

print("\nMissing values by column:")

missing_only = missing_values[missing_values > 0]

if len(missing_only) == 0:
    print("No missing values found.")
else:
    print(missing_only)

print(f"\nTotal missing values: {missing_values.sum()}")


# ============================================================
# 6. CONVERT TOTALCHARGES TO NUMERIC
# ============================================================

if "TotalCharges" in df.columns:

    print("\nChecking TotalCharges...")

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    totalcharges_missing = df["TotalCharges"].isnull().sum()

    print(
        f"Missing TotalCharges after conversion: "
        f"{totalcharges_missing}"
    )

    if totalcharges_missing > 0:

        median_value = df["TotalCharges"].median()

        df["TotalCharges"] = df["TotalCharges"].fillna(
            median_value
        )

        print(
            "Missing TotalCharges values were "
            "filled using the median."
        )


# ============================================================
# 7. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE ANALYSIS")
print("=" * 60)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

if duplicate_count > 0:

    df = df.drop_duplicates()

    print("Duplicate rows removed.")

else:

    print("No duplicate rows found.")


# ============================================================
# 8. CHECK IMPORTANT COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("IMPORTANT COLUMN CHECK")
print("=" * 60)

important_columns = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "Churn"
]

for column in important_columns:

    if column in df.columns:

        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False))


# ============================================================
# 9. NUMERICAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("NUMERICAL SUMMARY")
print("=" * 60)

print(df.describe())


# ============================================================
# 10. OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("OUTLIER ANALYSIS")
print("=" * 60)

numeric_columns = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

for column in numeric_columns:

    if column in df.columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_count = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        ).sum()

        print(
            f"{column}: "
            f"{outlier_count} potential outliers"
        )


# ============================================================
# 11. CHURN SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CHURN SUMMARY")
print("=" * 60)

if "Churn" in df.columns:

    churn_counts = df["Churn"].value_counts()

    churn_percentages = (
        df["Churn"]
        .value_counts(normalize=True)
        * 100
    )

    print("\nCustomer count by churn:")
    print(churn_counts)

    print("\nCustomer percentage by churn:")
    print(churn_percentages.round(2))


# ============================================================
# 12. CHURN RATE BY CONTRACT
# ============================================================

if "Contract" in df.columns and "Churn" in df.columns:

    contract_churn = pd.crosstab(
        df["Contract"],
        df["Churn"],
        normalize="index"
    ) * 100

    print("\n" + "=" * 60)
    print("CHURN RATE BY CONTRACT")
    print("=" * 60)

    print(contract_churn.round(2))


# ============================================================
# 13. CHURN RATE BY INTERNET SERVICE
# ============================================================

if "InternetService" in df.columns and "Churn" in df.columns:

    internet_churn = pd.crosstab(
        df["InternetService"],
        df["Churn"],
        normalize="index"
    ) * 100

    print("\n" + "=" * 60)
    print("CHURN RATE BY INTERNET SERVICE")
    print("=" * 60)

    print(internet_churn.round(2))


# ============================================================
# 14. VISUALIZATION - CHURN DISTRIBUTION
# ============================================================

if "Churn" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="Churn"
    )

    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "01_churn_distribution.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 15. VISUALIZATION - CHURN BY CONTRACT
# ============================================================

if "Contract" in df.columns and "Churn" in df.columns:

    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=df,
        x="Contract",
        hue="Churn"
    )

    plt.title("Customer Churn by Contract Type")
    plt.xlabel("Contract Type")
    plt.ylabel("Number of Customers")

    plt.xticks(rotation=15)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "02_churn_by_contract.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 16. VISUALIZATION - TENURE BY CHURN
# ============================================================

if "tenure" in df.columns and "Churn" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="tenure"
    )

    plt.title("Tenure Distribution by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Tenure (Months)")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "03_tenure_by_churn.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 17. VISUALIZATION - MONTHLY CHARGES BY CHURN
# ============================================================

if "MonthlyCharges" in df.columns and "Churn" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="MonthlyCharges"
    )

    plt.title("Monthly Charges by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Monthly Charges")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "04_monthly_charges_by_churn.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 18. VISUALIZATION - INTERNET SERVICE BY CHURN
# ============================================================

if "InternetService" in df.columns and "Churn" in df.columns:

    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=df,
        x="InternetService",
        hue="Churn"
    )

    plt.title("Customer Churn by Internet Service")
    plt.xlabel("Internet Service")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "05_churn_by_internet_service.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 19. VISUALIZATION - CORRELATION HEATMAP
# ============================================================

numeric_df = df.select_dtypes(include="number")

if numeric_df.shape[1] >= 2:

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "06_correlation_heatmap.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 20. SAVE CLEANED DATASET
# ============================================================

cleaned_file = DATA_FOLDER / "Telco_Customer_Churn_Cleaned.csv"

df.to_csv(
    cleaned_file,
    index=False
)

print("\n" + "=" * 60)
print("CLEANED DATASET SAVED")
print("=" * 60)

print(cleaned_file)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Final rows: {df.shape[0]}")
print(f"Final columns: {df.shape[1]}")

print("\nCleaned dataset:")
print(cleaned_file)

print("\nVisualization folder:")
print(OUTPUT_FOLDER)

print("\nGenerated visualization files:")

for file in sorted(OUTPUT_FOLDER.iterdir()):

    if file.is_file():
        print(f" - {file.name}")

print("\nTelco Customer Churn Analysis completed.")