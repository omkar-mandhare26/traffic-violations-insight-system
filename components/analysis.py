from utils.capitalize_column import capitalize_column
import plotly.express as px
import pandas as pd

def analysis_question(st,engine):
    st.title("Analysis Questions")
    st.write("---")

    # 1. What are the most common violations?
    query = """SELECT description, COUNT(*) as count 
        FROM violations 
        GROUP BY description 
        ORDER BY COUNT(*) 
        DESC LIMIT 10;
    """
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    result["Description_short"] = result["Description"].apply(
        lambda x: " ".join(x.split()[:5]) + "......"
    )

    fig = px.treemap(
        result,
        path=['Description_short'],
        values="Count",
        hover_data=['Description_short'],
        title="Top 10 common violations"
    )

    st.header("1. What are the most common violations?")
    st.table(result[["Description", "Count"]])
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # 2. Which areas or coordinates have the highest traffic incidents?
    st.header("2. Which areas or coordinates have the highest traffic incidents?")

    option = st.selectbox("Filter by", ["Area", "Coordinates"])
    if option == "Coordinates":
        query = """SELECT CONCAT(latitude, ', ', longitude) AS coordinates, COUNT(*) AS incident_count
            FROM violations
            GROUP BY latitude, longitude
            ORDER BY COUNT(*) DESC
            LIMIT 10;
        """
    else:
        query = """SELECT location, COUNT(*) AS incident_count
            FROM violations
            GROUP BY location
            ORDER BY COUNT(*) DESC
            LIMIT 10;
        """

    result = pd.read_sql(query,engine)
    capitalize_column(result)

    column = "Coordinates" if option == "Coordinates" else "Location"
    fig = px.bar(
        result,
        x=column,
        y='Incident Count',
        title="Top 10 Traffic Incidents"
    )

    st.table(result)
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # 3. Do certain demographics correlate with specific violation types?
    query = """SELECT race, gender, violation_type, COUNT(*) as count 
        FROM violations 
        GROUP BY race, gender, violation_type 
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """

    result = pd.read_sql(query,engine)
    capitalize_column(result)

    fig = px.sunburst(
        result,
        path=["Violation Type", "Race", "Gender"],
        values="Count",
        title="Demographics correlation with violation types"
    )

    st.header("3. Do certain demographics correlate with specific violation types?")
    st.table(result)
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # 4. How does violation frequency vary by time of day, weekday, or month?
    st.header("4. How does violation frequency vary by time of day, weekday, or month?")

    option = st.selectbox("Filter by", [ "Month", "Weekday", "Day"])
    if option == "Day": 
        query = """SELECT EXTRACT(HOUR FROM time_of_stop) AS hour, COUNT(*) AS count 
            FROM violations 
            GROUP BY EXTRACT(HOUR FROM time_of_stop) 
            ORDER BY hour;
        """
        result = pd.read_sql(query,engine)
        capitalize_column(result)

        fig = px.line(
            result,
            x= 'Hour',
            y= 'Count',
            title=f"How does violation frequency vary by {option}"
        )
        fig.update_xaxes(
            tickmode="linear",
            tick0=0,
            dtick=1,
            range=[00, 23.5]
        )
    elif option == "Weekday":
        weekday_order = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]

        query = """SELECT DAYNAME(date_of_stop) AS weekday, COUNT(*) AS count 
            FROM violations 
            GROUP BY DAYNAME(date_of_stop);
        """
        result = pd.read_sql(query,engine)
        capitalize_column(result)

        result["Weekday"] = pd.Categorical(result["Weekday"],categories=weekday_order,ordered=True)
        result = result.sort_values("Weekday")
        result = result.reset_index(drop=True)

        fig = px.line(
            result,
            x= 'Weekday',
            y= 'Count',
            title=f"How does violation frequency vary by {option}"
        )
    else:
        month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        query = """SELECT MONTHNAME(date_of_stop) AS month, COUNT(*) AS count 
            FROM violations 
            GROUP BY MONTHNAME(date_of_stop);
        """
        result = pd.read_sql(query,engine)
        capitalize_column(result)

        result["Month"] = pd.Categorical(result["Month"],categories=month_order,ordered=True)
        result = result.sort_values("Month")
        result = result.reset_index(drop=True)

        fig = px.line(
            result,
            x= 'Month',
            y= 'Count',
            title=f"How does violation frequency vary by {option}"
        )

    st.table(result)
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # 5.What types of vehicles are most often involved in violations?
    query = """SELECT vehicle_category, COUNT(*) as count 
        FROM violations 
        GROUP BY vehicle_category 
        ORDER BY count DESC 
        LIMIT 10;
    """
    result = pd.read_sql(query, engine)
    capitalize_column(result)

    fig = px.bar(
        result,
        x="Vehicle Category",
        y="Count",
        title="Top 10 vehicles types invovled in violations",
        log_y=True
    )

    st.header("5.What types of vehicles are most often involved in violations?")
    st.table(result)
    st.plotly_chart(fig, width="stretch")
    st.write("---")

    # 6.How often do violations involve accidents, injuries, or vehicle damage?
    query = "SELECT accident, personal_injury, property_damage FROM violations;"
    result = pd.read_sql(query,engine)
    capitalize_column(result)

    result = result.eq("Yes").sum().reset_index(name="value").rename(columns={"index": "name"})
    capitalize_column(result)

    fig = px.bar(
        result,
        x="Name",
        y="Value",
        title="Violations involving accidents, injuries & vehicle damage"
    )

    st.header("6.How often do violations involve accidents, injuries, or vehicle damage?")
    st.dataframe(result)
    st.plotly_chart(fig)
    st.write("---")