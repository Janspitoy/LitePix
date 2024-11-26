from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from libs.database.database import SessionLocal
from libs.database.models import User
import re
import bcrypt


class RegistrationScreen(MDScreen):
    dialog = None  # Переменная для хранения диалога

    def register(self):
        """Регистрация нового пользователя."""
        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        # Проверка на заполнение полей
        if not name or not email or not password:
            self.show_dialog("Error", "Please fill all the fields.")
            return

        # Проверка формата email
        if not self.is_valid_email(email):
            self.show_dialog("Error", "Invalid email format.")
            return

        # Проверка длины пароля
        if len(password) < 8:
            self.show_dialog("Error", "Password must be at least 8 characters long.")
            return

        try:
            # Открываем сессию для работы с базой данных
            db = SessionLocal()

            # Проверяем, существует ли пользователь с таким email
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                self.show_dialog("Error", "User already exists with this email.")
            else:
                # Хешируем пароль и создаем нового пользователя
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(name=name, email=email, password=hashed_password.decode('utf-8'))
                db.add(new_user)
                db.commit()

                # Сохраняем ID нового пользователя в приложении
                app = self.get_app_instance()
                app.set_user_logged_in(email=new_user.email, user_id=new_user.id)  # Сохраняем статус авторизации
                app.change_screen("home")  # Переход на главный экран

        except Exception as e:
            print(f"Error during registration: {e}")
            self.show_dialog("Error", "An unexpected error occurred. Please try again.")
        finally:
            db.close()

    @staticmethod
    def is_valid_email(email):
        """Проверяет корректность email."""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def show_dialog(self, title, text):
        """Отображает диалоговое окно с заданным текстом."""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=self.close_dialog
                    )
                ],
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
