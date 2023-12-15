import pandas as pd
import numpy as np
import streamlit as st
import altair as alt


plyr_salary = pd.read_csv("Dataset\RankedPlayersbySalaryNonCurr.csv", encoding="unicode_escape")
plyr_points = pd.read_csv("Dataset\RankedPlayersbyPoints.csv", encoding='unicode_escape')
plyr_assists = pd.read_csv("Dataset\RankedPlayersbyAssists.csv", encoding='unicode_escape')
plyr_rebounds = pd.read_csv("Dataset\RankedPlayersbyRebounds.csv", encoding='unicode_escape')

plyr_salary["Price Per Minimum Played_C"] = np.round(plyr_salary['Salary 2023-24'] / 65, 2)

salarytopoints_df = pd.merge(plyr_salary, plyr_points, on= 'Player')
salarytopoints_df["Current Salary vs. Performance_wP"] = np.round(salarytopoints_df['Salary 2023-24'] / (salarytopoints_df['PTS'] * 1.5 + salarytopoints_df['AST'] * 1.25 + salarytopoints_df['TRB'] * 1.25 + salarytopoints_df['G']), 2)
salarytopoints_df["Current Salary vs. Performance_wPFG"] = np.round(salarytopoints_df['Salary 2023-24'] / (salarytopoints_df['PTS'] * 1.5 + salarytopoints_df['AST'] * 1.2 + salarytopoints_df['TRB'] * 1 + salarytopoints_df['G']), 2)
salarytopoints_df["Accuracy Of Pay_wP"] = (salarytopoints_df['Price Per Minimum Played_C'] - salarytopoints_df["Current Salary vs. Performance_wP"])
salarytopoints_df["Accuracy Of Pay_wPFG"] = salarytopoints_df['Price Per Minimum Played_C'] - salarytopoints_df["Current Salary vs. Performance_wPFG"]
salarytopoints_df = salarytopoints_df.sort_values('PTS', ascending= False)

salarytoassists_df = pd.merge(plyr_salary, plyr_assists, on= 'Player')
salarytoassists_df["Current Salary vs. Performance_wA"] = np.round(salarytoassists_df['Salary 2023-24'] / (salarytoassists_df['PTS'] * 1.25 + salarytoassists_df['AST?'] * 1.5 + salarytoassists_df['TRB'] * 1.25 + salarytoassists_df['G']), 2)
salarytoassists_df["Current Salary vs. Performance_wAFG"] = np.round(salarytoassists_df['Salary 2023-24'] / (salarytoassists_df['PTS'] * 1.5 + salarytoassists_df['AST?'] * 1.2 + salarytoassists_df['TRB'] * 1 + salarytoassists_df['G']), 2)
salarytoassists_df["Accuracy Of Pay_wA"] = salarytoassists_df['Price Per Minimum Played_C'] - salarytoassists_df["Current Salary vs. Performance_wA"]
salarytoassists_df["Accuracy Of Pay_wAFG"] = salarytoassists_df['Price Per Minimum Played_C'] - salarytoassists_df["Current Salary vs. Performance_wAFG"]
salarytoassists_df = salarytoassists_df.sort_values('AST?', ascending= False)

salarytorebounds_df = pd.merge(plyr_salary, plyr_rebounds, on= 'Player')
salarytorebounds_df["Current Salary vs. Performance_wR"] = np.round(salarytorebounds_df['Salary 2023-24'] / (salarytorebounds_df['PTS'] * 1.25 + salarytorebounds_df['AST'] * 1.25 + salarytorebounds_df['TRB?'] * 1.5 + salarytoassists_df['G']), 2)
salarytorebounds_df["Current Salary vs. Performance_wRFG"] = np.round(salarytorebounds_df['Salary 2023-24'] / (salarytorebounds_df['PTS'] * 1.5 + salarytorebounds_df['AST'] * 1.2 + salarytorebounds_df['TRB?'] * 1 + salarytoassists_df['G']), 2)
salarytorebounds_df["Accuracy Of Pay_wR"] = salarytorebounds_df['Price Per Minimum Played_C'] - salarytorebounds_df["Current Salary vs. Performance_wR"]
salarytorebounds_df["Accuracy Of Pay_wRFG"] = salarytorebounds_df['Price Per Minimum Played_C'] - salarytorebounds_df["Current Salary vs. Performance_wRFG"]
salarytorebounds_df = salarytorebounds_df.sort_values('TRB?', ascending= False)

salarytopointstop25_df = salarytopoints_df[:26]
salarytoassiststop25_df = salarytoassists_df[:26]
salarytoreboundstop25_df = salarytorebounds_df[:26]

st.set_page_config(
    page_title="Most Valuable Player By The Numbers",
    layout= 'wide'
)

