import plotly.express
import pandas
from pathlib import Path


# Working directories
path_root = Path(__file__).parent
path_data = path_root / 'data' / '2020-03-27'


# Get Data
entry_data_frame = pandas.read_csv(path_data / 'entry.csv', index_col=1)
# The date column comes in with an silly name, so just rename to DATE
entry_data_frame.index.rename('DATE', inplace=True)
#entry_data_frame.set_index('DATE', inplace = True)
print(entry_data_frame)


# Drop irrelevant columns
entry_data_frame.drop(['ID', 'PSYCHOTIC SYMPTOMS', 'NOTE','THERAPY','WEIGHT','MENSTRUAL CYCLE'], inplace = True, axis=1)
print(entry_data_frame)


# Create records from the columns so that we can plot the data from each column in one plot
entry_data_frame_stacked = (entry_data_frame.stack().reset_index(name='VALUES').set_index('DATE').rename(columns={'level_1':'CATEGORIES'}))
print(entry_data_frame_stacked)


# Create the graph
#fig = plotly.express.bar(entry_data_frame, y='DATE')
#fig = plotly.express.scatter(entry_data_frame, x='CATEGORIES', y='DATE')
#fig = plotly.express.scatter_matrix(data_entry)
#fig.show()