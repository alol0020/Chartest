from Gui.helpers.mapview import Mapview
from db.db import db_get_chart, db_get_refpoints
from model.chart_model import ChartModel


class MapController:
    def __init__(self, app):
        self.mapView = None
        self.app = app
        self.chart_model = app.model.chart_model


    def start(self):
        self.load_chart()
        self.refresh_chart()

    def load_chart(self):
        self.chart_model.data = db_get_chart(1)
        self.chart_model.refs = db_get_refpoints(1)
        (h, w, _) = self.chart_model.data.shape
        self.mapView = Mapview(w, h)

        self.chart_model.currentSelection = self.chart_model.data[
                  self.mapView.y_min:self.mapView.y_max,
                  self.mapView.x_min:self.mapView.x_max
              ]


    def refresh_chart(self):
        self.app.view.chart_view.refresh(self.chart_model.currentSelection)


    def get_aspect(self):
        return self.mapView.aspect