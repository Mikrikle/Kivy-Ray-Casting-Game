from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import  Clock
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from player import  Player
from drawing import  Drawing
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout


class Controller(FloatLayout):
    
    btn_w = Button(text='w',size_hint=(.5,.5),pos_hint={'pos_hint_x':.1,'pos_hint_y':.1})
    btn_left = Button(text='left',size_hint=(.5,.5),pos_hint={'pos_hint_x':.2,'pos_hint_y':1})
    btn_right = Button(text='right',size_hint=(.5,.5),pos_hint={'pos_hint_x':.3,'pos_hint_y':1})
    
    btns = (btn_w, btn_left, btn_right)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,.1)
        
        cam_box = []
        step_box = []
        
        for btn in self.btns:
            self.add_widget(btn)
        

class GameField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.GAME = Widget()
        
        self.event = Clock.schedule_interval(self.mainloop, 0)
        self.GAME.canvas = Canvas().before
        self.player = Player()
        self.drawing = Drawing(self.GAME.canvas, None)
        self.add_widget(self.GAME)
        self.cc = Controller()
        self.add_widget(self.cc)
        
    def mainloop(self, dt):
        #print(dt)
        
        # player always work
        self.GAME.canvas.clear()
        self.drawing.background()
        for btn in self.cc.btns:
            if btn.state == 'down':
                self.player.movement(btn.text)
        self.drawing.world(self.player.pos, self.player.angle)
        self.drawing.mini_map(self.player)
        
        
        



class GameApp(App):

    def build(self):
        
        return GameField()


if __name__ == '__main__':
    GameApp().run()