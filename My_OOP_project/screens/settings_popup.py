from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button


class SettingsPopup(Popup):
    def __init__(self, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.title = "Ayarlar"
        self.size_hint = (0.7, 0.5) # Last: 0.7
        self.auto_dismiss = False
        self.game_screen = game_screen

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # 🎵 Müzik kontrol
        layout.add_widget(Label(text="Müzik Aç/Kapa"))
        self.music_toggle = ToggleButton(text="Açık" if game_screen.bg_music and game_screen.bg_music.state == "play" else "Kapalı",
                                         state="down" if game_screen.bg_music and game_screen.bg_music.state == "play" else "normal")
        self.music_toggle.bind(on_press=self.toggle_music)
        layout.add_widget(self.music_toggle)

        layout.add_widget(Label(text="Müzik Ses Seviyesi"))
        self.music_slider = Slider(min=0, max=1, value=1, step=0.1)
        self.music_slider.bind(value=self.set_music_volume)
        layout.add_widget(self.music_slider)

        # 📢 Anons kontrol
        layout.add_widget(Label(text="Anons Aç/Kapa"))
        self.announce_toggle = ToggleButton(text="Açık", state="down")
        self.announce_toggle.bind(on_press=self.toggle_announcements)
        layout.add_widget(self.announce_toggle)

        layout.add_widget(Label(text="Anons Ses Seviyesi"))
        self.announce_slider = Slider(min=0, max=1, value=1, step=0.1)
        self.announce_slider.bind(value=self.set_announce_volume)
        layout.add_widget(self.announce_slider)

        # Max skor sıfırlama butonu
        self.reset_score_btn = Button(text="🗑️ Max Skoru Sıfırla")
        self.reset_score_btn.bind(on_release=self.reset_max_score)
        layout.add_widget(self.reset_score_btn)

        # ✅ Kapat butonu
        close_btn = Button(text="Kapat")
        close_btn.bind(on_release=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

    # Fonksiyonlar
    def toggle_music(self, instance):
        if self.game_screen.bg_music:
            if self.game_screen.bg_music.state == "play":
                self.game_screen.bg_music.stop()
                instance.text = "Kapalı"
                instance.state = "normal"
            else:
                self.game_screen.bg_music.play()
                instance.text = "Açık"
                instance.state = "down"

    def set_music_volume(self, instance, value):
        if self.game_screen.bg_music:
            self.game_screen.bg_music.volume = value

    def toggle_announcements(self, instance):
        self.game_screen.announcements_enabled = (instance.state == "down")
        instance.text = "Açık" if instance.state == "down" else "Kapalı"

    def set_announce_volume(self, instance, value):
        self.game_screen.announce_volume = value

    # Max skor sıfırlama
    def reset_max_score(self, instance):
        app = self.game_screen.app  # App'e erişim
        app.max_score = 0

        # score.json dosyasını güncelle
        import json
        score_file = "score.json"
        with open(score_file, "w", encoding="utf-8") as f:
            json.dump({"max_score": 0}, f)