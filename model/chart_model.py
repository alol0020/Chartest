from db.db import db_get_chart, db_get_refpoints


class ChartModel:
    def __init__(self):
        self.chart = []
        self.refs = []
        self.currentSelection = []


