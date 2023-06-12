from simulation.ui import Controls
from simulation.loading import FerryBoat, CargoContainer

from ursina import Ursina, EditorCamera


def get_simulation():
    app = Ursina()

    boat = FerryBoat()
    boat.rotation_y = 270

    camera = EditorCamera()
    camera.position = 500, 300, 0
    camera.rotation_x = 30
    camera.rotation_y = -90

    def add_cargo(location):
        boat.load(CargoContainer(), next(location))

    Controls("Controles", add_cargo)

    return app
