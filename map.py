import plotly.graph_objects as go
import pandas as pd
import plotly.offline
import os
mapbox_access_token = open('mapbox_token').read()
cwd = os.getcwd()
df = pd.read_csv(cwd + '\\Object_detection\\processes\\csv_data\\final_ships.csv')
site_lat = df.lan
site_lon = df.lon
locations_name = df.text

fig = go.Figure()
		
fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=1
        ),
        text=locations_name,
        hoverinfo='text'	
    ))

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
		text=locations_name,
        hoverinfo='text'
    ))

fig.update_layout(
    title='Global Ship Positioning',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=22,
            lon=69
        ),
        pitch=0,
        zoom=3,
        style='light'
    ),
)
#fig.show()


################################# The map is stored in the "fig" variable ##################


##################################Standalone Window in PyQt5################################
import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets


class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig, exec=True):
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        super().__init__()

        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp.html"))
        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))
        self.setWindowTitle("Map")
        self.show()

        if exec:
            self.app.exec_()

    def closeEvent(self, event):
        os.remove(self.file_path)
#############################################################################################

#######################Display Window using PlotlyViewer PyQt class##########################
win = PlotlyViewer(fig)

#ref. https://plotly.com/python/scattermapbox/
