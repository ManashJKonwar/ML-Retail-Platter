__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from plotly.subplots import make_subplots

class Chart:
    def __init__(self, title, data):
        self.title = title
        self.data = data
    def plot(self):
    	pass

class Bar(Chart):
    def plot(self):
        if self.title is not None and self.data is not None:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=self.data['current']['x-data'],
                y=self.data['current']['y-data'],
                name='Current',
                marker_color='indianred'
            ))
            fig.add_trace(go.Bar(
                x=self.data['predicted']['x-data'],
                y=self.data['predicted']['y-data'],
                name='Predicted',
                marker_color='lightsalmon'
            ))

            # Here we modify the tickangle of the xaxis, resulting in rotated labels.
            fig.update_layout(barmode='group', xaxis_tickangle=-45, title=self.title)
            return fig

class Line(Chart):
    def plot(self):
        if self.title is not None and self.data is not None:
            fig = make_subplots(rows=2, subplot_titles=('Current Scatter','Predicted Scatter'))
            fig.add_trace(go.Scatter(
                x=self.data['current']['x-data'], 
                y=self.data['current']['y-data'],
                name='Current'),
            row=1, col=1) 
            fig.add_trace(go.Scatter(
                x=self.data['predicted']['x-data'], 
                y=self.data['predicted']['y-data'],
                name='Predicted'),
            row=2, col=1) 
            
            # Here we update line chart mode
            fig.update_traces(mode='markers+lines')
            return fig

class Pie(Chart):
    def plot(self):
        if self.title is not None and self.data is not None:
            data = {'Name':['Current','Predicted'],'Value':[abs(sum(self.data['current']['y-data'])), abs(sum(self.data['predicted']['y-data']))]}
            df_processed = pd.DataFrame(data)
            fig = px.pie(df_processed, values='Value', names='Name', color_discrete_sequence=px.colors.sequential.RdBu)

            # Here we add title to the pie chart
            fig.update_layout(title=self.title)
            return fig