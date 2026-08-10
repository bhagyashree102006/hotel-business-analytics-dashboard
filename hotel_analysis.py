# ============================================================
# HOTEL BUSINESS ANALYSIS USING DATA VISUALIZATION
# Internship Project
# ============================================================

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_theme(style="whitegrid")

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

# Load CSV file
df = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/Hotel_Business_Project/data/hotel_bookings_data.csv")


print("=" * 60)
print("HOTEL BUSINESS ANALYSIS")
print("=" * 60)

print("\nDataset loaded successfully!")

# Display first 5 records
print("\nFirst 5 rows:")
print(df.head())

# Dataset size
print("\nDataset Shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
# ------------------------------------------------------------
# 2. DATA OVERVIEW
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA OVERVIEW")
print("=" * 60)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

# Dataset information
print("\nDataset Information:")
print(df.info())

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())
# ------------------------------------------------------------
# 3. MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUE ANALYSIS")
print("=" * 60)

missing_values = df.isnull().sum()

print("\nMissing values in each column:")
print(missing_values[missing_values > 0])
# ------------------------------------------------------------
# 4. HANDLE MISSING VALUES
# ------------------------------------------------------------

# Handle missing values only for columns that exist

if "children" in df.columns:
    df["children"] = df["children"].fillna(0)

if "agent" in df.columns:
    df["agent"] = df["agent"].fillna(0)

if "company" in df.columns:
    df["company"] = df["company"].fillna(0)

if "country" in df.columns:
    df["country"] = df["country"].fillna("Unknown")

print("\nMissing values handled successfully.")


# ------------------------------------------------------------
# 5. DUPLICATE RECORDS
# ------------------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nNumber of duplicate records:", duplicate_count)

# Remove duplicates
df = df.drop_duplicates()

print("Duplicates removed.")
print("New dataset size:", df.shape)
# ------------------------------------------------------------
# 6. HANDLE UNDEFINED VALUES
# ------------------------------------------------------------

print("\nMeal values before cleaning:")
print(df["meal"].value_counts())

# Replace Undefined with No Meal
df["meal"] = df["meal"].replace("Undefined", "No Meal")

print("\nMeal values after cleaning:")
print(df["meal"].value_counts())
# ------------------------------------------------------------
# 7. ZERO GUEST BOOKINGS
# ------------------------------------------------------------

# Calculate total guests
df["total_guests"] = (
    df["adults"] +
    df["children"] +
    df["babies"]
)

zero_guest_count = (df["total_guests"] == 0).sum()

print("\nBookings with zero guests:", zero_guest_count)

# Remove zero guest bookings
df = df[df["total_guests"] > 0]

print("Zero guest bookings removed.")
# ------------------------------------------------------------
# 8. ADR ANALYSIS
# ------------------------------------------------------------

print("\nADR Statistics:")
print(df["adr"].describe())

# Count negative ADR
negative_adr = (df["adr"] < 0).sum()

print("\nNegative ADR records:", negative_adr)

# Remove negative ADR records
df = df[df["adr"] >= 0]

print("Invalid negative ADR records removed.")
# ------------------------------------------------------------
# 9. CREATE TOTAL STAY
# ------------------------------------------------------------

df["total_stay"] = (
    df["stays_in_weekend_nights"] +
    df["stays_in_weekdays_nights"]
)

print("\nTotal stay column created.")

print(
    df[
        [
            "stays_in_weekend_nights",
            "stays_in_weekdays_nights",
            "total_stay"
        ]
    ].head()
)
# ============================================================
# 10. BUSINESS QUESTION 1
# WHICH HOTEL TYPE IS BOOKED MOST OFTEN?
# ============================================================

print("\n" + "=" * 60)
print("BUSINESS QUESTION 1")
print("=" * 60)

# Count bookings
hotel_counts = df["hotel"].value_counts()

print("\nBookings by hotel type:")
print(hotel_counts)

# Calculate percentage
hotel_percentage = (
    df["hotel"]
    .value_counts(normalize=True)
    * 100
)

