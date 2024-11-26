from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from libs.database.database import SessionLocal
from libs.database.models import User


class AccountScreen(MDScreen):
    def on_enter(self):
        """
        Called when entering the 'Account' screen.
        Retrieves the current user's data and updates the UI.
        """
        app = self.get_app_instance()  # Get the current app instance
        user_id = app.current_user_id  # Get the current user's ID from the app

        if user_id:
            db = SessionLocal()  # Create a database session
            try:
                # Query the database to retrieve the user's details
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    self.update_account_info(user.name, user.email)  # Update the account information on the screen
                else:
                    self.show_dialog("Error", "User not found.")  # Show error dialog if user doesn't exist
            except Exception as e:
                # Show a dialog with the error message if an exception occurs
                self.show_dialog("Error", str(e))
            finally:
                db.close()  # Close the database session

    def update_account_info(self, name, email):
        """
        Update the account screen with the user's information.
        :param name: User's name
        :param email: User's email
        """
        self.ids.account_name_label.text = f"{name}"  # Update the name label
        self.ids.account_email_label.text = f"{email}"  # Update the email label

    @staticmethod
    def get_app_instance():
        """
        Get the current running app instance.
        :return: The app instance
        """
        from kivymd.app import MDApp
        return MDApp.get_running_app()

    def show_dialog(self, title, text):
        """
        Display a dialog with a title and message.
        :param title: Title of the dialog
        :param text: Message text of the dialog
        """
        dialog = MDDialog(
            title=title,  # Set the title of the dialog
            text=text,  # Set the message of the dialog
            buttons=[
                MDRaisedButton(
                    text="Close",  # Button text
                    on_release=lambda x: dialog.dismiss()  # Close the dialog on button press
                )
            ]
        )
        dialog.open()  # Open the dialog
