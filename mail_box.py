import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    """Класс для работы с электронной почтой (отправка и получение)."""

    def __init__(self, login: str, password: str, smtp_server: str, imap_server: str):
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.imap_server = imap_server

    def send_email(self, subject: str, recipients: list, message: str) -> None:
        """
        Отправляет электронное письмо.

        :param subject: Тема письма.
        :param recipients: Список получателей.
        :param message: Текст сообщения.
        """
        try:
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = self.login
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(message))

            # Подключение к SMTP серверу и отправка письма
            with smtplib.SMTP(self.smtp_server, 587) as smtp:
                smtp.ehlo()  # Идентификация клиента
                smtp.starttls()  # Шифрование соединения
                smtp.ehlo()  # Повторная идентификация после шифрования
                smtp.login(self.login, self.password)
                smtp.sendmail(self.login, recipients, msg.as_string())
            print("Письмо успешно отправлено.")
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")

    def receive_email(self, header: str = None) -> str:
        """
        Получает последнее письмо из почтового ящика.

        :param header: Заголовок для фильтрации писем. Если None, возвращается последнее письмо.
        :return: Текст последнего письма.
        """
        try:
            # Подключение к IMAP серверу
            with imaplib.IMAP4_SSL(self.imap_server, 993) as imap:
                imap.login(self.login, self.password)
                imap.select("inbox")

                # Формирование критерия поиска
                criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
                result, data = imap.uid('search', None, criterion)

                if not data[0]:
                    raise ValueError("Нет писем с указанным заголовком.")

                # Получение UID последнего письма
                latest_email_uid = data[0].split()[-1]
                result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = data[0][1]

                # Декодирование письма
                email_message = email.message_from_bytes(raw_email)
                if email_message.is_multipart():
                    # Если письмо содержит несколько частей, берем первую текстовую часть
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            return part.get_payload(decode=True).decode()
                else:
                    # Если письмо не multipart, возвращаем его содержимое
                    return email_message.get_payload(decode=True).decode()

        except Exception as e:
            print(f"Ошибка при получении письма: {e}")
            return ""


# Конфигурация
GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"

LOGIN = 'login@gmail.com'  # Заменить на реальный логин
PASSWORD = 'qwerty'        # Заменить на реальный пароль
SUBJECT = 'Subject'
RECIPIENTS = ['vasya@email.com', 'petya@email.com']
MESSAGE = 'Message'
HEADER = None


# Пример использования
if __name__ == "__main__":
    client = EmailClient(LOGIN, PASSWORD, GMAIL_SMTP, GMAIL_IMAP)

    # Отправка письма
    client.send_email(SUBJECT, RECIPIENTS, MESSAGE)

    # Получение письма
    last_email = client.receive_email(HEADER)
    print("Последнее письмо:", last_email)