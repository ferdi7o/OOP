from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window

# Cube size
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 30
BLOCK_SPEED = 4
FALL_SPEED = 7

class Block(Widget):
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        self.size = (BLOCK_WIDTH, BLOCK_HEIGHT)
        self.pos = pos
        with self.canvas:
            Color(0.2, 0.6, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_pos(self, pos):
        self.pos = pos
        self.rect.pos = pos

class TowerBlockGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moving_block = None
        self.base_blocks = []
        self.moving_right = True
        self.game_running = False
        self.is_falling = False
        self.score = 0
        self.score_label = Label(text="Skor: 0", size_hint=(None, None), pos=(10, Window.height - 40))
        self.add_widget(self.score_label)
        self.platform_x = None  # Kule nereye dizilmeye başladıysa, o x eksenine göre kontrol ederiz

        self.bind(on_touch_down=self.drop_block)
        self.start_game()

    def start_game(self):
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
            # first blok organizer
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
            # next blok down on the first blok
            last_block = self.base_blocks[-1]
            lx, ly = last_block.pos
            if y <= ly + BLOCK_HEIGHT:
                y = ly + BLOCK_HEIGHT

                # Hiza kontrolü
                overlap = self.get_overlap_ratio(self.moving_block.pos[0], last_block.pos[0])

                if overlap >= 0.51:
                    # Succesfuly
                    aligned_x = last_block.pos[0]  # Blok line maker
                    self.moving_block.update_pos((aligned_x, y))
                    self.base_blocks.append(self.moving_block)
                    self.score += 1
                    self.score_label.text = f"Skor: {self.score}"
                    self.spawn_new_block()
                else:
                    self.end_game()
                return False

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
        self.moving_block = Block(pos=(0, Window.height - 50))
        self.add_widget(self.moving_block)
        self.moving_right = True
        self.is_falling = False
        Clock.schedule_interval(self.move_block, 1 / 60)

    def end_game(self):
        self.game_running = False
        self.add_widget(Label(text="Oyun Bitti!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.6}))
        btn_restart = Button(text="Yeniden Başla", size_hint=(0.4, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        btn_restart.bind(on_release=self.restart_game)
        self.add_widget(btn_restart)

    def restart_game(self, *args):
        self.clear_widgets()
        self.__init__()

class TowerBlockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TowerBlockGame(name='game'))
        sm.current = 'game'
        return sm

if __name__ == '__main__':
    TowerBlockApp().run()
