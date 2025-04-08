class EventHandler:
    def __init__(self, controller):
        self.controller = controller

    def processEvent(self, event):
        self.controller.handleEvent(event)
