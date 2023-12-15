import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

plyr_salary = pd.read_csv("Dataset/RankedPlayersbySalaryNonCurr.csv", encoding="unicode_escape")
plyr_points = pd.read_csv("Dataset/RankedPlayersbyPoints.csv", encoding='unicode_escape')

plyr_salary["Price Per Minimum Played_C"] = np.round(plyr_salary['Salary 2023-24'] / 65, 2)

salarytopoints_df = pd.merge(plyr_salary, plyr_points, on= 'Player')
salarytopoints_df["Current Salary vs. Performance_wP"] = np.round(salarytopoints_df['Salary 2023-24'] / (salarytopoints_df['PTS'] * 1.5 + salarytopoints_df['AST'] * 1.25 + salarytopoints_df['TRB'] * 1.25 + salarytopoints_df['G']), 2)
salarytopoints_df["Current Salary vs. Performance_wPFG"] = np.round(salarytopoints_df['Salary 2023-24'] / (salarytopoints_df['PTS'] * 1.5 + salarytopoints_df['AST'] * 1.2 + salarytopoints_df['TRB'] * 1 + salarytopoints_df['G']), 2)
salarytopoints_df["Accuracy Of Pay_wP"] = (salarytopoints_df['Price Per Minimum Played_C'] - salarytopoints_df["Current Salary vs. Performance_wP"])
salarytopoints_df["Accuracy Of Pay_wPFG"] = salarytopoints_df['Price Per Minimum Played_C'] - salarytopoints_df["Current Salary vs. Performance_wPFG"]
salarytopoints_df = salarytopoints_df.sort_values('PTS', ascending= False)


salarytopointstop25_df = salarytopoints_df[:26]

st.set_page_config(
    page_title="Most Valuable Player By The Numbers",
    layout= 'wide'
)

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
    The first variable, "Current Salary vs. Performance_wP", puts a higher weight on Points Per Game and follows the following formula:

    Current Season Salary / (Points Per Game * 1.5 + AssistsPerGame * 1.25 + Rebounds Per Game * 1.25 + Games Played

    The second variable, "Current Salary vs. Performance_wPFG", puts a a weight on the three metrics
    according to how they are weighted in default NBA fantasy leagues and follows the following formula:

    Current Season Salary / (Points Per Game * 1.5 + AssistsPerGame * 1.2 + Rebounds Per Game * 1 + Games Played

    The grouped bar chart below shows the visualizations as follows (from right to left): "Price Per Minimum Played_C", "Current Salary vs. Performance_wP", 
    and "Current Salary vs. Performance_wPFG". The data includes the top 25 players filtered by Points Per Game and the visualizations are sorted from highest
    to lowest going left to right.
"""
)

melted_data_multibar_P = pd.melt(salarytopointstop25_df, id_vars=['Player'], value_vars=['Price Per Minimum Played_C', 'Current Salary vs. Performance_wP', 'Current Salary vs. Performance_wPFG'])


group_barchart_P = alt.Chart(melted_data_multibar_P, title = "Player Expected Value vs. Actual Value - Top Shooters").mark_bar().encode(
    x=alt.X('Player:N', title='Player', sort=alt.EncodingSortField(field='PTS', op='sum', order='descending'), axis=None),
    y=alt.Y('value:Q', title='Values'),
    color=alt.Color('variable:N', title='Metrics'),
    column=alt.Column('variable:N', title=None)
).properties(
    width=150
)

group_barchart_P = group_barchart_P.configure_legend(
    titleLimit=0,  
    labelLimit=0,  
)

st.altair_chart(group_barchart_P, use_container_width=False)

st.markdown(
    """
    As we can see from the visualization above, our forumlas on a grand scheme seem to model the expected averages fairly well.
    The flow of the average cost of each top 25 player almost matches that of what was calculated. These can only be assumed however at a glance, and we must go into further detail.

    -----------------------------------------------------------------------------------------------------------------------------------

    To really get a picture for how accurate the comparision of grading of performance of players against their salaries, we need further
    insight into the data.

    We have created two variables to find out if players are truly overperforming or under performing according to their current season and salary:

    The first variable, "Accuracy Of Pay_wP", takes the current season salary of a player and there current performance cost (weighted by Points Per Game) and finds the difference
    between the two. That formula is as follows:

    "Price Per Minimum Played_C" - "Current Salary vs. Performance_wP"

    The secound variable, "Accuracy Of Pay_wPFG", does the same as the first variable but the current performance cost is weigthed by the NBA Fantasy 
    weight scales. That formula is as follows:

    "Price Per Minimum Played_C" - "Current Salary vs. Performance_wPFG"

    The following visualization is a line plot of the average cost of a player for each game, and the difference between how they are measuring up
    to that cost with their current season performance.
"""
)

melted_data_multiline_P = pd.melt(salarytopointstop25_df, id_vars=['Player'], value_vars=['Price Per Minimum Played_C', 'Accuracy Of Pay_wP', 'Accuracy Of Pay_wPFG'])

line_chart_P = alt.Chart(melted_data_multiline_P, title= "Accuracy of Current Salary - Top Shooters").mark_line().encode(
    x='Player:N',
    y=alt.Y('value:Q', title='Values'),
    color=alt.Color('variable:N', title='Metrics', scale=alt.Scale(scheme='category10')),
    tooltip=['Player:N', 'value:Q']
).properties(
    width=800,
    height=400
)

line_chart_P = line_chart_P.configure_legend(
    titleLimit=0,  
    labelLimit=0,  
)

st.altair_chart(line_chart_P, use_container_width=False)

st.markdown(
    """
    As we can see from our accuracy visuaization, very few top shooting players overperform on their contracts. In fact most top shooting players
    in the top 25 are missing their mark of producing the value of their contract. The average difference in performance of contract from the top 
    25 players by points per game is around $60,000 dollars.
"""
)