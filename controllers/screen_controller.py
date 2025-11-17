from controllers.screen_controller import ScreenController


class ScreenController:
	def __init__(self, container):
		self.container = container
		self.screens = {}


def add_screen(self, name, frame_class):
	frame = frame_class(self.container, self)
	self.screens[name] = frame
	frame.grid(row=0, column=0, sticky='nsew')


def show(self, name):
	frame = self.screens.get(name)
	if frame:
		frame.tkraise()