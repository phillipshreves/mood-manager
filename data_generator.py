import plotly.express
import pandas
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

# Create records from the columns so that we can plot the data from each column in one plot
entry_data_frame_stacked = entry_data_frame.stack().reset_index().rename(columns={'level_1':'CATEGORIES','CATEGORIES':'VALUES'}).set_index('DATE')
print(entry_data_frame_stacked)

# Create the graph
fig = plotly.express.scatter(entry_data_frame_stacked, x='CATEGORIES', y=entry_data_frame_stacked.index, size='VALUES')
fig.show()