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
    btn_left = Button(text='left', size_hint=(
        None, .1), pos_hint={'x': .82, 'y': .02})
    btn_right = Button(text='right', size_hint=(
        None, .1), pos_hint={'x': .92, 'y': .02})
    btns = (btn_left, btn_right)
    
    joystick = Joystick(outer_size=1,
                        inner_size= .75,
                        pad_size=.5,
                        pad_line_width=.1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        #self.add_widget(self.step_grid)
        self.fpslbl = Label(text='0', pos_hint={
                            'x': .4, 'y': .4}, font_size=50)
        self.add_widget(self.fpslbl)
        for widget in (self.btn_left, self.btn_right):
            self.add_widget(widget)

        Joystick_box = BoxLayout(padding = 25, pos_hint={'x':.015, 'y':.05}, size_hint=(None,None), size=(200,200))
        Joystick_box.add_widget(self.joystick)
        self.add_widget(Joystick_box)

    def fps(self, dt):
        fps = int(1/dt)
        self.fpslbl.text = str(fps)


class GameField(BoxLayout):

    def __init__(self, cc, **kwargs):
        super().__init__(**kwargs)
        self.controller = cc
        self.size_hint = (.8, .8)
        self.orientation = 'vertical'
        self.GAME = Widget()
        self.event = Clock.schedule_interval(self.mainloop, 0)
        self.GAME.canvas = Canvas()
        self.player = Player()
        self.sprites = Sprites()
        self.drawing = Drawing(self.GAME.canvas, None)
        self.add_widget(self.GAME)
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
        # print(dt)
        self.controller.fps(dt)
        # player always work
        self.GAME.canvas.clear()
        self.drawing.background(self.player.angle)
        for btn in self.controller.btns:
            if btn.state == 'down':
                self.player.lookbehind(btn.text)
            if self.controller.joystick.pad != [0.0,0.0]:
                self.player.movement(self.controller.joystick)
        
        walls = ray_casting(self.player, self.drawing.textures)
        self.drawing.world(walls + [obj.object_locate(self.player)
                                    for obj in self.sprites.list_of_objects])
        self.drawing.mini_map(self.player)

        # self.drawing.field(self.player)

        self.drawing.sight()


class GameApp(App):

    def build(self):
        cc = Controller()
        ach = AnchorLayout(anchor_x='center', anchor_y='center')
        ach.add_widget(GameField(cc))
        ach.add_widget(cc)
        return ach


if __name__ == '__main__':
    GameApp().run()
