# events.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################



global sprites
global batch
global keyLog
global saveLog
batch = pgl.graphics.Batch()
sprites = {}
keyLog: list = []
saveLog: list = [0 for i in range(9)]

class Window(pgl.window.Window):
    # Initialization of the class
    def __init__(self):
        super(Window, self).__init__(vsync=False)

        self.alive = 1

    # Drawing of the sprites
    def on_draw(self):
        self.render()

    # Rendering of the sprites
    def render(self):
        self.clear()
        # sprites.draw()
        for sprite_name, sprite_obj in sprites.items():
            sprite_obj.draw()
        self.flip()

    # Close window event
    def on_close(self):
        self.alive = 0

    # It holds on running the window
    def run(self):
        k = 0
        import utilities as util
        util.drw_matrix()
        while self.alive:
            self.render()
            # Rectangle Selection Event
            if keyLog:
                for val in keyLog:
                    sprites[val].highlight()
            else: pass
            # sprites[b].hobj.color = util.Colors.blue
            # time.sleep(3)
            # It is used for dispatching events and make pyglet working
            # without hanging out because it can't input more events.
            event = self.dispatch_events()

    def on_key_press(self, symbol, modifiers):
        #  Key event press for enabling the manual selection of squares
        if symbol == key.NUM_1:
            keyLog.append(6)
        elif symbol == key.NUM_2:
            keyLog.append(7)
        elif symbol == key.NUM_3:
            keyLog.append(8)
        elif symbol == key.NUM_4:
            keyLog.append(3)
        elif symbol == key.NUM_5:
            keyLog.append(4)
        elif symbol == key.NUM_6:
            keyLog.append(5)
        elif symbol == key.NUM_7:
            keyLog.append(0)
        elif symbol == key.NUM_8:
            keyLog.append(1)
        elif symbol == key.NUM_9:
            keyLog.append(2)
        else: pass