print("\nBooking percentage:")
print(hotel_percentage.round(2))

# Most booked hotel
most_booked_hotel = hotel_counts.idxmax()

print(
    "\nMost frequently booked hotel:",
    most_booked_hotel
)
# ------------------------------------------------------------
# HOTEL BOOKING BAR CHART
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=hotel_counts.index,
    y=hotel_counts.values
)

plt.title("Number of Bookings by Hotel Type")
plt.xlabel("Hotel Type")
plt.ylabel("Number of Bookings")

plt.tight_layout()

plt.savefig(
    "hotel_booking_share.png",
    dpi=300
)

plt.show()
# ------------------------------------------------------------
# HOTEL BOOKING PIE CHART
# ------------------------------------------------------------

plt.figure(figsize=(7, 7))

plt.pie(
    hotel_counts.values,
    labels=hotel_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Booking Share by Hotel Type")

plt.savefig(
    "hotel_booking_pie.png",
    dpi=300
)

plt.show()
# ============================================================
# 11. MONTHLY BOOKING ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("MONTHLY BOOKING ANALYSIS")
print("=" * 60)

# Correct month order
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

# Group monthly bookings
monthly_bookings = (
    df.groupby(
        ["arrival_date_month", "hotel"]
    )
    .size()
    .reset_index(name="bookings")
)

# Correct month order
monthly_bookings["arrival_date_month"] = pd.Categorical(
    monthly_bookings["arrival_date_month"],
    categories=month_order,
    ordered=True
)

monthly_bookings = monthly_bookings.sort_values(
    "arrival_date_month"
)

print("\nMonthly booking data:")
print(monthly_bookings)
# ------------------------------------------------------------
# MONTHLY BOOKING TREND
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_bookings,
    x="arrival_date_month",
    y="bookings",
    hue="hotel",
    marker="o"
)

plt.title("Monthly Booking Trend by Hotel Type")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "monthly_booking_trend.png",
    dpi=300
)

plt.show()
# ------------------------------------------------------------
# BUSIEST AND QUIETEST MONTH
# ------------------------------------------------------------

total_monthly_bookings = (
    df.groupby("arrival_date_month")
    .size()
    .reindex(month_order)
)

busiest_month = total_monthly_bookings.idxmax()
busiest_count = total_monthly_bookings.max()

quietest_month = total_monthly_bookings.idxmin()
quietest_count = total_monthly_bookings.min()

print("\nBusiest month:")
print(busiest_month, "-", busiest_count, "bookings")

print("\nQuietest month:")
print(quietest_month, "-", quietest_count, "bookings")
# ============================================================
# 12. BUSINESS QUESTION 2
# DOES LENGTH OF STAY AFFECT CANCELLATION?
# ============================================================

print("\n" + "=" * 60)
print("BUSINESS QUESTION 2")
print("=" * 60)

# Cancellation rate by hotel
cancellation_by_hotel = (
    df.groupby("hotel")["is_canceled"]
    .mean()
    * 100
)

print("\nCancellation rate by hotel:")
print(cancellation_by_hotel.round(2))
# ------------------------------------------------------------
# CANCELLATION RATE BY HOTEL
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=cancellation_by_hotel.index,
    y=cancellation_by_hotel.values
)

plt.title("Cancellation Rate by Hotel Type")
plt.xlabel("Hotel Type")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "cancellation_rate_by_hotel.png",
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
        "is_canceled": "cancellation_rate"
    },
    inplace=True
)

# Display first records
print("\nStay duration cancellation data:")
print(stay_cancellation.head(20))
# ------------------------------------------------------------
# STAY DURATION CANCELLATION GRAPH
# ------------------------------------------------------------

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

plt.xlabel("Total Stay (Nights)")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "stay_duration_vs_cancellation.png",
    dpi=300
)

plt.show()
# ============================================================
# 13. BUSINESS QUESTION 3
# DOES LEAD TIME AFFECT CANCELLATION?
# ============================================================

print("\n" + "=" * 60)
print("BUSINESS QUESTION 3")
print("=" * 60)

