# ============================================================
# HOTEL BUSINESS ANALYSIS - EDA
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------

sns.set_theme(style="whitegrid")

os.makedirs("outputs", exist_ok=True)

# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/Hotel_Business_Project/data/hotel_bookings_data.csv")

print("=" * 70)
print("HOTEL BUSINESS ANALYSIS")
print("=" * 70)

print("\nDataset loaded successfully!")

# ------------------------------------------------------------
# 3. DATA OVERVIEW
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)

print("\nNumber of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nDataset information:")
print(df.info())

# ------------------------------------------------------------
# 4. MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing_values = df.isnull().sum()

missing_values = missing_values[
    missing_values > 0
].sort_values(ascending=False)

print("\nMissing values:")
print(missing_values)

# ------------------------------------------------------------
# 5. HANDLE MISSING VALUES
# ------------------------------------------------------------

if "children" in df.columns:
    df["children"] = df["children"].fillna(0)

if "agent" in df.columns:
    df["agent"] = df["agent"].fillna(0)

if "company" in df.columns:
    df["company"] = df["company"].fillna(0)

if "country" in df.columns:
    df["country"] = df["country"].fillna("Unknown")

if "city" in df.columns:
    df["city"] = df["city"].fillna("Unknown")

print("\nMissing values handled.")

# ------------------------------------------------------------
# 6. DUPLICATES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print("Duplicate records:", duplicate_count)

df = df.drop_duplicates()

print(
    "Dataset shape after removing duplicates:",
    df.shape
)

# ------------------------------------------------------------
# 7. MEAL CLEANING
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MEAL ANALYSIS")
print("=" * 70)

if "meal" in df.columns:

    print("\nMeal values before cleaning:")
    print(df["meal"].value_counts())

    df["meal"] = df["meal"].replace(
        "Undefined",
        "No Meal"
    )

    print("\nMeal values after cleaning:")
    print(df["meal"].value_counts())

# ------------------------------------------------------------
# 8. TOTAL GUESTS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("GUEST ANALYSIS")
print("=" * 70)

df["adults"] = df["adults"].fillna(0)
df["children"] = df["children"].fillna(0)
df["babies"] = df["babies"].fillna(0)

df["total_guests"] = (
    df["adults"]
    + df["children"]
    + df["babies"]
)

zero_guest_count = (
    df["total_guests"] == 0
).sum()

print(
    "Bookings with zero guests:",
    zero_guest_count
)

# Remove zero guest bookings
df = df[df["total_guests"] > 0]

# ------------------------------------------------------------
# 9. ADR ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ADR ANALYSIS")
print("=" * 70)

print("\nADR statistics:")
print(df["adr"].describe())

negative_adr = (
    df["adr"] < 0
).sum()

print(
    "\nNegative ADR records:",
    negative_adr
)

# Remove negative ADR
df = df[df["adr"] >= 0]

# ------------------------------------------------------------
# 10. TOTAL STAY
# ------------------------------------------------------------

df["total_stay"] = (
    df["stays_in_weekend_nights"]
    +
    df["stays_in_weekdays_nights"]
)

print("\nTotal stay column created.")

# ------------------------------------------------------------
# BUSINESS QUESTION 1
# HOTEL TYPE BOOKING ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BUSINESS QUESTION 1")
print("WHICH HOTEL TYPE IS BOOKED MOST OFTEN?")
print("=" * 70)

hotel_counts = df["hotel"].value_counts()

hotel_percentage = (
    df["hotel"]
    .value_counts(normalize=True)
    * 100
)

print("\nBooking count:")
print(hotel_counts)

print("\nBooking percentage:")
print(hotel_percentage.round(2))

most_booked_hotel = hotel_counts.idxmax()

print(
    "\nMost frequently booked hotel:",
    most_booked_hotel
)

# ------------------------------------------------------------
# HOTEL BOOKING CHART
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=hotel_counts.index,
    y=hotel_counts.values
)

plt.title("Hotel Booking Share")
plt.xlabel("Hotel Type")
plt.ylabel("Number of Bookings")

plt.tight_layout()

