from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.storage.jsonstore import JsonStore
import json

# Importing database and screens
from libs.database.database import init_db
from libs.ui.archive import ArchiveScreen
from libs.ui.converter import ConverterScreen
from libs.ui.file_manager import FileManagerScreen
from libs.ui.register import RegistrationScreen
from libs.ui.login import LoginScreen
from libs.ui.home import HomeScreen
from libs.ui.account import AccountScreen
from libs.ui.settings import SettingsScreen
from libs.ui.welcome import WelcomeScreen
from libs.ui.menu_screen import MenuScreen
from libs.ui.compression import CompressionScreen  # Импортируем CompressionScreen
from kivy import platform

# Request permissions for Android platform
if platform == "android":
    from android.permissions import request_permissions, Permission

    # Request required permissions for storage access
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    # Function to get Android-specific base directory
    def get_android_base_directory():
        from android.storage import app_storage_path
        return app_storage_path()

else:
    # Fallback function for non-Android platforms
    def get_android_base_directory():
        return None


class LitePixApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.store = JsonStore("user_data.json")
        self.current_user_id = None
        self.previous_screen = None

    def build(self):
        # Initialize the database
        init_db()

        # Set up application theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"

        # Load KV files for all screens
        Builder.load_file("kv/welcome_screen.kv")
        Builder.load_file("kv/register_screen.kv")
        Builder.load_file("kv/login_screen.kv")
        Builder.load_file("kv/home_screen.kv")
        Builder.load_file("kv/account_screen.kv")
        Builder.load_file("kv/settings_screen.kv")
        Builder.load_file("kv/menu_screen.kv")
        Builder.load_file("kv/file_manager_screen.kv")
        Builder.load_file("kv/archive_screen.kv")
        Builder.load_file("kv/convert_screen.kv")
        Builder.load_file("kv/compression_screen.kv")

        # Initialize screen manager and add all screens
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(RegistrationScreen(name="registration"))
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(AccountScreen(name="account"))
        self.screen_manager.add_widget(SettingsScreen(name="settings"))
        self.screen_manager.add_widget(MenuScreen(name="menu"))
        self.screen_manager.add_widget(FileManagerScreen(name="file_manager"))
        self.screen_manager.add_widget(ArchiveScreen(name="archive"))
        self.screen_manager.add_widget(ConverterScreen(name="converter"))
        self.screen_manager.add_widget(CompressionScreen(name="compression"))

        # Check login status and set the initial screen
        if self.is_user_logged_in():
            self.current_user_id = self.store.get("user_data")["id"]
            self.screen_manager.current = "home"
        else:
            self.screen_manager.current = "welcome"

        # Bind swipe gesture for navigation
        Window.bind(on_touch_move=self.swipe_back)
        return self.screen_manager

    def is_user_logged_in(self):
        """Check if the user is logged in based on stored data."""
        if self.store.exists("user_data"):
            user_data = self.store.get("user_data")
            return user_data.get("status", False)
        return False

    @staticmethod
    def set_user_logged_in(email, user_id):
        """Save user email and login status to a JSON file."""
        file_path = "user_data.json"

        data = {
            "user_data": {
                "email": email,
                "status": True,
                "id": user_id
            }
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def logout(self):
        """Log the user out by clearing stored data."""
        self.store.delete("user_data")
        self.current_user_id = None
        self.change_screen("welcome")

    def change_screen(self, screen_name):
        """Switch to a different screen with a 0.2-second delay."""

        def perform_change(dt):
            self.screen_manager.transition = NoTransition()
            self.screen_manager.current = screen_name

        Clock.schedule_once(perform_change, 0.1)

    def open_menu(self):
        """Open the menu screen and remember the current screen."""
        self.previous_screen = self.screen_manager.current
        self.change_screen("menu")

    def close_menu(self):
        """Return to the previous screen from the menu."""
        if self.previous_screen:
            self.change_screen(self.previous_screen)
            self.previous_screen = None

    def swipe_back(self, window, touch):
        """Handle swipe gestures to navigate back."""
        if touch.dx > 50 and self.screen_manager.current not in ["home", "menu"]:
            self.change_screen("home")


if __name__ == "__main__":
    LitePixApp().run()