# Create lead time groups

bins = [
    0,
    7,
    30,
    90,
    180,
    365,
    np.inf
]

labels = [
    "0-7 days",
    "8-30 days",
    "31-90 days",
    "91-180 days",
    "181-365 days",
    "365+ days"
]

df["lead_time_group"] = pd.cut(
    df["lead_time"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

print("\nLead time groups created:")
print(df["lead_time_group"].value_counts().sort_index())
# ------------------------------------------------------------
# LEAD TIME VS CANCELLATION RATE
# ------------------------------------------------------------

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
        "is_canceled": "cancellation_rate"
    },
    inplace=True
)

print("\nCancellation rate by lead time:")
print(lead_cancellation)
# ------------------------------------------------------------
# LEAD TIME CANCELLATION GRAPH
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

plt.xlabel("Lead Time")
plt.ylabel("Cancellation Rate (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "lead_time_vs_cancellation.png",
    dpi=300
)

plt.show()
# ------------------------------------------------------------
# HIGHEST AND LOWEST CANCELLATION GROUPS
# ------------------------------------------------------------

highest = lead_cancellation.loc[
    lead_cancellation["cancellation_rate"].idxmax()
]

lowest = lead_cancellation.loc[
    lead_cancellation["cancellation_rate"].idxmin()
]

print("\nHighest cancellation group:")
print(highest)

print("\nLowest cancellation group:")
print(lowest)
# ============================================================
# 14. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL PROJECT SUMMARY")
print("=" * 60)

print(
    f"\nMost frequently booked hotel: "
    f"{most_booked_hotel}"
)

print(
    f"Most popular hotel booking percentage: "
    f"{hotel_percentage.max():.2f}%"
)

print(
    f"\nBusiest month: "
    f"{busiest_month} ({busiest_count} bookings)"
)

print(
    f"Quietest month: "
    f"{quietest_month} ({quietest_count} bookings)"
)

print("\nCancellation rate by hotel:")
print(cancellation_by_hotel.round(2))

print("\nHighest lead-time cancellation:")
print(highest)

print("\nLowest lead-time cancellation:")
print(lowest)

print("\nAnalysis completed successfully!")

# ------------------------------------------------------------
# 5. DUPLICATE RECORDS
# ------------------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\n" + "=" * 60)
print("DUPLICATE RECORD ANALYSIS")
print("=" * 60)

print("Number of duplicate records:", duplicate_count)

# Remove duplicate records
df = df.drop_duplicates()

print("Duplicates removed.")
print("Current dataset shape:", df.shape)
# ------------------------------------------------------------
# 6. MEAL VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MEAL VALUE ANALYSIS")
print("=" * 60)

if "meal" in df.columns:

    print("\nMeal values before cleaning:")
    print(df["meal"].value_counts(dropna=False))

    # Replace Undefined with No Meal
    df["meal"] = df["meal"].replace(
        "Undefined",
        "No Meal"
    )

    print("\nMeal values after cleaning:")
    print(df["meal"].value_counts(dropna=False))

else:
    print("Meal column is not available in this dataset.")
    # ------------------------------------------------------------
# 7. TOTAL GUESTS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("GUEST ANALYSIS")
print("=" * 60)

# Check that required columns exist
required_guest_columns = [
    "adults",
    "children",
    "babies"
]

if all(column in df.columns for column in required_guest_columns):

    # Handle missing values
    df["adults"] = df["adults"].fillna(0)
    df["children"] = df["children"].fillna(0)
    df["babies"] = df["babies"].fillna(0)

    # Calculate total guests
    df["total_guests"] = (
        df["adults"]
        + df["children"]
        + df["babies"]
    )

    print("\nTotal guests column created.")

    print(
        df[
            [
                "adults",
                "children",
                "babies",
                "total_guests"
            ]
        ].head()
    )

else:
    print("Guest columns are not available.")
    # ------------------------------------------------------------
# 8. ZERO GUEST BOOKINGS
# ------------------------------------------------------------

