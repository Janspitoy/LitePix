from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def logout(self):
        """Метод для выхода из аккаунта."""
        print("Logging out...")
        # Переключаемся на экран входа
        self.manager.current = 'welcome'

    def open_menu(self):
        self.manager.app.open_menu()
