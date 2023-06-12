from typing import Type

from ursina import EditorCamera, Entity, color, held_keys, time


class CargoContainer(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(
            add_to_scene_entities,
            model="low_poly_container.glb",
            collider="box",
            color=color.random_color(),
            scale=0.3,
            **kwargs,
        )


class FerryBoat(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(
            add_to_scene_entities, model="low_poly_cargo_ship.glb", scale=0.1, **kwargs
        )

    def cargo_x(self, x: int):
        return self.x + ((x - 2) * 70)

    def cargo_z(self, z: int):
        return self.z + ((22 * z) - 54)

    def cargo_x_relative(self, x: int):
        return -130 + (x * 225)

    def cargo_z_relative(self, z: int):
        # print(f"Z = {z} -> {-130 + ((22 * z) - 54)}")
        return 100 + ((-620 * (z)))

    def load(self, container: Type[CargoContainer], location: int):
        y = self.y - 26

        if location > 9:
            y += 25
            location -= 9

        x = 1 + (location - 1) // 3
        z = location - 3 * ((location - 1) // 3)

        container.world_x = self.cargo_x(x)
        container.world_z = self.cargo_z(z)
        container.world_y = y

    def load_relative(self, container: Type[CargoContainer], location: int):
        container.parent = self
        container.rotation_y = -90
        container.scale = 3

        y = -285

        if location > 9:
            y += 255
            location -= 9

        x = (location - 1) % 3
        z = (location - 1) // 3

        container.x = self.cargo_x_relative(x)
        container.z = self.cargo_z_relative(z)
        container.y = y


if __name__ == "__main__":
    from ursina import Ursina

    app = Ursina()

    camera = EditorCamera()
    camera.perspective_fov = 100
    camera.position = 500, 300, 100
    camera.rotation_x = 30
    camera.rotation_y = -90

    boat = FerryBoat()
    boat.position = 0, 0, 100
    boat.rotation_y = 270

    c1 = CargoContainer()
    c2 = CargoContainer()
    boat.load_relative(c1, 1)
    boat.load_relative(c2, 2)

    def input(key):
        if key == "q":
            boat.rotation_z += 5
        elif key == "e":
            boat.rotation_z -= 5

    # boat.load_relative(CargoContainer(), 2)
    # boat.load_relative(CargoContainer(), 3)
    # boat.load_relative(CargoContainer(), 12)

    app.run()
