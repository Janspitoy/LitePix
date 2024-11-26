from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from libs.database.database import SessionLocal
from libs.database.models import User
import bcrypt


class LoginScreen(MDScreen):
    dialog = None  # Переменная для хранения диалога

    def login(self):
        """Проверяет введенные данные и выполняет вход пользователя."""
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        # Проверяем, заполнены ли поля
        if not email or not password:
            self.show_dialog("Error", "Please, fill all the fields before.")
            return

        try:
            # Открываем сессию для работы с базой данных
            db = SessionLocal()
            user = db.query(User).filter(User.email == email).first()

            # Проверяем, существует ли пользователь и совпадает ли пароль
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                app = self.get_app_instance()
                app.set_user_logged_in(email=user.email, user_id=user.id)
                app.current_user_id = user.id  # Сохраняем user_id в экземпляре приложения
                app.change_screen("home")  # Переход на главный экран
            else:
                self.show_dialog("Error", "Incorrect email or password.")
        except Exception as e:
            print(f"Error during login: {e}")
            self.show_dialog("Error", "An unexpected error occurred. Please try again.")
        finally:
            db.close()

    def show_dialog(self, title, text):
        """Отображает диалоговое окно с заданным текстом."""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[MDFlatButton(
                    text="Close", on_release=self.close_dialog
                )]
            )
        else:
            self.dialog.title = title
            self.dialog.text = text
        self.dialog.open()

    def close_dialog(self, *args):
        """Закрывает диалоговое окно."""
        if self.dialog:
            self.dialog.dismiss()

    @staticmethod
    def get_app_instance():
        """Возвращает текущий экземпляр приложения."""
        from kivymd.app import MDApp
        return MDApp.get_running_app()
