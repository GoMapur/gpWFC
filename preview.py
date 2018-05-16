import pyglet
import pyglet.text
import numpy as np
from pyglet.window import key

class PreviewWindow(pyglet.window.Window):
	def __init__(self, model, observer, propagator):
		super().__init__(width=512, height=512)
		self.model = model
		self.observer = observer
		self.propagator = propagator
		self.grid = self.model.build_grid()
		self.grid_array = grid.get()
		self.scale = 24
		self.label = pyglet.text.Label(
			font_name='DejaVu Sans Mono',
			font_size=self.scale,
			multiline=True,
			anchor_y='top',
			width=512,
			y=512,
		)

	def get_char(self, bits):
		tiles = self.model.get_tiles(bits)
		if len(tiles) == 1:
			return tiles[0].char
		elif len(tiles) < len(self.model.tiles):
			return str(len(tiles))
		else:
			return '?'

	def on_draw(self):
		self.clear()

		self.label.text = '\n'.join(''.join(self.get_char(tile) for tile in row) for row in self.grid_array)
		self.label.draw()

	def on_key_press(self, symbol, modifiers):
		if symbol == key.SPACE:
			status, index, collapsed = self.observer.observe(self.grid)
			if status == 'continue':
				self.propagator.propagate(self, self.grid, index, collapsed)
			self.grid.get(ary=self.grid_array)
