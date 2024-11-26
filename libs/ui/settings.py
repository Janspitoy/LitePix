import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivymd.uix.snackbar import Snackbar


def show_dialog(title, text):
    """Showing the dialog with the massage"""
    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDRaisedButton(
                text="Close",
                on_release=lambda x: dialog.dismiss()
            )
        ]
    )
    dialog.open()


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def change_password():
        """Method of changing password"""
        show_dialog("Change Password", "Here will be the Method of changing the password.")

    @staticmethod
    def logout():
        """Metod of Log Out and change the user status"""
        try:
            # Load the existing data from user_data.json
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update the status to False
            if "user_data" in data:
                data["user_data"]["status"] = False

                # Save the updated data back to the file
                with open("user_data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            else:
                print("Invalid data format in user_data.json")

        except FileNotFoundError:
            print("Error: user_data.json file not found.")
            Snackbar(text="File user_data.json not found").open()
        except json.JSONDecodeError:
            print("Error: Failed to parse user_data.json.")
            Snackbar(text="Error reading file user_data.json").open()

        # Change to the login screen
        app = App.get_running_app()
        app.change_screen("welcome")

    def open_menu(self):
        self.manager.app.open_menu()