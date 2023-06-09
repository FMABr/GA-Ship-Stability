import ui
import loading

from ursina import *

app = Ursina()

boat = loading.FerryBoat()
boat.rotation_y = 270

camera = EditorCamera()
camera.position = 500, 300, 0
camera.rotation_x = 30
camera.rotation_y = -90


def add_cargo(location):
    boat.load(loading.Cargo(), next(location))


ui.Controls("Controles", add_cargo)

app.run()
