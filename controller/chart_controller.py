from Gui.helpers.mapview import Mapview
from db.db import db_get_chart, db_get_refpoints

nav_commands = ["zoom out", "zoom in", "up", "down", "left", "right"]


class ChartController:
    def __init__(self, app):
        self.mapView = None
        self.app = app
        self.chart_model = app.model.chart_model
        self.panning = False

    def start(self):
        self.load_chart()
        self.refresh_chart()

    def load_chart(self):
        self.chart_model.data = db_get_chart(1)
        self.chart_model.refs = db_get_refpoints(1)
        (h, w, _) = self.chart_model.data.shape
        # self.mapView = Mapview(w, h)
        #
        # self.chart_model.currentSelection = self.chart_model.data[
        #           self.mapView.y_min:self.mapView.y_max,
        #           self.mapView.x_min:self.mapView.x_max
        #       ]
        self.chart_model.reset(w, h)

    def refresh_chart(self):
        self.chart_model.refresh()
        self.app.view.chart_view.refresh(self.chart_model.view)

    def get_aspect(self):
        return self.chart_model.aspect

    def nav(self, command):
        print(command)
        if command == "zoom in":
            self.chart_model.setWidht(self.chart_model.width // 2)
            self.chart_model.setHeight(self.chart_model.height // 2)
        if command == "zoom out":
            self.chart_model.setWidht(self.chart_model.width * 2)
            self.chart_model.setHeight(self.chart_model.height * 2)
        if command == "left":
            self.chart_model.setCenter(
                (self.chart_model.center[0] - self.chart_model.width // 5, self.chart_model.center[1]))
        if command == "right":
            self.chart_model.setCenter((
                self.chart_model.center[0] + self.chart_model.width // 5, self.chart_model.center[1]))
        if command == "up":
            self.chart_model.setCenter(
                (self.chart_model.center[0], self.chart_model.center[1] - self.chart_model.height // 5))
        if command == "down":
            self.chart_model.setCenter(( self.chart_model.center[0],self.chart_model.center[1] + self.chart_model.height // 5))

        self.refresh_chart()

    def on_pan(self,x,y): #Todo: Get initial pos of pan to get the propper motion.
        self.chart_model.setCenter((x*self.chart_model.width,y*self.chart_model.height))
        self.refresh_chart()