plt.savefig(
    "outputs/hotel_booking_share.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# BUSINESS QUESTION 1B
# MONTHLY BOOKING ANALYSIS
# ------------------------------------------------------------

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_bookings = (
    df.groupby(
        ["arrival_date_month", "hotel"]
    )
    .size()
    .reset_index(
        name="bookings"
    )
)

monthly_bookings[
    "arrival_date_month"
] = pd.Categorical(
    monthly_bookings[
        "arrival_date_month"
    ],
    categories=month_order,
    ordered=True
)

monthly_bookings = (
    monthly_bookings
    .sort_values("arrival_date_month")
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_bookings,
    x="arrival_date_month",
    y="bookings",
    hue="hotel",
    marker="o"
)

plt.title(
    "Monthly Booking Trend by Hotel Type"
)

plt.xlabel("Month")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/monthly_booking_trend.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# BUSIEST / QUIETEST MONTH
# ------------------------------------------------------------

total_monthly_bookings = (
    df.groupby("arrival_date_month")
    .size()
    .reindex(month_order)
)

busiest_month = (
    total_monthly_bookings.idxmax()
)

quietest_month = (
    total_monthly_bookings.idxmin()
)

print(
    "\nBusiest month:",
    busiest_month,
    "| Bookings:",
    total_monthly_bookings.max()
)

print(
    "Quietest month:",
    quietest_month,
    "| Bookings:",
    total_monthly_bookings.min()
)

# ------------------------------------------------------------
# BUSINESS QUESTION 2
# CANCELLATION BY HOTEL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BUSINESS QUESTION 2")
print("DOES STAY DURATION AFFECT CANCELLATION?")
print("=" * 70)

cancellation_rate = (
    df.groupby("hotel")["is_canceled"]
    .mean()
    * 100
)

print("\nCancellation rate by hotel:")
print(cancellation_rate.round(2))

# ------------------------------------------------------------
# CANCELLATION CHART
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=cancellation_rate.index,
    y=cancellation_rate.values
)

plt.title(
    "Cancellation Rate by Hotel Type"
)

plt.xlabel("Hotel Type")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "outputs/cancellation_by_hotel.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# STAY DURATION VS CANCELLATION
# ------------------------------------------------------------

stay_cancellation = (
    df.groupby(
        ["hotel", "total_stay"]
    )["is_canceled"]
    .mean()
    * 100
).reset_index()

stay_cancellation.rename(
    columns={
        "is_canceled":
        "cancellation_rate"
    },
    inplace=True
)

# Limit graph to 20 nights
stay_plot = stay_cancellation[
    stay_cancellation["total_stay"] <= 20
]

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=stay_plot,
    x="total_stay",
    y="cancellation_rate",
    hue="hotel",
    marker="o"
)

plt.title(
    "Cancellation Rate vs Length of Stay"
)

plt.xlabel(
    "Length of Stay (Nights)"
)

plt.ylabel(
    "Cancellation Rate (%)"
)

plt.tight_layout()

plt.savefig(
    "outputs/stay_duration_cancellation.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# STAY GROUP ANALYSIS
# ------------------------------------------------------------

df["stay_group"] = pd.cut(
    df["total_stay"],
    bins=[0, 2, 5, 10, np.inf],
    labels=[
        "1-2 Nights",
        "3-5 Nights",
        "6-10 Nights",
        "10+ Nights"
    ]
)

stay_group_cancellation = (
    df.groupby(
        ["hotel", "stay_group"],
        observed=True
    )["is_canceled"]
    .mean()
    * 100
).reset_index()

stay_group_cancellation.rename(
    columns={
        "is_canceled":
        "cancellation_rate"
    },
    inplace=True
)

print(
    "\nCancellation rate by stay group:"
)

print(
    stay_group_cancellation
)

# ------------------------------------------------------------
# BUSINESS QUESTION 3
# LEAD TIME VS CANCELLATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BUSINESS QUESTION 3")
print("DOES LEAD TIME AFFECT CANCELLATION?")
print("=" * 70)

df["lead_time_group"] = pd.cut(
    df["lead_time"],
    bins=[
        0,
        7,
        30,
        90,
        180,
        365,
        np.inf
    ],
    labels=[
        "0-7 Days",
        "8-30 Days",
        "31-90 Days",
        "91-180 Days",
        "181-365 Days",
        "365+ Days"
    ],
    include_lowest=True
)

lead_cancellation = (
    df.groupby(
        ["hotel", "lead_time_group"],
        observed=True
    )["is_canceled"]
    .mean()
    * 100
).reset_index()

lead_cancellation.rename(
    columns={
        "is_canceled":
        "cancellation_rate"
    },
    inplace=True
)

print(
    "\nCancellation rate by lead time:"
)

print(
    lead_cancellation
)

# ------------------------------------------------------------
# LEAD TIME CHART
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=lead_cancellation,
    x="lead_time_group",
    y="cancellation_rate",
    hue="hotel",
    marker="o"
)

plt.title(
    "Cancellation Rate by Lead Time"
)

plt.xlabel(
    "Lead Time"
)

plt.ylabel(
    "Cancellation Rate (%)"
)

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "outputs/lead_time_cancellation.png",
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# OVERALL CANCELLATION
# ------------------------------------------------------------

overall_cancellation = (
    df["is_canceled"].mean()
    * 100
)

print(
    "\nOverall cancellation rate:",
    round(
        overall_cancellation,
        2
    ),
    "%"
)

# ------------------------------------------------------------
# SAVE CLEANED DATA
# ------------------------------------------------------------

df.to_csv(
    "outputs/hotel_bookings_cleaned.csv",
    index=False
)

print(
    "\nCleaned dataset saved."
)

# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)