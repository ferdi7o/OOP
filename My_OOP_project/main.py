from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.main_menu import MainMenuScreen
from screens.game_screen import TowerBlockGame
from screens.about_screen import AboutScreen
from kivy.storage.jsonstore import JsonStore
import os

class CubeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Android uyumlu path
        if platform == "android":
            from android.storage import app_storage_path
            self.data_dir = app_storage_path()
        else:
            self.data_dir = os.getcwd()
        self.store = JsonStore(os.path.join(self.data_dir, "score.json"))
        self.max_score = self.load_max_score()

    def load_max_score(self):
        if self.store.exists("max"):
            return self.store.get("max")["score"]
        return 0

    def save_max_score(self, score):
        self.store.put("max", score=score)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(TowerBlockGame(name='game'))
        sm.add_widget(AboutScreen(name='about'))
        return sm

if __name__ == '__main__':
    CubeApp().run()