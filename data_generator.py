import plotly.express
import pandas
import dash
import dash_core_components
import dash_html_components
from dash.dependencies import Inpurt, Output
from pathlib import Path


# Working directories
path_root = Path(__file__).parent
path_data = path_root / 'data' / '2020-03-27'


# Get Data
entry_data_frame = pandas.read_csv(path_data / 'entry.csv', index_col=0)
# The date column comes in with an silly name, so just rename to DATE
entry_data_frame.rename(columns = {'DATE (YYYY-MM-DD)':'DATE'}, inplace=True)


# Drop irrelevant columns
entry_data_frame.drop(['PSYCHOTIC SYMPTOMS', 'NOTE','THERAPY','WEIGHT','MENSTRUAL CYCLE'], inplace = True, axis=1)

entry_data_frame.set_index('DATE', inplace=True)

# Add multilevel for stack
levels_to_add = [('CATEGORIES','IRRITABILITY'),('CATEGORIES','ANXIETY'),('CATEGORIES','DEPRESSED'),('CATEGORIES','ELEVATED'),('CATEGORIES','SLEEP')]
entry_data_frame.columns = pandas.MultiIndex.from_tuples(levels_to_add)

# The data uses 1 for values when the value is "None", so set 1 to 0, then reduce the size of SLEEP to a max of 4 to keep graph consistent
def size_index(row):
    if row['VALUES'] == 1:
        return 0
    if row['VALUES'] > 4:
        return 4
    return row['VALUES']


# Create records from the columns so that we can plot the data from each column in one plot
entry_data_frame_stacked = entry_data_frame.stack().reset_index().rename(columns={'level_1':'CATEGORIES','CATEGORIES':'VALUES'}).set_index('DATE')

# Add size index
entry_data_frame_stacked['SIZE'] = entry_data_frame_stacked.apply(
    lambda row: size_index(row), axis = 1
)

# Create the graph
height_records = len(entry_data_frame_stacked.index) * 7
fig = plotly.express.scatter(
    entry_data_frame_stacked, 
    x='CATEGORIES',
    y=entry_data_frame_stacked.index, 
    size='SIZE', 
    hover_data=['VALUES'], 
    height=height_records, 
    color='SIZE' 
)

# Style graph
fig.update_layout(
    xaxis=dict(
        side='top'
    ),
    yaxis=dict(
        tickmode='linear',
        type='date'
    ),
    coloraxis_colorbar=dict(
        thicknessmode='pixels',
        thickness=40,
        lenmode='pixels', 
        len=300,
        yanchor='top',
        y=1,
        title='Intensity',
        dtick=1
    )
)

fig.update_traces(
    marker=dict(
        line=dict(
            width=1,
            color='DarkSlateGrey'
        )
    ),
    selector=dict(
        mode='markers'
    )
)

# Display
fig.show()