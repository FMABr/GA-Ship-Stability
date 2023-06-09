from ursina import *

app = Ursina()


class LocationChooser(Draggable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.origin = 0.5, -0.5  # Bottom right
        self.scale = 1 / 3, 1 / 3
        self.position = window.bottom_right

        self.buttons = self.__create_buttons(3, 3)

    def __create_buttons(self, lines, columns):
        index = 1
        for y in range(lines):
            for x in range(columns):
                Button(
                    text=str(index),
                    parent=self,
                    origin=(-0.5, 0.5),
                    position=(x, y),
                    scale=(1 / 3, 1 / 3),
                )
                index += 1


Entity(model="Cube")

c = LocationChooser()
cam = EditorCamera()

app.run()