if "total_guests" in df.columns:

    zero_guest_count = (
        df["total_guests"] == 0
    ).sum()

    print(
        "\nNumber of bookings with zero guests:",
        zero_guest_count
    )

    # Remove zero-guest bookings
    df = df[df["total_guests"] > 0]

    print(
        "Zero-guest bookings removed."
    )

    print(
        "Current dataset shape:",
        df.shape
    )
    # ------------------------------------------------------------
# 9. ADR ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ADR ANALYSIS")
print("=" * 60)

if "adr" in df.columns:

    print("\nADR statistics:")
    print(df["adr"].describe())

    # Check negative ADR
    negative_adr_count = (
        df["adr"] < 0
    ).sum()

    print(
        "\nNumber of negative ADR records:",
        negative_adr_count
    )

    # Remove negative ADR
    df = df[df["adr"] >= 0]

    print(
        "Negative ADR records removed."
    )

else:
    print("ADR column is not available.")
    # ------------------------------------------------------------
# 10. TOTAL STAY DURATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAY DURATION")
print("=" * 60)

if (
    "stays_in_weekend_nights" in df.columns
    and
    "stays_in_weekdays_nights" in df.columns
):

    df["total_stay"] = (
        df["stays_in_weekend_nights"]
        +
        df["stays_in_weekdays_nights"]
    )

    print("\nTotal stay column created.")

    print(
        df[
            [
                "stays_in_weekend_nights",
                "stays_in_weekdays_nights",
                "total_stay"
            ]
        ].head()
    )

else:
    print(
        "Stay-duration columns are not available."
    )
    # ------------------------------------------------------------
# 11. FINAL DATA QUALITY CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA QUALITY CHECK")
print("=" * 60)

print("\nFinal rows:", df.shape[0])
print("Final columns:", df.shape[1])

print(
    "\nTotal remaining missing values:",
    df.isnull().sum().sum()
)

print(
    "Total remaining duplicate rows:",
    df.duplicated().sum()
)

print("\nData preprocessing completed successfully.")
# ============================================================
# BUSINESS QUESTION 2
# DOES LENGTH OF STAY AFFECT CANCELLATION?
# ============================================================

print("\n" + "=" * 60)
print("CANCELLATION ANALYSIS")
print("=" * 60)

# Calculate cancellation rate
cancellation_rate = (
    df.groupby("hotel")["is_canceled"]
    .mean()
    * 100
)

print("\nCancellation Rate by Hotel:")
print(cancellation_rate.round(2))
# ------------------------------------------------------------
# CANCELLATION RATE BY HOTEL
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    x=cancellation_rate.index,
    y=cancellation_rate.values
)

plt.title("Cancellation Rate by Hotel Type")
plt.xlabel("Hotel Type")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "cancellation_rate_by_hotel.png",
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
        "is_canceled": "cancellation_rate"
    },
    inplace=True
)

print("\nCancellation Rate by Length of Stay:")
print(stay_cancellation.head(20))
# ------------------------------------------------------------
# STAY DURATION VS CANCELLATION GRAPH
# ------------------------------------------------------------

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

plt.xlabel("Length of Stay (Nights)")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "stay_duration_vs_cancellation.png",
    dpi=300
)

plt.show()
# ------------------------------------------------------------
# STAY DURATION GROUPS
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
        "is_canceled": "cancellation_rate"
    },
    inplace=True
)

print("\nCancellation Rate by Stay Group:")
print(
    stay_group_cancellation
)
# ------------------------------------------------------------
# STAY GROUP CANCELLATION CHART
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.barplot(
    data=stay_group_cancellation,
    x="stay_group",
    y="cancellation_rate",
    hue="hotel"
)

plt.title(
    "Cancellation Rate by Length of Stay Group"
)

plt.xlabel("Length of Stay")
plt.ylabel("Cancellation Rate (%)")

plt.tight_layout()

plt.savefig(
    "stay_group_cancellation.png",
    dpi=300
)

plt.show()
# ============================================================
# BUSINESS QUESTION 3
# DOES LEAD TIME AFFECT CANCELLATION?
# ============================================================

