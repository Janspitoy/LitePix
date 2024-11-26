from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class MenuScreen(MDScreen):
    def navigate_to(self, screen_name):
        """Навигация на выбранный экран"""
        self.manager.current = screen_name

    def close_menu(self):
        """Возвращение на предыдущий экран"""
        app = MDApp.get_running_app()  # Получаем экземпляр приложения
        app.close_menu()
