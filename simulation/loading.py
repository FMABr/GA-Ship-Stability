from ursina import Entity, color, EditorCamera


class FerryBoat(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(
            add_to_scene_entities, model="low_poly_cargo_ship.glb", scale=0.1, **kwargs
        )

        self._cargo_hold = [
            (self.x + x, self.y + -26, self.z + z)
            for x in range(-70, 140, 70)
            for z in range(68, 115, 22)
        ]

    def load(self, container: Entity, location: int):
        container.world_position = self._cargo_hold[location - 1]


class Cargo(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(
            add_to_scene_entities,
            model="low_poly_container.glb",
            collider="box",
            color=color.random_color(),
            scale=0.3,
            **kwargs
        )


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

    boat.load(Cargo(), 3)

    app.run()
