"""
Модул: KnowledgeBase
Ниво: 2 (над DataCollector)

Описание:
   Обогатява суровите данни, подадени по дадена тема.
   Използва базови логически правила, вграден контекст и вътрешна памет.
   Подготвен за бъдещо разширение с външна база знания, reasoning agents и граф логика.
"""

import datetime


class KnowledgeBase:
    """
    Клас за обогатяване на сурови данни.
    Поддържа вътрешна памет, правила и логическо обобщение.
    """

    def __init__(self):
        self.memory = {}  # Запомнени теми и тяхното обогатяване
        self.rules = [
            "Всяка тема е свързана с икономически и социални фактори.",
            "Историята често разкрива модели на поведение.",
            "Темите не са изолирани – всичко е взаимосвързано.",
            "Контекстът придава смисъл на информацията.",
            "Източникът е толкова важен, колкото и самото съдържание.",
        ]

    def enrich(self, raw_data: str) -> dict:
        """
        Обогатява данните чрез прилагане на правила и контекст.

        :param raw_data: Сурови данни от DataCollector
        :return: Обогатен речник с логически контекст
        """
        topic = self._extract_topic(raw_data)
        timestamp = datetime.datetime.now().isoformat()

        context = {
            "topic": topic,
            "original": raw_data,
            "rules_applied": self.rules[:3],
            "timestamp": timestamp,
            "summary": self._generate_summary(raw_data, topic),
        }

        self.memory[topic] = context
        return context

    def _extract_topic(self, raw_data: str) -> str:
        """
        Извлича тема от текста (ако има кавички).
        :param raw_data: суров текст
        :return: тема
        """
        if "'" in raw_data:
            return raw_data.split("'")[1]
        elif '"' in raw_data:
            return raw_data.split('"')[1]
        return "неизвестна тема"

    def _generate_summary(self, raw_data: str, topic: str) -> str:
        """
        Обобщава съдържанието по темата.
        :param raw_data: оригинален текст
        :param topic: извлечена тема
        :return: обобщен текст
        """
        trimmed = raw_data.strip().replace("\n", " ")
        short = trimmed if len(trimmed) < 80 else trimmed[:80] + "..."
        return (
            f"Тема: '{topic}'\n"
            f'Данни: "{short}"\n'
            f"Добавено чрез правила и времеви отпечатък."
        )

    def get_memory(self) -> dict:
        """
        Връща паметта (всички обработени теми).
        """
        return self.memory

    def get_topic_context(self, topic: str) -> dict:
        """
        Връща обогатения контекст за дадена тема, ако е наличен.
        """
        return self.memory.get(topic, {})

    def list_rules(self) -> list:
        """
        Връща списък с логическите правила, които се прилагат.
        """
        return self.rules

    def add_rule(self, new_rule: str):
        """
        Добавя ново правило към базата.
        :param new_rule: текст на правилото
        """
        if new_rule not in self.rules:
            self.rules.append(new_rule)
