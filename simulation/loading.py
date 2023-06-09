from typing import Type

from ursina import EditorCamera, Entity, color


class Cargo(Entity):
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

    def load(self, container: Type[Cargo], location: int):
        y = self.y - 26

        if location > 9:
            y += 25
            location -= 9

        x = 1 + (location - 1) // 3
        z = location - 3 * ((location - 1) // 3)

        container.world_x = self.cargo_x(x)
        container.world_z = self.cargo_z(z)
        container.world_y = y


if __name__ == "__main__":
    from ursina import Ursina

    app = Ursina()

    camera = EditorCamera()
    camera.position = 500, 300, 100
    camera.rotation_x = 30
    camera.rotation_y = -90

    boat = FerryBoat()
    boat.position = 0, 0, 100
    boat.rotation_y = 270

    boat.load(Cargo(), 1)
    boat.load(Cargo(), 2)
    boat.load(Cargo(), 3)
    boat.load(Cargo(), 12)

    app.run()
