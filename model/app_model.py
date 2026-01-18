from model.chart_model import ChartModel
from model.point_model import PointModel

class AppModel:
    def __init__(self):
        self.point_model = PointModel()
        self.chart_model = ChartModel()
