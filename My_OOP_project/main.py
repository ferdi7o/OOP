from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.main_menu import MainMenuScreen
from screens.game_screen import TowerBlockGame
from screens.about_screen import AboutScreen

class CubeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(TowerBlockGame(name='game'))
        sm.add_widget(AboutScreen(name='about'))
        return sm

if __name__ == '__main__':
    CubeApp().run()