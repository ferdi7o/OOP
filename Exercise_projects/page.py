from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

Window.clearcolor = (0.5, 0.5, 0.5, 1)

class PageFerdi(App):
    def build(self):
        self.sayac = 0
        layout = FloatLayout()

        self.sayi_label = Label(text=str(self.sayac),
                                font_size=72,
                                size_hint=(0, 0),
                                pos_hint={'x': 0.5, 'y': 0.5}
                                )

        button = Button(text='Bas Bas paralari',
                        size_hint=(0.1, 0.1),
                        pos_hint={'x': 0.5, 'y': 0.1},
                        )

        button.bind(on_press=self.sayiyi_arttir)

        layout.add_widget(button)
        layout.add_widget(self.sayi_label)
        return layout

    def sayiyi_arttir(self, instance):
        self.sayac += 1
        self.sayi_label.text = str(self.sayac)

PageFerdi().run()