print("\n" + "=" * 60)
print("LEAD TIME ANALYSIS")
print("=" * 60)

# Create lead time groups

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

print("\nLead Time Groups:")
print(
    df["lead_time_group"]
    .value_counts()
    .sort_index()
)
# ------------------------------------------------------------
# LEAD TIME CANCELLATION RATE
# ------------------------------------------------------------

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
        "is_canceled": "cancellation_rate"
    },
    inplace=True
)

print("\nCancellation Rate by Lead Time:")
print(lead_cancellation)
# ------------------------------------------------------------
# LEAD TIME VS CANCELLATION GRAPH
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

plt.xlabel("Lead Time")
plt.ylabel("Cancellation Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "lead_time_vs_cancellation.png",
    dpi=300
)

plt.show()
# ------------------------------------------------------------
# HIGHEST AND LOWEST CANCELLATION
# ------------------------------------------------------------

highest_cancellation = lead_cancellation.loc[
    lead_cancellation["cancellation_rate"].idxmax()
]

lowest_cancellation = lead_cancellation.loc[
    lead_cancellation["cancellation_rate"].idxmin()
]

print("\nHighest Cancellation Group:")
print(highest_cancellation)

print("\nLowest Cancellation Group:")
print(lowest_cancellation)
# ------------------------------------------------------------
# OVERALL CANCELLATION RATE
# ------------------------------------------------------------

overall_cancellation = (
    df["is_canceled"].mean() * 100
)

print(
    "\nOverall Cancellation Rate:",
    round(overall_cancellation, 2),
    "%"
)
# ============================================================
# 15. KEY FINDINGS
# ============================================================

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)

# ------------------------------------------------------------
# FINDING 1: HOTEL TYPE
# ------------------------------------------------------------

most_booked_hotel = hotel_counts.idxmax()
most_booked_count = hotel_counts.max()
most_booked_percentage = hotel_percentage.max()

print("\n1. HOTEL TYPE")
print(
    f"{most_booked_hotel} receives the highest number of bookings "
    f"with {most_booked_count} bookings "
    f"({most_booked_percentage:.2f}% of total bookings)."
)


# ------------------------------------------------------------
# FINDING 2: MONTHLY BOOKINGS
# ------------------------------------------------------------

print("\n2. MONTHLY BOOKING PATTERN")

print(
    f"The busiest month is {busiest_month} "
    f"with {busiest_count} bookings."
)

print(
    f"The quietest month is {quietest_month} "
    f"with {quietest_count} bookings."
)


# ------------------------------------------------------------
# FINDING 3: HOTEL CANCELLATION
# ------------------------------------------------------------

print("\n3. CANCELLATION BY HOTEL")

highest_hotel_cancellation = (
    cancellation_rate.idxmax()
)

highest_hotel_rate = (
    cancellation_rate.max()
)

lowest_hotel_cancellation = (
    cancellation_rate.idxmin()
)

lowest_hotel_rate = (
    cancellation_rate.min()
)

print(
    f"{highest_hotel_cancellation} has the highest "
    f"cancellation rate of "
    f"{highest_hotel_rate:.2f}%."
)

print(
    f"{lowest_hotel_cancellation} has the lowest "
    f"cancellation rate of "
    f"{lowest_hotel_rate:.2f}%."
)


# ------------------------------------------------------------
# FINDING 4: STAY DURATION
# ------------------------------------------------------------

print("\n4. STAY DURATION")

highest_stay_group = stay_group_cancellation.loc[
    stay_group_cancellation["cancellation_rate"].idxmax()
]

lowest_stay_group = stay_group_cancellation.loc[
    stay_group_cancellation["cancellation_rate"].idxmin()
]

print(
    f"The highest cancellation rate occurs in the "
    f"{highest_stay_group['stay_group']} category "
    f"for {highest_stay_group['hotel']}, "
    f"at {highest_stay_group['cancellation_rate']:.2f}%."
)

