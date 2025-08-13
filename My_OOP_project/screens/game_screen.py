from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from random import randint
from kivy.core.window import Window

class Cube(Widget):
    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)
        self.size = (50, 50)
        self.pos = (randint(0, Window.width - 50), Window.height)
        with self.canvas:
            Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self, *args):
        x, y = self.pos
        y -= 5  # düşme hızı
        if y <= 0:
            y = 0
        self.pos = (x, y)
        self.rect.pos = self.pos

class CubeGameScreen(Screen):
    def __init__(self, **kwargs):
        super(CubeGameScreen, self).__init__(**kwargs)
        self.cube = None
        self.cube_list = []
        Clock.schedule_once(self.start_game, 1)

    def start_game(self, *args):
        self.cube = Cube()
        self.add_widget(self.cube)
        self.cube_list.append(self.cube)
        Clock.schedule_interval(self.cube.update, 1 / 30)

        # Devam ettikçe burada %51 kontrolü eklenebilir

    def end_game(self):
        self.clear_widgets()

        btn_new = Button(text='Yeni Oyun', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        btn_menu = Button(text='Ana Menü', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.4})

        btn_new.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        btn_menu.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))

        self.add_widget(btn_new)
        self.add_widget(btn_menu)
