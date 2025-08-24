from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class PageFerdi(App):
    def build(self):
        self.label = Label(text="Hoş geldiniz, Kral Ferdi 👑")
        button = Button(text="Tahta Bas")
        button.bind(on_press=self.butona_basildi)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def butona_basildi(self, instance):
        self.label.text = "Kral Ferdi tahta bastı! 👑🔥"

PageFerdi().run()
