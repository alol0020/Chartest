class PointController:
    def __init__(self, app):
        self.app = app
        self.model = app.model.point_model

    def add_point(self, x, y):
        self.model.add_point(x, y)
        self.app.view.point_view.refresh(self.model.points)
