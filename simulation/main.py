from ursina import *
import ui

app = Ursina()

ui.Controls("Controles", lambda x: print(next(x)))

app.run()
