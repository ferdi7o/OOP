from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.resources import resource_add_path
from kivy.storage.jsonstore import JsonStore

resource_add_path("assets")

# Cube size
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 70
BLOCK_SPEED = 4
FALL_SPEED = 7

class Block(Widget):
    def __init__(self, pos, image_source="assets/tower1.png", **kwargs):
        super().__init__(**kwargs) # sadece kwargs
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

    # def change_image(self, new_source):
    #     self.image.source = new_source
    #     self.image.reload()


class TowerBlockGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moving_block = None
        self.base_blocks = []
        self.moving_right = True
        self.game_running = False
        self.is_falling = False
        self.score = 0
        self.app = App.get_running_app()
        self.max_score = self.app.max_score

        self.app = App.get_running_app()
        self.max_score = self.app.max_score
        self.score_label = Label(
            text="Skor: 0",
            size_hint=(None, None),
            pos=(10, Window.height - 60),
            color=(1, 1, 1, 1),  # Beyaz renk RGBA
            font_size='20sp',
            bold=True)
        self.add_widget(self.score_label)

        self.max_score_label = Label(
            text="Max Skor: 0",
            size_hint=(None, None),
            pos=(Window.width - 150, Window.height - 60),  # Sağ üst köşeye yakın
            color=(1, 1, 0, 1),  # Sarı
            font_size='20sp',
            bold=True
        )
        self.add_widget(self.max_score_label)

        self.platform_x = None  # Kule nereye dizilmeye başladıysa, o x eksenine göre kontrol ederiz

        self.bind(on_touch_down=self.drop_block)
        self.start_game()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(TowerBlockGame(name='game'))
        sm.current = 'game'
        return sm

    def start_game(self):
        self.max_score = self.app.max_score  # Güncel max skoru al
        self.max_score_label.text = f"Max Skor: {self.max_score}"
        # İlk blok düşsün ve kule pozisyonu belirlensin
        Clock.schedule_once(self.drop_first_block, 1)

    def drop_first_block(self, dt):
        self.moving_block = Block(pos=(0, Window.height - 50))
        self.add_widget(self.moving_block)
        self.moving_right = True
        self.game_running = True
        self.is_falling = False
        Clock.schedule_interval(self.move_block, 1 / 60)

    def move_block(self, dt):
        if not self.game_running or self.is_falling:
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
        if not self.game_running or self.is_falling:
            return

        self.is_falling = True
        Clock.unschedule(self.move_block)
        Clock.schedule_interval(self.fall_block, 1 / 60)

    def fall_block(self, dt):
        x, y = self.moving_block.pos
        y -= FALL_SPEED

        if len(self.base_blocks) == 0:
            # İlk blok için
            if y <= 0:
                y = 0
                self.platform_x = self.moving_block.pos[0]  # İlk blok nereye düştüyse kule orada
                self.moving_block.update_pos((self.platform_x, y))
                self.base_blocks.append(self.moving_block)
                self.score = 1
                self.score_label.text = f"Skor: {self.score}"
                self.spawn_new_block()
                return False
        else:
            # Diğer bloklar için
            last_block = self.base_blocks[-1]
            lx, ly = last_block.pos

            if y <= ly + BLOCK_HEIGHT:
                y = ly + BLOCK_HEIGHT

                overlap = self.get_overlap_ratio(self.moving_block.pos[0], last_block.pos[0])

                if overlap >= 0.55:
                    # Yeni bloğun hedef pozisyonunu belirle
                    self.moving_block.update_pos((x, y))

                    # Ekranda maksimum blok sayısı (60% yüksekliğe kadar)
                    max_blocks = int((Window.height * 0.6) // BLOCK_HEIGHT)

                    if len(self.base_blocks) >= max_blocks:
                        # 1. En alt bloğu kaldır
                        bottom_block = self.base_blocks.pop(0)
                        self.remove_widget(bottom_block)

                        # 2. Diğer tüm blokları 1 blok aşağı kaydır
                        for block in self.base_blocks:
                            bx, by = block.pos
                            block.update_pos((bx, by - BLOCK_HEIGHT))

                        # 3. Yeni bloğu da aşağı kaydır
                        mx, my = self.moving_block.pos
                        self.moving_block.update_pos((mx, my - BLOCK_HEIGHT))

                    # 4. Yeni bloğu listeye ekle
                    self.base_blocks.append(self.moving_block)
                    self.score += 1
                    self.score_label.text = f"Skor: {self.score}"
                    if self.score > self.app.max_score:
                        self.app.max_score = self.score
                        self.max_score_label.text = f"Max Skor: {self.app.max_score}"
                        self.app.save_max_score(self.score)
                    self.spawn_new_block()
                else:
                    self.end_game()
                return False

        # Henüz yere çarpmadıysa düşmeye devam et
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

        self.moving_block = Block(pos=(0, Window.height - 50), image_source=image_source)
        self.add_widget(self.moving_block)
        self.moving_right = True
        self.is_falling = False
        Clock.schedule_interval(self.move_block, 1 / 60)

    def end_game(self):
        self.game_running = False
        self.add_widget(Label(text="Oyun Bitti!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}))

        # Yeniden başlat butonu
        btn_restart = Button(text="Yeniden Başla", size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        btn_restart.bind(on_release=self.restart_game)
        self.add_widget(btn_restart)

        # Ana menüye dön butonu
        btn_menu = Button(text="Ana Menü", size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.25})
        btn_menu.bind(on_release=self.go_to_main_menu)
        self.add_widget(btn_menu)

    def go_to_main_menu(self, *args):
        self.manager.current = 'main'

    def restart_game(self, *args):
        # Skoru sıfırla
        self.score = 0
        self.score_label.text = "Skor: 0"

        # Maksimum skoru güncelle (App içindeki kalacak)
        self.max_score = App.get_running_app().max_score
        self.max_score_label.text = f"Max Skor: {self.max_score}"

        # Tüm blokları temizle
        for block in self.base_blocks:
            self.remove_widget(block)
        self.base_blocks = []

        # Düşen blok varsa onu da kaldır
        if self.moving_block:
            self.remove_widget(self.moving_block)
            self.moving_block = None

        # Oyun değişkenlerini sıfırla
        self.game_running = False
        self.is_falling = False
        self.platform_x = None

        # Ekrandaki diğer buton ve "Oyun Bitti" yazısını sil
        self.clear_widgets()

        # Skor etiketlerini tekrar ekle
        self.add_widget(self.score_label)
        self.add_widget(self.max_score_label)

        # Oyunu yeniden başlat
        self.start_game()


class TowerBlockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TowerBlockGame(name='game'))
        sm.current = 'game'
        return sm

if __name__ == '__main__':
    TowerBlockApp().run()
