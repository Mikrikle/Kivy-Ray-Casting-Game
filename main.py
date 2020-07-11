from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from player import Player
from drawing import Drawing
from ray_casting import ray_casting
from sprite_objects import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from joystick.joystick import Joystick
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
from settings import NULLX, NULLY, REAL_SCREEN_Y, REAL_SCREEN_X

Window.fullscreen = 'auto'


class Controller(FloatLayout):
    
    # left and right camera rotation buttons
    btn_left = Button(text='left', size_hint=(
        None, .1), pos_hint={'x': .82, 'y': .02})
    btn_right = Button(text='right', size_hint=(
        None, .1), pos_hint={'x': .92, 'y': .02})
    btns = (btn_left, btn_right)
    
    # joystick for movement
    joystick = Joystick(outer_size=1,
                        inner_size= .75,
                        pad_size=.5,
                        pad_line_width=.1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        # add fps counter to the top left corner 
        self.fpslbl = Label(text='0', pos_hint={
                            'x': .4, 'y': .4}, font_size=50)
        self.add_widget(self.fpslbl)
        
        # add camera rotation buttons 
        for widget in (self.btn_left, self.btn_right):
            self.add_widget(widget)

        # add joystick
        Joystick_box = BoxLayout(padding = 25, pos_hint={'x':.015, 'y':.05}, size_hint=(None,None), size=(200,200))
        Joystick_box.add_widget(self.joystick)
        self.add_widget(Joystick_box)

    def fps_label_update(self, dt):
        fps = int(1/dt)
        self.fpslbl.text = str(fps)


class GameField(BoxLayout):

    def __init__(self, overlay, **kwargs):
        super().__init__(**kwargs)
        # creating an interface
        self.controller = overlay
        self.size_hint = (.8, .8)
        self.orientation = 'vertical'
        # starting the gameloop
        self.event = Clock.schedule_interval(self.mainloop, 0)
        # create main canvas
        self.GAME = Widget()
        self.GAME.canvas = Canvas()
        self.add_widget(self.GAME)
        # game classes
        self.player = Player()
        self.sprites = Sprites()
        self.drawing = Drawing(self.GAME.canvas, None)
        
        # draw borders
        with self.canvas.after:
            Color(.05, .05, .05)
            Rectangle(pos=(0, 0), size=(NULLX, REAL_SCREEN_Y))
            Color(.01, .01, .01)
            Rectangle(pos=(NULLX, REAL_SCREEN_Y-NULLY),
                      size=(REAL_SCREEN_X-NULLX, NULLY))
            Color(.01, .01, .01)
            Rectangle(pos=(NULLX, 0), size=(REAL_SCREEN_X-NULLX, NULLY))
            Color(.05, .05, .05)
            Rectangle(pos=(REAL_SCREEN_X-NULLX, 0),
                      size=(REAL_SCREEN_X, REAL_SCREEN_Y))

    def mainloop(self, dt):
        self.controller.fps_label_update(dt)
        self.GAME.canvas.clear()
        self.drawing.background(self.player.angle)
        
        # processing the movement
        for btn in self.controller.btns:
            if btn.state == 'down':
                self.player.lookbehind(btn.text)
            if self.controller.joystick.pad != [0.0,0.0]:
                self.player.movement(self.controller.joystick)
        
        # draw
        walls = ray_casting(self.player, self.drawing.textures)
        self.drawing.world(walls + [obj.object_locate(self.player)
                                    for obj in self.sprites.list_of_objects])
        self.drawing.mini_map(self.player)
        # self.drawing.field(self.player)
        self.drawing.sight()


class GameApp(App):

    def build(self):
        overlay = Controller()
        ach = AnchorLayout(anchor_x='center', anchor_y='center')
        ach.add_widget(GameField(overlay))
        ach.add_widget(overlay)
        return ach


if __name__ == '__main__':
    GameApp().run()
