from .drawing_controller import DrawingController
from .event_handler import EventHandler

class SuperController:
    def __init__(self, canvas, canvasView):
        self.drawingController = DrawingController(canvas, canvasView)
        self.eventHandler = EventHandler(self.drawingController)
