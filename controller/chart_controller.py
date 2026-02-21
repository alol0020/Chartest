from Gui.helpers.mapview import Mapview
from db.db import db_get_chart, db_get_refpoints

nav_commands = ["zoom out", "zoom in", "up", "down", "left", "right"]


class ChartController:
    def __init__(self, app):
        self.mapView = None
        self.app = app
        self.chart_model = app.model.chart_model
        self.panning = False
        self.pan_coordinates = [None,None]

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
    def set_frame_size(self,size):
        self.chart_model.frame_size = size

    def nav(self, command):
        if command == "zoom in":
            self.chart_model.setWidht(self.chart_model.width // 2)
            self.chart_model.setHeight(self.chart_model.height // 2)
        if command == "zoom out":
            self.chart_model.setWidht(self.chart_model.width * 2)
            self.chart_model.setHeight(self.chart_model.height * 2)
        if command == "left":
            self.chart_model.setCenter(
                [self.chart_model.center[0] - self.chart_model.width // 5, self.chart_model.center[1]])
        if command == "right":
            self.chart_model.setCenter([
                self.chart_model.center[0] + self.chart_model.width // 5, self.chart_model.center[1]])
        if command == "up":
            self.chart_model.setCenter(
                [self.chart_model.center[0], self.chart_model.center[1] - self.chart_model.height // 5])
        if command == "down":
            self.chart_model.setCenter([ self.chart_model.center[0],self.chart_model.center[1] + self.chart_model.height // 5])

        self.refresh_chart()

    def on_pan_start(self,x,y):
        self.pan_coordinates[0] = x
        self.pan_coordinates[1] = y
    def on_pan_stop(self):
        self.pan_coordinates = [None, None]
    def on_pan(self,x,y):
        if self.pan_coordinates[0] is None or self.pan_coordinates[1] is None:
            return 
        dx = (self.pan_coordinates[0] - x) * self.chart_model.width / self.chart_model.frame_size[0]
        dy = (self.pan_coordinates[1] - y) *  self.chart_model.height / self.chart_model.frame_size[1]

        self.pan_coordinates[0] = x
        self.pan_coordinates[1] = y

        center = self.chart_model.center
        center[0]= center[0]+dx
        center[1]= center[1]+dy

        self.chart_model.setCenter(center)
        self.refresh_chart()
