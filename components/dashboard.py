from utils.capitalize_column import capitalize_column
import plotly.express as px
import pandas as pd

def dashboard(st,engine):
    st.title("Dashboard")
    st.write("---")

    # Filter violations by date, location, vehicle type, gender, race, or violation type
    st.header("Filter violations by date, location, vehicle type, gender, race, or violation type")

    query = "SELECT date_of_stop AS date, description, violation_type, vehicle_type, location, gender, race FROM violations;"
    result = pd.read_sql(query, engine)
    capitalize_column(result)

    filter_option = st.selectbox("Filter by", ["Date", "Violation Type", "Vehicle Type", "Location", "Gender", "Race"])

    if filter_option == "Date": 
        result["Date"] = pd.to_datetime(result["Date"])
        min_date = result["Date"].min().date()
        max_date = result["Date"].max().date()

        with st.form("date_form"):
            start_date, end_date = st.date_input(
                "Select date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            submitted = st.form_submit_button("Apply")

        if submitted:
            result = result[
                (result["Date"].dt.date >= start_date) &
                (result["Date"].dt.date <= end_date)
            ]
    else:
        selected_option = st.selectbox(f"Select {filter_option.lower()}", result[filter_option].unique())

        result = result[result[filter_option] == selected_option]
        st.write(f"Selected: {selected_option} ")

    st.dataframe(result)
    st.write("---")

    # View geographical heatmaps of incident hotspots
    query = "SELECT latitude, longitude FROM violations WHERE accident = 'Yes';"
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    fig = px.density_mapbox(
        result,
        lat="Latitude",
        lon="Longitude",
        radius=15,
        zoom=10,
        mapbox_style="carto-positron",
        color_continuous_scale="Turbo"
    )

    st.header("View geographical heatmaps of incident hotspots")
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # Explore trend charts, bar plots, distribution graphs, and multi-filter insights
    # 1. Trend Chart
    query = """SELECT date_of_stop, COUNT(*) AS incidents
        FROM violations
        GROUP BY date_of_stop
        ORDER BY date_of_stop;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    fig = px.line(
        result,
        x="Date Of Stop",
        y="Incidents",
        title="Incidents Over Time"
    )

    st.header("Trend Charts")
    st.plotly_chart(fig)
    st.write("---")

    # 2. Bar plot
    query = """SELECT year, COUNT(*) AS incidents
        FROM violations
        GROUP BY year
        HAVING COUNT(*) > 500
        ORDER BY year;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    fig = px.bar(
        result,
        x="Year",
        y="Incidents",
        title="Yearly Incident Distribution"
    )

    st.header("Bar Plot")
    st.plotly_chart(fig)
    st.write("---")

    # 3. Distribution graphs
    query = """SELECT MONTH(date_of_stop) AS hour, COUNT(*) AS incidents
        FROM violations
        GROUP BY hour
        ORDER BY hour;
    """
    result = pd.read_sql(query, engine)
    capitalize_column(result)

    fig = px.line(
        result,
        x="Hour",
        y="Incidents",
    ).update_xaxes(
            tickmode="linear",
            tick0=0,
            dtick=1,
            range=[00, 23.5]
        )

    st.header("Distribution graphs")
    st.plotly_chart(fig)
    st.write("---")


    # 4. Multi-filter insights
    query = """SELECT year, COUNT(*) AS accident
        FROM violations
        WHERE accident = 'Yes' AND belts = 'No' AND personal_injury = 'Yes' AND search_conducted = 'Yes'
        GROUP BY year
        HAVING COUNT(*) > 1
        ORDER BY year;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    fig = px.bar(
        result,
        x="Year",
        y="Accident",
        title="Accidents with No Seatbelt Use, Personal Injury, and Searches Conducted",
        labels={
            "Year": "Hour of Day",
            "Accident": "Number of accident"
        }
    )

    fig.update_xaxes( tickmode="linear", tick0=0, dtick=1)

    st.header("Multi-filter insights")
    st.plotly_chart(fig)
    st.write("---")

    st.header("Summary")
    st.write("---")

    # 1. Total violations
    query = "SELECT COUNT(*) AS total_violations FROM violations;"
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    st.header("Total violations")
    st.table(result)

    # 2. Violations involving accidents
    query = "SELECT COUNT(*) AS accident_violations FROM violations WHERE accident = 'Yes';"
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    st.header("Violations involving accidents")
    st.table(result)

    # 3. high-risk zones
    query = """SELECT latitude, longitude, COUNT(*) AS incident_count
        FROM violations
        GROUP BY latitude, longitude
        ORDER BY incident_count DESC
        LIMIT 20;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    st.header("High-risk Zones")
    st.dataframe(result)

    # 4. Most frequently cited vehicle makes/models
    query = """SELECT make, model, COUNT(*) AS incidents
        FROM violations
        GROUP BY make, model
        ORDER BY incidents DESC
        LIMIT 10;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    st.header("Most frequent cited vehicle makes/models")
    st.table(result)