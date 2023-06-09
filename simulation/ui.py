from functools import partial
from typing import Callable

from ursina import Draggable, Button, Entity, color, window, Quad

FIRST_COLOR = color.azure
SECOND_COLOR = color.azure.tint(0.1)


class Controls(Draggable):
    def __init__(self, title: str, click: Callable[[int], None], **kwargs):
        super().__init__(**kwargs)

        # Remove rounded edges of default Quad
        self.model = Quad(radius=0)

        # Size equals to a third of vertical and horizontal space
        self.scale = 1 / 3, 1 / 3

        # Position bottom_right of controls to bottom_right of the window
        self.origin = 0.5, -0.5
        self.position = window.bottom_right

        # Add title
        self.text = title
        self.text_origin = 0, 0.45

        # Add buttons
        self.__on_button_click = click
        self.button_grid = self.__create_buttons(3, 3)

    def __create_buttons(self, lines, columns):
        grid = Entity(
            parent=self,
            scale=(1, 0.8),  # 90% of parent's vertical space
            origin=(-0.5, 0.5),  # grid.top_left at parent.origin
        )
        index = 1
        for y in range(lines, 0, -1):
            for x in range(columns, 0, -1):
                button = Button(
                    text=str(index),
                    color=FIRST_COLOR,
                    parent=grid,
                    origin=(
                        -0.5,
                        0.5,
                    ),  # button.top_left at grid.origin
                    position=(-x / 3, y / 3),
                    scale=(1 / 3, 1 / 3),
                )

                def click(button: Button):
                    # First click
                    location = int(button.text)
                    button.color = SECOND_COLOR
                    button.text = str(location + 9)
                    yield location

                    # Second click
                    location += 9
                    button.disabled = True
                    yield location

                button.on_click = partial(self.__on_button_click, click(button))

                index += 1
        return grid


if __name__ == "__main__":
    from ursina import Ursina

    app = Ursina()

    Controls("Controles", lambda x: print(next(x)))

    app.run()
