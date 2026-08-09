# ============================================================
# TELCO CUSTOMER CHURN - DATA CLEANING & ANALYSIS
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
# 2. FIND THE EXCEL DATASET
# ============================================================

excel_files = list(DATA_FOLDER.glob("*.xlsx"))

if not excel_files:
    raise FileNotFoundError(
        "No Excel (.xlsx) file was found inside the 'data' folder."
    )

INPUT_FILE = excel_files[0]

print("=" * 70)
print("TELCO CUSTOMER CHURN ANALYSIS")
print("=" * 70)

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

print("\n" + "=" * 70)
print("INITIAL DATA INSPECTION")
print("=" * 70)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ============================================================
# 5. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing_values = df.isnull().sum()
missing_only = missing_values[missing_values > 0]

if len(missing_only) == 0:
    print("\nNo missing values found.")
else:
    print("\nMissing values by column:")
    print(missing_only)

print(f"\nTotal missing values: {missing_values.sum()}")


# ============================================================
# 6. CONVERT TOTAL CHARGES TO NUMERIC
# ============================================================

if "Total Charges" in df.columns:

    print("\nChecking Total Charges...")

    df["Total Charges"] = pd.to_numeric(
        df["Total Charges"],
        errors="coerce"
    )

    total_charges_missing = df["Total Charges"].isnull().sum()

    print(
        f"Missing Total Charges after conversion: "
        f"{total_charges_missing}"
    )

    if total_charges_missing > 0:

        median_value = df["Total Charges"].median()

        df["Total Charges"] = df["Total Charges"].fillna(
            median_value
        )

        print(
            "Missing Total Charges values were "
            "filled using the median."
        )


# ============================================================
# 7. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

if duplicate_count > 0:

    df = df.drop_duplicates()

    print("Duplicate rows removed.")

else:

    print("No duplicate rows found.")


# ============================================================
# 8. IMPORTANT COLUMN CHECK
# ============================================================

print("\n" + "=" * 70)
print("IMPORTANT COLUMN CHECK")
print("=" * 70)

important_columns = [
    "Gender",
    "Senior Citizen",
    "Partner",
    "Dependents",
    "Contract",
    "Internet Service",
    "Payment Method",
    "Churn Label"
]

for column in important_columns:

    if column in df.columns:

        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False))


# ============================================================
# 9. NUMERICAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("NUMERICAL SUMMARY")
print("=" * 70)

print(df.describe())


# ============================================================
# 10. OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("OUTLIER ANALYSIS")
print("=" * 70)

numeric_columns = [
    "Tenure Months",
    "Monthly Charges",
    "Total Charges",
    "Churn Score",
    "CLTV"
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

print("\n" + "=" * 70)
print("CHURN SUMMARY")
print("=" * 70)

if "Churn Label" in df.columns:

    churn_counts = df["Churn Label"].value_counts()

    churn_percentages = (
        df["Churn Label"]
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

if "Contract" in df.columns and "Churn Label" in df.columns:

    contract_churn = pd.crosstab(
        df["Contract"],
        df["Churn Label"],
        normalize="index"
    ) * 100

    print("\n" + "=" * 70)
    print("CHURN RATE BY CONTRACT")
    print("=" * 70)

    print(contract_churn.round(2))


# ============================================================
# 13. CHURN RATE BY INTERNET SERVICE
# ============================================================

if "Internet Service" in df.columns and "Churn Label" in df.columns:

    internet_churn = pd.crosstab(
        df["Internet Service"],
        df["Churn Label"],
        normalize="index"
    ) * 100

    print("\n" + "=" * 70)
    print("CHURN RATE BY INTERNET SERVICE")
    print("=" * 70)

    print(internet_churn.round(2))


# ============================================================
# 14. VISUALIZATION - CHURN DISTRIBUTION
# ============================================================

if "Churn Label" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="Churn Label"
    )

    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "01_churn_distribution.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 15. VISUALIZATION - CHURN BY CONTRACT
# ============================================================

if "Contract" in df.columns and "Churn Label" in df.columns:

    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=df,
        x="Contract",
        hue="Churn Label"
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

    plt.close()


# ============================================================
# 16. VISUALIZATION - TENURE BY CHURN
# ============================================================

if "Tenure Months" in df.columns and "Churn Label" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Churn Label",
        y="Tenure Months"
    )

    plt.title("Tenure Distribution by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Tenure (Months)")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "03_tenure_by_churn.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 17. VISUALIZATION - MONTHLY CHARGES BY CHURN
# ============================================================

if "Monthly Charges" in df.columns and "Churn Label" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Churn Label",
        y="Monthly Charges"
    )

    plt.title("Monthly Charges by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Monthly Charges")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "04_monthly_charges_by_churn.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 18. VISUALIZATION - INTERNET SERVICE BY CHURN
# ============================================================

if "Internet Service" in df.columns and "Churn Label" in df.columns:

    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=df,
        x="Internet Service",
        hue="Churn Label"
    )

    plt.title("Customer Churn by Internet Service")
    plt.xlabel("Internet Service")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "05_churn_by_internet_service.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 19. VISUALIZATION - CORRELATION HEATMAP
# ============================================================

numeric_df = df.select_dtypes(include="number")

if numeric_df.shape[1] >= 2:

    plt.figure(figsize=(12, 8))

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

    plt.close()


# ============================================================
# 20. SAVE CLEANED DATASET
# ============================================================

cleaned_file = DATA_FOLDER / "Telco_Customer_Churn_Cleaned.csv"

df.to_csv(
    cleaned_file,
    index=False
)

print("\n" + "=" * 70)
print("CLEANED DATASET SAVED")
print("=" * 70)

print(cleaned_file)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)

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

print("\nTelco Customer Churn Analysis completed successfully.")