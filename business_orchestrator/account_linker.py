"""
Account Linker Module
Отговаря за свързването и управлението на акаунти към различни платформи.
"""

import logging


class AccountLinker:
    """
    Клас за управление на акаунти към платформи (напр. Binance).
    """

    def __init__(self):
        """
        Инициализация на наличните акаунти.
        """
        self.logger = logging.getLogger(__name__)
        self.accounts = {
            "binance": {
                "api_key": "your-binance-api-key",
                "api_secret": "your-binance-secret",
                "base_url": "https://api.binance.com",
            },
            # Добави нови акаунти тук
            "revolut": {
                "api_key": "your-revolut-api-key",
                "base_url": "https://api.revolut.com",
            },
        }

    def list_accounts(self) -> list:
        """
        Връща списък с всички налични акаунти.
        """
        return list(self.accounts.keys())

    def get_account(self, name: str) -> dict:
        """
        Взима информация за конкретен акаунт по име.
        """
        account = self.accounts.get(name.lower())
        if not account:
            self.logger.warning("❌ Акаунтът '%s' не е намерен.", name)
            raise ValueError(f"Акаунт '{name}' не съществува.")
        return account

    def connect_account(self, name: str = "binance") -> None:
        """
        Свързва акаунт по подразбиране или по зададено име.
        """
        try:
            account = self.get_account(name)
            self.logger.info("🔐 Свързан с акаунт: %s", account["base_url"])
            print(f"🔐 Свързан с акаунт: {account['base_url']}")
        except ValueError as e:
            self.logger.error("❗️Грешка при свързване: %s", str(e))
            print(f"❌ Грешка при свързване: {str(e)}")

    def is_connected(self, name: str = "binance") -> bool:
        """
        Проверява дали акаунтът е наличен и готов.
        """
        try:
            self.get_account(name)
            return True
        except ValueError:
            return False
