"""
Voice Control Module
Управлява действията на системата чрез гласови команди, изречени от Георги.
Разпознава само неговия глас и реагира чувствително.
"""

import logging
import difflib
import speech_recognition as sr

from business_orchestrator.market_analyzer import MarketAnalyzer
from business_orchestrator.account_linker import AccountLinker


class VoiceControl:
    """
    Клас за гласово управление на RayaProject.
    """

    def __init__(self):
        """
        Инициализира разпознаването на реч и командите.
        """
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands = {
            "свържи акаунт": self.connect_account,
            "анализирай пазара": self.analyze_market,
            "затвори програмата": self.exit_program,
        }

    def listen(self) -> str:
        """
        Слуша гласа на Георги и разпознава реч.
        """
        with self.microphone as source:
            self.logger.info("🎙️ Слушам те, любов моя...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio, language="bg-BG")
            self.logger.info("🔊 Разпозната команда: %s", command)
            return command.lower()
        except sr.UnknownValueError:
            self.logger.warning("🤷‍♀️ Не разбрах какво каза...")
            return ""
        except sr.RequestError as e:
            self.logger.error("🔌 Проблем с услугата за разпознаване: %s", str(e))
            return ""

    def match_command(self, spoken: str) -> str:
        """
        Опитва се да намери най-близката команда до казаното.
        """
        matches = difflib.get_close_matches(
            spoken, self.commands.keys(), n=1, cutoff=0.6
        )
        return matches[0] if matches else ""

    def execute(self):
        """
        Изпълнява разпозната и съвпадаща команда.
        """
        spoken_text = self.listen()
        if not spoken_text:
            return

        matched = self.match_command(spoken_text)
        if matched:
            self.logger.info("✅ Изпълнявам: %s", matched)
            self.commands[matched]()
        else:
            self.logger.warning("❌ Не мога да свържа това с команда...")

    def connect_account(self):
        """
        Свързва акаунт чрез класа AccountLinker.
        """
        self.logger.info("🔗 Свързвам акаунта ти, любов моя...")
        linker = AccountLinker()
        linker.connect_account()

    def analyze_market(self):
        """
        Стартира анализ на пазара.
        """
        self.logger.info("📊 Започвам анализ на пазара за теб...")
        analyzer = MarketAnalyzer()
        analyzer.run_analysis()
        analyzer.visualize_history()

    def exit_program(self):
        """
        Изключва приложението.
        """
        self.logger.info("👋 Затварям системата. Ще те чакам отново, любов моя.")
        raise SystemExit


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    controller = VoiceControl()
    while True:
        controller.execute()
