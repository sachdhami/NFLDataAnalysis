"""
Submission: geospatials.py as part of the CSE163 Final Project
CSE163 Section A: Lucas Swanson, Sachin Dhami, Zach Rinehart

geospatials.py is a python script that takes some datasets in .csv format and
plots them according to a shape file of the United States. It can produce
plots of player counts given their high school location and position, and
plot the totals accordingly.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def main():
    """
    main() reads in the necessary files to begin plotting the data.
    """
    shape_data = gpd.read_file("states.geojson")
    basic_stats = pd.read_csv("Basic_Stats.csv")
    basic_stats.dropna(subset=["High School Location"], inplace=True)
    

    merged = shape_data.merge(basic_stats, left_on='STUSPS',
                          right_on='High School Location', how='left')
    
    
    player_count_states_df = get_players_per_state(merged)
    
    """
    position is the default position variable for plot_counts_bypos().
    Valid inputs: ['G' 'C' 'DE' 'RB' 'OLB' 'FB' 'P' 'QB' 'OG' 'NT' 'TE' 'SAF'
                   'T' 'WR' 'LS' 'DB' 'MLB' 'SS' 'CB' 'ILB' 'OT' 'LB' 'DT'
                   'K' 'FS' nan].
    """
    position = "QB"
    
    plot_counts(merged)
    percent = False
    plot_counts_bypos(merged, player_count_states_df, position, percent)


def plot_counts(merged):
    """
    plot_counts() takes in a merged shape file and csv dataset as a parameter.
    It dissolves the data by state with aggfunc count to plot the total number
    of players from each state.
    """
    counts = get_players_per_state(merged)
    fig, ax = plt.subplots(1, figsize=(20, 10))
    merged.plot(ax=ax, color = '#EEEEEE')
    counts.plot(ax=ax, column='High School Location', legend=True)
    plt.title("U.S. NFL Players Location Density by High School Location")
    plt.savefig("map.png")
    

def plot_counts_bypos(merged, totals, pos, percent):
    """
    plot_counts_bypos() takes in a merged shape file and csv dataset, the
    dissolved dataset (totals), a string pos which represents an NFL position,
    and a boolean value called percent as parameters. It will filter out all
    players that don't play at the specified position, then produce the same
    plot as plot_counts(). If percent is true, it will plot the percentage of
    players in each state that play the specified position.
    """
    positions_abv = merged['Position'].unique()
    #check if position input is valid. If not, pass through the function.
    if pos not in positions_abv:
        print("Invalid position input.")
        pass
    posmask = merged['Position'] == pos
    new_merged = merged[posmask]
    counts = get_players_per_state(new_merged)
    if percent:          
        counts['High School Location'] = counts[
            'High School Location'] / totals['High School Location']
    counts.dropna(subset=["High School Location"], inplace=True)
    #plot data
    fig, ax = plt.subplots(1, figsize=(20, 10))
    merged.plot(ax=ax, color = '#EEEEEE')
    counts.plot(ax=ax, column="High School Location", legend=True)
    plt.title(pos.upper() 
              + " Player High School Location by State (percent = "
              + str(percent) + ")" )
    plt.savefig("position_counts.png")
    

def get_players_per_state(data):
    """
    get_players_by_state() takes a dataset as a parameter. It dissolves the
    data by state, and returns a dataset counts that represents the number of
    players from each state.
    """
    counts = data.dissolve(by='STUSPS', aggfunc='count')
    return(counts)
    

def test_plot_count_bypos(shape_data):
    """
    test function for plot_count_bypos
    """
    test = pd.read_csv("test_file.csv")
    test_merged = shape_data.merge(test, left_on='STUSPS',
                          right_on='High School Location', how='left')
    
    test_totals = get_players_per_state(test_merged)
    test_percent = True
    test_pos = "QB"
    return plot_count_bypos(test_merged, test_totals, test_pos, test_percent)
    

if __name__ == "__main__":
    main()