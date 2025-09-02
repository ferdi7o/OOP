# Düzeltilmiş TowerBlockGame (tam sınıf)
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.resources import resource_add_path
from kivy.animation import Animation

from pythonProject.OOP.My_OOP_project.screens.settings_popup import SettingsPopup

resource_add_path("assets")

BLOCK_WIDTH = 80
BLOCK_HEIGHT = 70
BLOCK_SPEED = 4
FALL_SPEED = 7

class ImageButton(ButtonBehavior, Image):
    pass

class Block(Widget):
    def __init__(self, pos, image_source="assets/tower1.png", **kwargs):
        super().__init__(**kwargs)
        self.size = (BLOCK_WIDTH, BLOCK_HEIGHT)
        self.pos = pos

        self.image = Image(
            source=image_source,
            size=self.size,
            pos=self.pos,
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.image)

    def update_pos(self, pos):
        self.pos = pos
        self.image.pos = pos

class TowerBlockGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- genel ayarlar ---
        self.announcements_enabled = True
        self.announce_volume = 1.0

        # --- layout (tüm görseller burada olacak) ---
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # --- skor etiketleri (tek tanım, layout içine ekliyoruz) ---
        # self.score_label
        self.score_label = Label(
            text="Skor: 0",
            size_hint=(None, None),
            size=(150, 40),
            pos=(10, Window.height - 50),
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.score_label)

        # self.max_score_label
        self.max_score_label = Label(
            text="Max Skor: 0",
            size_hint=(None, None),
            size=(150, 40),
            pos=(Window.width - 160, Window.height - 50),
            font_size='20sp',
            color=(1, 1, 0, 1)
        )
        self.layout.add_widget(self.max_score_label)

        # --- ayarlar ikonu (ikon dosyan varsa background veya ImageButton tercih et) ---
        # Eğer assets/settings.png varsa ImageButton kullan:
        try:
            self.settings_icon = ImageButton(
                source="assets/settings.png",
                size_hint=(None, None),
                size=(48, 48),
                pos_hint={"right": 0.98, "top": 0.98}
            )
        except Exception:
            # fallback: text button
            self.settings_icon = Button(
                text="⚙️",
                size_hint=(None, None),
                size=(48, 48),
                pos_hint={"right": 0.98, "top": 0.98},
                border=(0,0,0,0)
            )
        self.settings_icon.bind(on_release=self.open_settings_popup)
        self.layout.add_widget(self.settings_icon)

        # --- müzik (yükle fakat oynatma kontrolünü on_enter/start_game'e bırak) ---
        self.bg_music = SoundLoader.load("music/city_sound.flac")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5

        # --- announcement (anons) seslerini yükle ve dict'te tut ---
        self.announcement_sounds = {
            "legendary": SoundLoader.load("music/legendary.wav"),
            "amazing": SoundLoader.load("music/amazing.wav"),
            "super": SoundLoader.load("music/super.wav"),
            "nice": SoundLoader.load("music/nice.wav"),
            "brick_fall": SoundLoader.load("music/brick_fall.wav"),
        }
        # apply initial volume
        for s in self.announcement_sounds.values():
            if s:
                s.volume = self.announce_volume

        # oyun değişkenleri
        self.base_blocks = []
        self.moving_block = None
        self.moving_right = True
        self.game_running = False
        self.is_falling = False
        self.platform_x = None

        # input bind
        self.bind(on_touch_down=self.drop_block)

        # NOTE: artık __init__ içinde start_game() çağırmıyoruz.
        # Oyun ekranı aktif olduğunda (on_enter) start_game() çalışacak.

    # --- settings popup ---
    def open_settings_popup(self, *args):
        popup = SettingsPopup(self)
        popup.open()

    # --- screen lifecycle ---
    def on_enter(self):
        # ekran aktif olduğunda oyunu başlat ve müziği aç
        if not self.game_running:
            self.start_game()
        if self.bg_music and self.bg_music.state != "play":
            self.bg_music.play()

    def on_leave(self):
        # ekran dışına çıkıldığında müziği durdur, oyun döngüsünü durdur
        if self.bg_music and self.bg_music.state == "play":
            self.bg_music.stop()
        self.game_running = False
        # temiz zamanlayıcılar
        Clock.unschedule(self.move_block)
        Clock.unschedule(self.fall_block)

    # --- geri bildirim / anons çalma ---
    def show_feedback(self, message, sound_key=None, volume=1.0):
        # anons açık mı kontrol et
        if sound_key and not self.announcements_enabled:
            sound_key = None

        if message:
            label = Label(
                text=message,
                font_size='40sp',
                color=(1, 1, 0, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.7},
                opacity=0
            )
            self.layout.add_widget(label)
            anim = Animation(opacity=1, duration=0.3) + Animation(opacity=0, duration=0.5)
            anim.bind(on_complete=lambda *a: self.layout.remove_widget(label))
            anim.start(label)

        if sound_key:
            sound = self.announcement_sounds.get(sound_key)
            if sound:
                sound.volume = self.announce_volume * volume
                sound.play()

    # --- oyun başlat / blok işlemleri ---
    def start_game(self):
        # max score güncelle
        self.app = App.get_running_app()
        self.max_score = getattr(self.app, "max_score", 0)
        self.max_score_label.text = f"Max Skor: {self.max_score}"

        # oyun değişkenleri
        self.game_running = True
        self.is_falling = False
        self.moving_right = True

        # ilk bloğu bırak
        Clock.schedule_once(self.drop_first_block, 0.8)

    def drop_first_block(self, dt):
        # önce varsa eski blokları kaldır (güvenlik)
        if self.moving_block:
            try: self.layout.remove_widget(self.moving_block)
            except Exception: pass

        self.moving_block = Block(pos=(0, Window.height - 50))
        self.layout.add_widget(self.moving_block)
        self.moving_right = True
        self.is_falling = False
        Clock.schedule_interval(self.move_block, 1 / 60)

    def move_block(self, dt):
        if not self.game_running or self.is_falling or not self.moving_block:
            return

        x, y = self.moving_block.pos
        if self.moving_right:
            x += BLOCK_SPEED
            if x + BLOCK_WIDTH >= Window.width:
                self.moving_right = False
        else:
            x -= BLOCK_SPEED
            if x <= 0:
                self.moving_right = True

        self.moving_block.update_pos((x, y))

    def drop_block(self, *args):
        if not self.game_running or self.is_falling or not self.moving_block:
            return
        self.is_falling = True
        Clock.unschedule(self.move_block)
        Clock.schedule_interval(self.fall_block, 1 / 60)

    def fall_block(self, dt):
        if not self.moving_block:
            return False

        x, y = self.moving_block.pos
        y -= FALL_SPEED

        if len(self.base_blocks) == 0:
            if y <= 0:
                y = 0
                self.platform_x = self.moving_block.pos[0]
                self.moving_block.update_pos((self.platform_x, y))
                self.base_blocks.append(self.moving_block)
                self.score = 1
                self.score_label.text = f"Skor: {self.score}"
                self.spawn_new_block()
                return False
        else:
            last_block = self.base_blocks[-1]
            lx, ly = last_block.pos
            if y <= ly + BLOCK_HEIGHT:
                y = ly + BLOCK_HEIGHT
                overlap = self.get_overlap_ratio(self.moving_block.pos[0], last_block.pos[0])

                if overlap >= 0.55:
                    self.moving_block.update_pos((x, y))
                    # brick fall feedback
                    self.show_feedback("", sound_key="brick_fall", volume=0.3)
                    if overlap >= 0.95:
                        self.show_feedback("Legendary!", sound_key="legendary")
                    elif overlap >= 0.9:
                        self.show_feedback("Amazing!", sound_key="amazing")
                    elif overlap >= 0.8:
                        self.show_feedback("Super!", sound_key="super")
                    elif overlap >= 0.75:
                        self.show_feedback("Nice!", sound_key="nice")

                    # max block logic
                    max_blocks = int((Window.height * 0.6) // BLOCK_HEIGHT)
                    if len(self.base_blocks) >= max_blocks:
                        bottom_block = self.base_blocks.pop(0)
                        try: self.layout.remove_widget(bottom_block)
                        except Exception: pass
                        for block in self.base_blocks:
                            bx, by = block.pos
                            block.update_pos((bx, by - BLOCK_HEIGHT))
                        mx, my = self.moving_block.pos
                        self.moving_block.update_pos((mx, my - BLOCK_HEIGHT))

                    self.base_blocks.append(self.moving_block)
                    self.score += 1
                    self.score_label.text = f"Skor: {self.score}"
                    if self.score > getattr(self.app, "max_score", 0):
                        self.app.max_score = self.score
                        self.max_score_label.text = f"Max Skor: {self.app.max_score}"
                        # app.save_max_score varsa çağır
                        if hasattr(self.app, "save_max_score"):
                            self.app.save_max_score(self.score)
                    self.spawn_new_block()
                else:
                    self.end_game()
                return False

        # hala düşüş devam ediyor
        self.moving_block.update_pos((x, y))
        return True

    def get_overlap_ratio(self, x1, x2):
        left1 = x1
        right1 = x1 + BLOCK_WIDTH
        left2 = x2
        right2 = x2 + BLOCK_WIDTH
        overlap = max(0, min(right1, right2) - max(left1, left2))
        return overlap / BLOCK_WIDTH

    def spawn_new_block(self):
        if self.score > 30:
            image_source = "assets/tower4.png"
        elif self.score > 20:
            image_source = "assets/tower3.png"
        elif self.score > 10:
            image_source = "assets/tower2.png"
        else:
            image_source = "assets/tower1.png"

        # yeni blok layout içine eklensin
        self.moving_block = Block(pos=(0, Window.height - 50), image_source=image_source)
        self.layout.add_widget(self.moving_block)
        self.moving_right = True
        self.is_falling = False
        # zamanlayıcıyı (move_block) tekrar ayarla
        Clock.unschedule(self.move_block)
        Clock.schedule_interval(self.move_block, 1 / 60)

    def end_game(self):
        # oyun bitti sesi
        g_over = SoundLoader.load("music/game_over.wav")
        if g_over:
            g_over.play()

        self.game_running = False

        # gösterimi layout içine ekle
        lbl = Label(text="Oyun Bitti!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65})
        self.layout.add_widget(lbl)

        # restart button
        btn_restart = Button(text="Yeniden Başla", size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        btn_restart.bind(on_release=self.restart_game)
        self.layout.add_widget(btn_restart)

        # menu button
        btn_menu = Button(text="Ana Menü", size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.25})
        btn_menu.bind(on_release=self.go_to_main_menu)
        self.layout.add_widget(btn_menu)

    def go_to_main_menu(self, *args):
        # leave screen, stop music
        if self.bg_music and self.bg_music.state == "play":
            self.bg_music.stop()
        self.manager.current = 'main'

    def restart_game(self, *args):
        # Clock'ları temizle
        Clock.unschedule(self.move_block)
        Clock.unschedule(self.fall_block)

        # skor sıfırla
        self.score = 0
        self.score_label.text = "Skor: 0"

        # max score update
        self.app = App.get_running_app()
        self.max_score_label.text = f"Max Skor: {getattr(self.app, 'max_score', 0)}"

        # tüm blokları layout'tan kaldır
        for block in list(self.base_blocks):
            try: self.layout.remove_widget(block)
            except Exception: pass
        self.base_blocks = []

        if self.moving_block:
            try: self.layout.remove_widget(self.moving_block)
            except Exception: pass
            self.moving_block = None

        # layout temizle (bütün geçici widget'ları temizle)
        self.layout.clear_widgets()

        # sabit widget'ları tekrar ekle (skorlar + ikon)
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.max_score_label)
        self.layout.add_widget(self.settings_icon)

        # oyun değişkenlerini sıfırla
        self.game_running = False
        self.is_falling = False
        self.platform_x = None

        # yeniden başlat
        self.start_game()
