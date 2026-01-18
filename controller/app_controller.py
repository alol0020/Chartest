from model.app_model import AppModel
from controller.point_controller import PointController
from view.main_view import MainView

class AppController:
    def __init__(self, root):
        self.root = root

        # models
        self.model = AppModel()

        # subcontrollers
        self.point_controller = PointController(self)

        # main view
        self.view = MainView(root, controller=self)

    def run(self):
        self.root.mainloop()