print(
    f"The lowest cancellation rate occurs in the "
    f"{lowest_stay_group['stay_group']} category "
    f"for {lowest_stay_group['hotel']}, "
    f"at {lowest_stay_group['cancellation_rate']:.2f}%."
)


# ------------------------------------------------------------
# FINDING 5: LEAD TIME
# ------------------------------------------------------------

print("\n5. LEAD TIME")

print(
    f"The highest cancellation rate was observed for "
    f"{highest_cancellation['hotel']} bookings in the "
    f"{highest_cancellation['lead_time_group']} lead-time group, "
    f"at {highest_cancellation['cancellation_rate']:.2f}%."
)

print(
    f"The lowest cancellation rate was observed for "
    f"{lowest_cancellation['hotel']} bookings in the "
    f"{lowest_cancellation['lead_time_group']} lead-time group, "
    f"at {lowest_cancellation['cancellation_rate']:.2f}%."
)
# ============================================================
# 16. SAVE ANALYSIS RESULTS
# ============================================================

summary_data = {
    "Metric": [
        "Most Booked Hotel",
        "Most Booked Hotel Percentage",
        "Busiest Month",
        "Busiest Month Bookings",
        "Quietest Month",
        "Quietest Month Bookings",
        "Overall Cancellation Rate"
    ],

    "Value": [
        most_booked_hotel,
        round(most_booked_percentage, 2),
        busiest_month,
        busiest_count,
        quietest_month,
        quietest_count,
        round(overall_cancellation, 2)
    ]
}

summary_df = pd.DataFrame(summary_data)

summary_df.to_csv(
    "hotel_analysis_summary.csv",
    index=False
)

print("\nAnalysis summary saved as:")
print("hotel_analysis_summary.csv")
# ============================================================
# 17. SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    "hotel_bookings_cleaned.csv",
    index=False
)

print(
    "\nCleaned dataset saved as:"
    " hotel_bookings_cleaned.csv"
)
# ============================================================
# 18. BUSINESS RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 60)
print("BUSINESS RECOMMENDATIONS")
print("=" * 60)

print("\n1. HOTEL TYPE")
print(
    f"Focus marketing and promotional strategies on "
    f"{most_booked_hotel}, while developing targeted campaigns "
    f"to improve demand for the other hotel type."
)

print("\n2. SEASONAL DEMAND")
print(
    f"Prepare additional operational resources during "
    f"the busiest period around {busiest_month} and use "
    f"promotional offers during quieter periods such as "
    f"{quietest_month}."
)

print("\n3. CANCELLATION MANAGEMENT")
print(
    "Consider suitable cancellation policies, booking "
    "confirmation messages and reminders to reduce "
    "potential cancellation-related revenue loss."
)

print("\n4. STAY DURATION")
print(
    "Monitor cancellation behaviour across different "
    "stay-duration groups and consider appropriate "
    "booking conditions for groups with higher cancellation rates."
)

print("\n5. LEAD TIME")
print(
    "Bookings made far in advance should be monitored "
    "carefully if they show higher cancellation rates. "
    "Advance reminders and flexible rebooking options "
    "can help reduce cancellation risk."
)

print("\n6. DATA-DRIVEN DECISIONS")
print(
    "Use historical booking, cancellation and seasonal "
    "patterns to support pricing, marketing and resource planning."
)
# ============================================================
# 19. PROJECT CONCLUSION
# ============================================================

print("\n" + "=" * 60)
print("PROJECT CONCLUSION")
print("=" * 60)

print("""
The hotel booking dataset was analysed using Python,
Pandas, NumPy, Matplotlib and Seaborn.

The analysis examined hotel type preferences, monthly
booking patterns, cancellation behaviour, length of stay
and lead time.

Data preprocessing was performed by checking missing
values, duplicate records, unclear values, zero-guest
bookings and invalid ADR values.

The analysis provides useful business insights that can
help hotel management improve demand planning, marketing,
pricing strategies and cancellation management.

The project demonstrates how data visualization and
exploratory data analysis can support data-driven
decision making in the hotel business.
""")

print("=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 60)

