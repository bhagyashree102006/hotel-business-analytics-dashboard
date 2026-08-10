import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hotel Business Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    possible_files = [
        Path("data/hotel_bookings_data.csv"),
        Path("data/hotel_bookings.csv"),
        Path("hotel_bookings_data.csv"),
        Path("hotel_bookings.csv")
    ]

    for file in possible_files:

        if file.exists():
            return pd.read_csv(file)

    return None


df = load_data()


# ============================================================
# DATASET CHECK
# ============================================================

if df is None:

    st.error("Hotel dataset was not found.")

    st.info(
        "Please place your CSV file inside the data folder."
    )

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "hotel",
    "is_canceled",
    "arrival_date_year",
    "arrival_date_month",
    "stays_in_weekend_nights",
    "stays_in_weekdays_nights",
    "adults",
    "children",
    "babies",
    "market_segment",
    "customer_type",
    "adr",
    "reservation_status"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error("Some required columns are missing.")

    st.write(missing_columns)

    st.write("Available columns:")

    st.write(list(df.columns))

    st.stop()


# ============================================================
# DATA CLEANING
# ============================================================

numeric_columns = [
    "is_canceled",
    "arrival_date_year",
    "stays_in_weekend_nights",
    "stays_in_weekdays_nights",
    "adults",
    "children",
    "babies",
    "adr"
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


df["children"] = df["children"].fillna(0)
df["adults"] = df["adults"].fillna(0)
df["babies"] = df["babies"].fillna(0)
df["adr"] = df["adr"].fillna(0)


# ============================================================
# DERIVED COLUMNS
# ============================================================

df["total_nights"] = (
    df["stays_in_weekend_nights"]
    + df["stays_in_weekdays_nights"]
)


df["total_guests"] = (
    df["adults"]
    + df["children"]
    + df["babies"]
)


# ============================================================
# MONTH ORDER
# ============================================================

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


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏨 HotelIQ")

    st.caption("Hotel Business Intelligence")

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "📊 Dataset",
            "📈 EDA",
            "🔬 Statistical Analysis",
            "🎯 Business Insights",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("🎯 Filters")

    st.caption(
        "Use the filters to customize your analysis."
    )


    # HOTEL

    hotel_options = [
        "All"
    ] + sorted(
        df["hotel"]
        .dropna()
        .unique()
        .tolist()
    )

    hotel_type = st.selectbox(
        "Hotel Type",
        hotel_options
    )


    # BOOKING STATUS

    booking_status = st.selectbox(
        "Booking Status",
        [
            "All",
            "Confirmed",
            "Cancelled",
            "No-Show"
        ]
    )


    # YEAR

    year_values = sorted(
        df["arrival_date_year"]
        .dropna()
        .unique()
        .tolist()
    )

    arrival_year = st.selectbox(
        "Arrival Year",
        ["All"] +
        [
            str(int(year))
            for year in year_values
        ]
    )


    # MONTH

    available_months = [
        month
        for month in month_order
        if month in df["arrival_date_month"]
        .dropna()
        .unique()
    ]

    arrival_month = st.selectbox(
        "Arrival Month",
        ["All"] + available_months
    )


    # MARKET SEGMENT

    market_options = [
        "All"
    ] + sorted(
        df["market_segment"]
        .dropna()
        .unique()
        .tolist()
    )

    market_segment = st.selectbox(
        "Market Segment",
        market_options
    )


    # CUSTOMER TYPE

    customer_options = [
        "All"
    ] + sorted(
        df["customer_type"]
        .dropna()
        .unique()
        .tolist()
    )

    customer_type = st.selectbox(
        "Customer Type",
        customer_options
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if hotel_type != "All":

    filtered_df = filtered_df[
        filtered_df["hotel"] == hotel_type
    ]


if booking_status == "Confirmed":

    filtered_df = filtered_df[
        filtered_df["reservation_status"]
        == "Check-Out"
    ]

elif booking_status == "Cancelled":

    filtered_df = filtered_df[
        filtered_df["reservation_status"]
        == "Canceled"
    ]

elif booking_status == "No-Show":

    filtered_df = filtered_df[
        filtered_df["reservation_status"]
        == "No-Show"
    ]


if arrival_year != "All":

    filtered_df = filtered_df[
        filtered_df["arrival_date_year"]
        == int(arrival_year)
    ]


if arrival_month != "All":

    filtered_df = filtered_df[
        filtered_df["arrival_date_month"]
        == arrival_month
    ]


if market_segment != "All":

    filtered_df = filtered_df[
        filtered_df["market_segment"]
        == market_segment
    ]


if customer_type != "All":

    filtered_df = filtered_df[
        filtered_df["customer_type"]
        == customer_type
    ]


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("🏨 Hotel Business Analytics")

    st.subheader(
        "Predictive and Descriptive Analytics for Hotel Business Performance"
    )

    st.write(
        "Analyze hotel bookings, cancellation behaviour, "
        "pricing, customer segments and demand patterns."
    )

    st.header("📊 Dashboard Overview")

    total_bookings = len(filtered_df)

    if total_bookings > 0:

        cancelled = (
            filtered_df["reservation_status"]
            == "Canceled"
        ).sum()

        confirmed = (
            filtered_df["reservation_status"]
            == "Check-Out"
        ).sum()

        cancellation_rate = (
            cancelled / total_bookings
        ) * 100

        confirmation_rate = (
            confirmed / total_bookings
        ) * 100

        average_adr = filtered_df["adr"].mean()

        average_stay = filtered_df[
            "total_nights"
        ].mean()

        total_guests = filtered_df[
            "total_guests"
        ].sum()

    else:

        cancellation_rate = 0
        confirmation_rate = 0
        average_adr = 0
        average_stay = 0
        total_guests = 0


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏨 Total Bookings",
            f"{total_bookings:,}"
        )

    with col2:
        st.metric(
            "✅ Confirmation Rate",
            f"{confirmation_rate:.1f}%"
        )

    with col3:
        st.metric(
            "💰 Average ADR",
            f"${average_adr:,.2f}"
        )


    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "❌ Cancellation Rate",
            f"{cancellation_rate:.1f}%"
        )

    with col5:
        st.metric(
            "🌙 Average Stay",
            f"{average_stay:.1f} nights"
        )

    with col6:
        st.metric(
            "👥 Total Guests",
            f"{total_guests:,.0f}"
        )


    st.divider()

    st.header("📈 Booking Performance")


    monthly = (
        filtered_df
        .groupby("arrival_date_month")
        .size()
        .reindex(month_order)
        .fillna(0)
        .reset_index(name="Bookings")
    )


    fig = px.line(
        monthly,
        x="arrival_date_month",
        y="Bookings",
        markers=True,
        title="Monthly Booking Trend"
    )

    fig.update_layout(
        xaxis_title="Arrival Month",
        yaxis_title="Bookings",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    hotel_summary = (
        filtered_df
        .groupby("hotel")
        .size()
        .reset_index(name="Bookings")
    )


    fig_hotel = px.bar(
        hotel_summary,
        x="hotel",
        y="Bookings",
        text="Bookings",
        title="Bookings by Hotel Type"
    )

    st.plotly_chart(
        fig_hotel,
        use_container_width=True
    )


# ============================================================
# PAGE 2 — DATASET
# ============================================================

elif page == "📊 Dataset":

    st.title("📊 Dataset Explorer")

    st.write(
        "Explore the hotel booking records used in this project."
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Total Columns",
            f"{len(df.columns):,}"
        )

    with col3:
        st.metric(
            "Filtered Records",
            f"{len(filtered_df):,}"
        )


    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        hide_index=True
    )


    st.subheader("Dataset Information")
    st.subheader("Download Filtered Dataset")

    csv_data = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_data,
        file_name="filtered_hotel_data.csv",
        mime="text/csv"
    )

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(df[column].dtype)
            for column in df.columns
        ],
        "Missing Values": [
            int(df[column].isna().sum())
            for column in df.columns
        ],
        "Unique Values": [
            int(df[column].nunique())
            for column in df.columns
        ]
    })


    st.dataframe(
        info_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 3 — EDA
# ============================================================

elif page == "📈 EDA":

    st.title("📈 Exploratory Data Analysis")

    st.write(
        "Explore data quality, distributions, trends and "
        "relationships within the hotel booking dataset."
    )


    # --------------------------------------------------------
    # EDA KPIs
    # --------------------------------------------------------

    total_rows = len(df)

    total_columns = len(df.columns)

    missing_values = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Records",
            f"{total_rows:,}"
        )


    with col2:

        st.metric(
            "Features",
            f"{total_columns:,}"
        )


    with col3:

        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )


    with col4:

        st.metric(
            "Duplicate Rows",
            f"{duplicate_rows:,}"
        )


    # --------------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------------

    st.divider()

    st.header("🔎 Missing Value Analysis")


    missing_df = (
        df.isna()
        .sum()
        .reset_index()
    )


    missing_df.columns = [
        "Column",
        "Missing Values"
    ]


    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]


    if len(missing_df) > 0:

        missing_df = missing_df.sort_values(
            "Missing Values",
            ascending=False
        )


        fig_missing = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            text="Missing Values",
            title="Missing Values by Column"
        )


        fig_missing.update_layout(
            xaxis_title="Column",
            yaxis_title="Missing Values"
        )


        st.plotly_chart(
            fig_missing,
            use_container_width=True
        )

    else:

        st.success(
            "No missing values were found in the dataset."
        )


    # --------------------------------------------------------
    # NUMERICAL SUMMARY
    # --------------------------------------------------------

    st.divider()

    st.header("📊 Numerical Summary")


    numeric_df = df.select_dtypes(
        include="number"
    )


    summary = numeric_df.describe().T


    summary = summary.reset_index()

    summary = summary.rename(
        columns={
            "index": "Feature"
        }
    )


    st.dataframe(
        summary,
        use_container_width=True
    )


    # --------------------------------------------------------
    # ADR DISTRIBUTION
    # --------------------------------------------------------

    st.divider()

    st.header("💰 ADR Distribution")


    fig_adr = px.histogram(
        filtered_df,
        x="adr",
        nbins=50,
        title="Average Daily Rate Distribution"
    )


    fig_adr.update_layout(
        xaxis_title="ADR",
        yaxis_title="Number of Bookings"
    )


    st.plotly_chart(
        fig_adr,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LEAD TIME
    # --------------------------------------------------------

    if "lead_time" in df.columns:

        st.header("⏱️ Lead Time Analysis")


        fig_lead = px.histogram(
            filtered_df,
            x="lead_time",
            nbins=50,
            title="Booking Lead Time Distribution"
        )


        fig_lead.update_layout(
            xaxis_title="Lead Time (Days)",
            yaxis_title="Number of Bookings"
        )


        st.plotly_chart(
            fig_lead,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TOTAL STAY
    # --------------------------------------------------------

    st.header("🌙 Length of Stay Analysis")


    fig_stay = px.histogram(
        filtered_df,
        x="total_nights",
        nbins=30,
        title="Distribution of Total Stay Nights"
    )


    fig_stay.update_layout(
        xaxis_title="Total Nights",
        yaxis_title="Number of Bookings"
    )


    st.plotly_chart(
        fig_stay,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CORRELATION ANALYSIS
    # --------------------------------------------------------

    st.divider()

    st.header("🔗 Correlation Analysis")


    correlation_columns = [
        "is_canceled",
        "lead_time",
        "arrival_date_year",
        "arrival_date_week_number",
        "arrival_date_day_of_month",
        "stays_in_weekend_nights",
        "stays_in_weekdays_nights",
        "adults",
        "children",
        "babies",
        "adr",
        "required_car_parking_spaces",
        "total_of_special_requests"
    ]


    available_correlation_columns = [
        column
        for column in correlation_columns
        if column in df.columns
    ]


    correlation = df[
        available_correlation_columns
    ].corr()


    fig_corr = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix"
    )


    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )


    # --------------------------------------------------------
    # EDA FINDINGS
    # --------------------------------------------------------

    st.divider()

    st.header("📝 Key EDA Findings")


    st.write(
        "• The dataset contains "
        f"{len(df):,} booking records."
    )


    st.write(
        "• The dataset contains "
        f"{len(df.columns)} analytical features."
    )


    st.write(
        "• Average Daily Rate (ADR) is used "
        "as an important pricing indicator."
    )


    st.write(
        "• Lead time helps understand how early "
        "customers make hotel reservations."
    )


    st.write(
        "• Cancellation behaviour can be studied "
        "using reservation status and cancellation indicators."
    )


# ============================================================
# PAGE 4 — STATISTICAL ANALYSIS
# ============================================================

elif page == "🔬 Statistical Analysis":

    st.title("🔬 Statistical Analysis")

    st.write(
        "Statistical exploration of important numerical variables."
    )


    numerical_columns = [
        column
        for column in [
            "lead_time",
            "adr",
            "total_nights",
            "adults",
            "children",
            "babies",
            "total_guests"
        ]
        if column in filtered_df.columns
    ]


    selected_variable = st.selectbox(
        "Select Variable",
        numerical_columns
    )


    st.subheader(
        f"Distribution of {selected_variable}"
    )


    fig = px.histogram(
        filtered_df,
        x=selected_variable,
        nbins=40,
        title=f"{selected_variable} Distribution"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    statistics = filtered_df[
        selected_variable
    ].describe()


    st.subheader("Descriptive Statistics")


    stats_df = pd.DataFrame({
        "Statistic": statistics.index,
        "Value": statistics.values
    })


    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 5 — BUSINESS INSIGHTS
# ============================================================

elif page == "🎯 Business Insights":

    st.title("🎯 Business Insights")

    st.write(
        "Data-driven observations and recommendations "
        "for hotel management."
    )

    if len(filtered_df) == 0:

        st.warning(
            "No records are available for the selected filters."
        )

    else:

        # ====================================================
        # BASIC BUSINESS METRICS
        # ====================================================

        total = len(filtered_df)

        cancelled = (
            filtered_df["reservation_status"]
            == "Canceled"
        ).sum()

        cancellation_rate = (
            cancelled / total
        ) * 100


        average_adr = filtered_df["adr"].mean()


        average_stay = filtered_df[
            "total_nights"
        ].mean()


        # ====================================================
        # TOP HOTEL
        # ====================================================

        hotel_counts = (
            filtered_df
            .groupby("hotel")
            .size()
            .sort_values(
                ascending=False
            )
        )


        top_hotel = hotel_counts.index[0]

        top_hotel_bookings = hotel_counts.iloc[0]


        # ====================================================
        # TOP MONTH
        # ====================================================

        month_counts = (
            filtered_df
            .groupby("arrival_date_month")
            .size()
        )


        month_counts = (
            month_counts
            .reindex(month_order)
            .dropna()
        )


        if len(month_counts) > 0:

            top_month = month_counts.idxmax()

            top_month_bookings = int(
                month_counts.max()
            )

        else:

            top_month = "N/A"

            top_month_bookings = 0


        # ====================================================
        # HIGHEST ADR HOTEL
        # ====================================================

        adr_by_hotel = (
            filtered_df
            .groupby("hotel")["adr"]
            .mean()
            .sort_values(
                ascending=False
            )
        )


        highest_adr_hotel = adr_by_hotel.index[0]

        highest_adr_value = adr_by_hotel.iloc[0]


        # ====================================================
        # KPI SECTION
        # ====================================================

        st.header("📊 Key Business Metrics")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Total Bookings",
                f"{total:,}"
            )


        with col2:

            st.metric(
                "Cancellation Rate",
                f"{cancellation_rate:.1f}%"
            )


        with col3:

            st.metric(
                "Average ADR",
                f"${average_adr:,.2f}"
            )


        with col4:

            st.metric(
                "Average Stay",
                f"{average_stay:.1f} nights"
            )


        # ====================================================
        # PERFORMANCE INSIGHTS
        # ====================================================

        st.divider()

        st.header("🏆 Performance Insights")


        insight1, insight2 = st.columns(2)


        with insight1:

            with st.container(border=True):

                st.subheader("🏨 Top Performing Hotel")

                st.write(
                    f"**{top_hotel}** has the highest "
                    f"booking volume with "
                    f"**{top_hotel_bookings:,} bookings**."
                )


        with insight2:

            with st.container(border=True):

                st.subheader("📅 Highest Demand Month")

                st.write(
                    f"**{top_month}** recorded the highest "
                    f"booking demand with "
                    f"**{top_month_bookings:,} bookings**."
                )


        insight3, insight4 = st.columns(2)


        with insight3:

            with st.container(border=True):

                st.subheader("💰 Highest ADR")

                st.write(
                    f"**{highest_adr_hotel}** has the highest "
                    f"average daily rate of "
                    f"**${highest_adr_value:,.2f}**."
                )


        with insight4:

            with st.container(border=True):

                st.subheader("❌ Cancellation Behaviour")

                st.write(
                    f"The current cancellation rate is "
                    f"**{cancellation_rate:.1f}%**."
                )


        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        st.divider()

        st.header("💡 Management Recommendations")


        if cancellation_rate >= 30:

            st.warning(
                "Cancellation rate is relatively high. "
                "Management should consider reviewing "
                "cancellation policies, deposit requirements "
                "and customer retention strategies."
            )

        elif cancellation_rate >= 20:

            st.info(
                "Cancellation levels require monitoring. "
                "Targeted offers and flexible booking policies "
                "could help improve booking retention."
            )

        else:

            st.success(
                "Cancellation levels are relatively controlled. "
                "The current booking strategy appears effective."
            )


        if average_stay < 3:

            st.info(
                "The average stay is relatively short. "
                "Long-stay packages and extended-stay discounts "
                "could encourage customers to stay longer."
            )

        else:

            st.success(
                "The average length of stay indicates "
                "reasonable customer engagement with the hotel."
            )


        st.info(
            f"{top_month} represents the strongest demand period. "
            "Management can consider dynamic pricing and "
            "targeted promotional campaigns during high-demand periods."
        )


        st.info(
            f"{highest_adr_hotel} records the highest ADR. "
            "Management can study its pricing strategy and "
            "apply successful pricing practices where appropriate."
        )


        # ====================================================
        # FINAL BUSINESS SUMMARY
        # ====================================================

        st.divider()

        st.header("📋 Executive Summary")


        st.write(
            f"""
            Based on the selected data:

            • Total bookings analyzed: **{total:,}**

            • Cancellation rate: **{cancellation_rate:.1f}%**

            • Average Daily Rate: **${average_adr:,.2f}**

            • Average length of stay: **{average_stay:.1f} nights**

            • Highest booking volume: **{top_hotel}**

            • Highest demand month: **{top_month}**

            • Highest ADR hotel: **{highest_adr_hotel}**
            """
        )