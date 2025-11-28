from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.size = (720, 1280)


class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 24
        self.bold = True
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Tam şeffaf
        self.color = (1, 1, 1, 1)  # Beyaz yazı
        self.padding = (20, 20)

        with self.canvas.before:
            # Neon Glow efekti
            Color(0.0, 1.0, 1.0, 0.4)  # Turkuaz mavi ışık
            self.glow = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        self.bind(pos=self.update_glow, size=self.update_glow)

    def update_glow(self, *args):
        self.glow.pos = self.pos
        self.glow.size = self.size


class VideoBackgroundApp(App):
    def build(self):
        layout = FloatLayout()

        # Arka planda video
        video = Video(source="My_OOP_project/assets/video.mp4",
                      state='play',
                      options={'eos': 'loop'},
                      allow_stretch=True,
                      keep_ratio=False,
                      size_hint=(1, 1),
                      pos_hint={'x': 0, 'y': 0})
        layout.add_widget(video)

        # Butonlar için alt merkezde BoxLayout
        button_layout = BoxLayout(orientation='vertical',
                                  size_hint=(0.6, 0.3),
                                  pos_hint={'center_x': 0.5, 'y': 0.05},
                                  spacing=20)

        # Butonlar
        start_button = NeonButton(text='Oyuna Başla')
        about_button = NeonButton(text='Hakkımızda')
        exit_button = NeonButton(text='Çıkış')

        # Buton işlevleri
        start_button.bind(on_release=lambda x: print("Start Game"))  # değiştirebilirsin
        about_button.bind(on_release=lambda x: print("About Screen"))
        exit_button.bind(on_release=lambda x: App.get_running_app().stop())

        # Butonları ekle
        button_layout.add_widget(start_button)
        button_layout.add_widget(about_button)
        button_layout.add_widget(exit_button)

        layout.add_widget(button_layout)

        return layout


if __name__ == '__main__':
    VideoBackgroundApp().run()
