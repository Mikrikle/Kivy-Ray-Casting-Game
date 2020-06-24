from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import  Clock
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from player import  Player
from drawing import  Drawing
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import  GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Window.fullscreen = 'auto'


class Controller(FloatLayout):
    
    btn_w = Button(text='w', size_hint=(None, None), size=(50,50),  pos_hint={'x':.2, 'y':1} )
    btn_s = Button(text='s', size_hint=(None, None), size=(50,50),  pos_hint={'x':.2, 'y':0} )
    btn_a = Button(text='a', size_hint=(None, None), size=(50,50),  pos_hint={'x':.14, 'y':.5} )
    btn_d = Button(text='d', size_hint=(None, None), size=(50,50),  pos_hint={'x':.26, 'y':.5} )
    
    step_grid = GridLayout(rows=3, cols=3, size_hint=(None, None), pos_hint={'x':.1, 'y':.05} )
    step_grid.add_widget(Widget())
    step_grid.add_widget(btn_w)
    step_grid.add_widget(Widget())
    step_grid.add_widget(btn_a)
    step_grid.add_widget(Widget())
    step_grid.add_widget(btn_d)
    step_grid.add_widget(Widget())
    step_grid.add_widget(btn_s)
    step_grid.add_widget(Widget())
    
    
    
    btn_left = Button(text='left', size_hint=(None, .1), pos_hint={'x':.7, 'y':.02} )
    btn_right = Button(text='right', size_hint=(None, .1), pos_hint={'x':.85, 'y':.02} )
    
    btns = (btn_w, btn_s, btn_a, btn_d, btn_left, btn_right)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,1)

        self.add_widget(self.step_grid)
        
        for widget in (self.btn_left, self.btn_right):
            self.add_widget(widget)

        

class GameField(BoxLayout):
    def fps(self, dt):
        fps = int(1/dt)
        self.FPSlbl.text = str(fps)
    
    def __init__(self,cc, **kwargs):
        super().__init__(**kwargs)
        self.cc = cc
        self.size_hint = (.8, .8)
        self.orientation = 'vertical'
        self.GAME = Widget()
        self.FPSlbl = Label(text='0', size_hint=(None, None), pos_hint={'x':.9, 'y':.5} )
        self.add_widget(self.FPSlbl)
        self.event = Clock.schedule_interval(self.mainloop, 0)
        self.GAME.canvas = Canvas()
        self.player = Player()
        self.drawing = Drawing(self.GAME.canvas, None)
        self.add_widget(self.GAME)

        
        
    def mainloop(self, dt):
        #print(dt)
        self.fps(dt)
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