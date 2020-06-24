from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from player import Player
from drawing import Drawing
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
from settings import NULLX, NULLY, REAL_SCREEN_Y, REAL_SCREEN_X
Window.fullscreen = 'auto'


class Controller(FloatLayout):

    btn_w = Button(text='w', size_hint=(None, None),
                   size=(70, 70),  pos_hint={'x': .2, 'y': 1})
    btn_s = Button(text='s', size_hint=(None, None),
                   size=(70, 70),  pos_hint={'x': .2, 'y': 0})
    btn_a = Button(text='a', size_hint=(None, None),
                   size=(70, 70),  pos_hint={'x': .14, 'y': .5})
    btn_d = Button(text='d', size_hint=(None, None),
                   size=(70, 70),  pos_hint={'x': .26, 'y': .5})

    step_grid = GridLayout(rows=3, cols=3, size_hint=(
        None, None), pos_hint={'x': .04, 'y': .11})

    for elem in (btn_w, btn_a, btn_d, btn_s):
        step_grid.add_widget(Widget())
        step_grid.add_widget(elem)
    step_grid.add_widget(Widget())

    btn_left = Button(text='left', size_hint=(
        None, .1), pos_hint={'x': .82, 'y': .02})
    btn_right = Button(text='right', size_hint=(
        None, .1), pos_hint={'x': .92, 'y': .02})
    btns = (btn_w, btn_s, btn_a, btn_d, btn_left, btn_right)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        self.add_widget(self.step_grid)
        self.fpslbl = Label(text='0', pos_hint={
                            'x': .4, 'y': .4}, font_size=50)
        self.add_widget(self.fpslbl)
        for widget in (self.btn_left, self.btn_right):
            self.add_widget(widget)

    def fps(self, dt):
        fps = int(1/dt)
        self.fpslbl.text = str(fps)


class GameField(BoxLayout):

    def __init__(self, cc, **kwargs):
        super().__init__(**kwargs)
        self.cc = cc
        self.size_hint = (.8, .8)
        self.orientation = 'vertical'
        self.GAME = Widget()
        self.event = Clock.schedule_interval(self.mainloop, 0)
        self.GAME.canvas = Canvas()
        self.player = Player()
        self.drawing = Drawing(self.GAME.canvas, None)
        self.add_widget(self.GAME)
        with self.canvas.after:
            Color(.05, .05, .05)
            Rectangle(pos=(0, 0), size=(NULLX, REAL_SCREEN_Y))
            Color(.05, .01, .15)
            Rectangle(pos=(NULLX, REAL_SCREEN_Y-NULLY),
                      size=(REAL_SCREEN_X-NULLX, NULLY))
            Color(.01, .01, .01)
            Rectangle(pos=(NULLX, 0), size=(REAL_SCREEN_X-NULLX, NULLY))
            Color(.05, .05, .05)
            Rectangle(pos=(REAL_SCREEN_X-NULLX, 0),
                      size=(REAL_SCREEN_X, REAL_SCREEN_Y))

    def mainloop(self, dt):
        # print(dt)
        self.cc.fps(dt)
        # player always work
        self.GAME.canvas.clear()
        self.drawing.background()
        for btn in self.cc.btns:
            if btn.state == 'down':
                self.player.movement(btn.text)
        self.drawing.world(self.player.pos, self.player.angle)
        self.drawing.mini_map(self.player)
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
