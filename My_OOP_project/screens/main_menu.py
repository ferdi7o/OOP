from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Ekran çözünürlüğü
Window.size = (720, 1280)


class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 24
        self.bold = True
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.padding = (20, 20)

        with self.canvas.before:
            Color(0.0, 1.0, 1.0, 0.4)  # Neon mavi
            self.glow = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        self.bind(pos=self.update_glow, size=self.update_glow)

    def update_glow(self, *args):
        self.glow.pos = self.pos
        self.glow.size = self.size


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        # Arka planda video
        video = Video(source="assets/video.mp4",
                      state='play',
                      options={'eos': 'loop'},
                      allow_stretch=True,
                      keep_ratio=False,
                      size_hint=(1, 1),
                      pos_hint={'x': 0, 'y': 0})
        layout.add_widget(video)

        # Butonları içeren alt merkez kutu
        button_layout = BoxLayout(orientation='vertical',
                                  size_hint=(0.6, 0.3),
                                  pos_hint={'center_x': 0.5, 'y': 0.05},
                                  spacing=20)

        # Neon butonlar
        start_button = NeonButton(text='Oyuna Başla')
        about_button = NeonButton(text='Hakkımızda')
        exit_button = NeonButton(text='Çıkış')

        # İşlevler
        start_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        about_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'about'))
        exit_button.bind(on_release=lambda x: App.get_running_app().stop())

        # Butonları yerleştir
        button_layout.add_widget(start_button)
        button_layout.add_widget(about_button)
        button_layout.add_widget(exit_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)


# Örnek diğer ekranlar
class GameScreen(Screen):
    pass


class AboutScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(AboutScreen(name='about'))
        return sm


if __name__ == '__main__':
    MyApp().run()