st.write("# Welcome to By The Numbers: The NBA's Most Valuable Player")

st.sidebar.success("Select a page from this menu!")

st.markdown(
    """
    Each year, the NBA deems one player from a playoff team the "Most Valuable Player"...
    
    ...However, just how valuable are players contracts according to their performance?
    
    In this project, we delve into three metrics (Points Per Game, Assists Per Game, Rebounds Per Game) in order to gain a comparison for what metrics are best for determining contract value.
"""
)

st.image('Working_Folder\JoelEmbiidMVP.jpg')

st.write("# Grading Players by Points Per Game vs. Base Weighting Scale")

st.markdown(
    """
    One of the most valuable ways of determining the value of a player is the points they can put up in each game and their average
    (Points Per Game). 
    
    Here we will grade players using all three metrics but give Points Per Game the highest weight to test it against our base weighted
    scales.

    -----------------------------------------------------------------------------------------------------------------------------------

    Our first visualization relies on the fabricated variable of "Price Per Minimum Played_C". This takes the current salary of players and divides
    that salary by the minimum number of games they are required to play (65 games). This then gives us a number that is an average of their value
    for each game hypothetically.

    From this line of thought we then examine player performance based upon the three metrics cited in the introduction, and create two new
    varaibles to stack up against how they are supposed to be played according to their cost to play each game. 
    The first fabricated variable, "Current Salary vs. Performance_wP", puts a higher weight on Points Per Game and follows the following formula:

    Current Season Salary / (Points Per Game * 1.5 + AssistsPerGame * 1.25 + Rebounds Per Game * 1.25 + Games Played

    The second fabricated variable, "Current Salary vs. Performance_wPFG", puts a a weight on the three metrics
    according to how they are weighted in default NBA fantasy leagues and follows the following formula:

    Current Season Salary / (Points Per Game * 1.5 + AssistsPerGame * 1.2 + Rebounds Per Game * 1 + Games Played

    The grouped bar chart below shows the visualizations as follows (from right to left): "Price Per Minimum Played_C", "Current Salary vs. Performance_wP", 
    and "Current Salary vs. Performance_wPFG".
"""
)


# points = alt.Chart(salarytopointstop25_df).mark_circle(size=60).encode(
#     x=alt.X("Price Per Minimum Played_C:Q"),
#     y=alt.Y("Current Salary vs. Performance_wPFG:Q")
# )

# minimumsalarybypointsaccchart = alt.Chart(salarytopointstop25_df, title='Percentage of Accuracy of Contracts Per Game').mark_line().encode(
#     x =alt.X('Player', axis = None),
#     y =alt.Y('Accuracy Of Pay_wP:Q'),
#     tooltip = ['Player', 'Accuracy Of Pay_wP:Q']
# ).mark_point()

melted_data_multibar = pd.melt(salarytopointstop25_df, id_vars=['Player'], value_vars=['Price Per Minimum Played_C', 'Current Salary vs. Performance_wP', 'Current Salary vs. Performance_wPFG'])

# Create a grouped bar chart
group_barchart = alt.Chart(melted_data_multibar, title = "Player Expected Value vs. Actual Value").mark_bar().encode(
    x=alt.X('Player:N', title='Player', sort=alt.EncodingSortField(field='PTS', op='sum', order='descending'), axis=None),
    y=alt.Y('value:Q', title='Values'),
    color=alt.Color('variable:N', title='Metrics'),
    column=alt.Column('variable:N', title=None)
).properties(
    width=150  # Adjust the width of each column
)

group_barchart = group_barchart.configure_legend(
    titleLimit=0,  # Set titleLimit to 0 to show the full variable names
    labelLimit=0,  # Set labelLimit to 0 to show the full variable names
)

melted_data_multiline = pd.melt(salarytopointstop25_df, id_vars=['Player'], value_vars=['Price Per Minimum Played_C', 'Accuracy Of Pay_wP', 'Accuracy Of Pay_wPFG'])

# Create a multi-line plot
line_chart = alt.Chart(melted_data_multiline, title= "Accuracy of Current Salary").mark_line().encode(
    x='Player:N',
    y=alt.Y('value:Q', title='Values'),
    color=alt.Color('variable:N', title='Metrics', scale=alt.Scale(scheme='category10')),
    tooltip=['Player:N', 'value:Q']
).properties(
    width=800,  # Adjust the width of the plot
    height=400  # Adjust the height of the plot
)

line_chart = line_chart.configure_legend(
    titleLimit=0,  # Set titleLimit to 0 to show the full variable names
    labelLimit=0,  # Set labelLimit to 0 to show the full variable names
)

st.altair_chart(group_barchart, use_container_width=False)
st.altair_chart(line_chart, use_container_width=False)