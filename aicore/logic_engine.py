"""
Модул: LogicEngine
Ниво: 3 (след KnowledgeBase)

Описание:
   Този модул прилага дедукция, индукция и аналогия.
   Генерира логическа верига от обогатените данни.
   Работи с гъвкави шаблони, разширяема база и интелигентна логика.
"""

import re
from typing import Dict, List, Optional


class LogicEngine:
    """
    Логически двигател със следните възможности:
    - Дедукция по правила
    - Индукция чрез разпознати шаблони
    - Аналогия от база със сходства
    """

    __slots__ = ["induction_patterns"]

    TEMPLATES: Dict[str, str] = {
        "deduction": (
            "Прилагайки правило '{rule}' към '{topic}', "
            "стигаме до извод: {conclusion}."
        ),
        "induction": (
            "На база наблюдавани модели в '{topic}' ({patterns}), "
            "индуктивно заключаваме: {conclusion}."
        ),
        "analogy": ("Чрез аналогия, '{topic}' прилича на '{analogy}' поради {reason}."),
    }

    ANALOGY_DB: Dict[str, Dict[str, str]] = {
        "биткойн": {
            "analogy": "дигитално злато",
            "reason": "ограничено предлагане и стойност от доверие",
        },
        "инфлация": {
            "analogy": "невидим данък",
            "reason": "ерозира покупателната способност",
        },
        "ai": {
            "analogy": "индустриална революция",
            "reason": "радикална трансформация на производствените процеси",
        },
        "блокчейн": {
            "analogy": "дигитален нотариус",
            "reason": "непроменлив регистър на транзакции",
        },
        "крипто": {
            "analogy": "дигитална валута",
            "reason": "децентрализирана природа и криптографска сигурност",
        },
    }

    def __init__(self):
        """
        Инициализира шаблоните за индукция.
        """
        self.induction_patterns: Dict[str, str] = {
            r"повтаряемост": "циклични модели",
            r"икономическ": "икономически зависимости",
            r"тренд": "статистически тенденции",
            r"закон|правило": "приложими регулаторни рамки",
        }

    def process(self, enriched_data: Dict) -> List[str]:
        """
        Обработва логическа верига от данни и връща списък с изводи.

        :param enriched_data: Обогатени данни с теми, правила и контекст
        :return: Списък с логически изводи (str)
        """
        topic = enriched_data.get("topic", "неизвестна тема")
        context = enriched_data.get("summary", "")
        rules = enriched_data.get("rules_applied", [])

        chain = [
            self._deduce(topic, rules),
            self._induce(topic, context),
            self._analogize(topic),
        ]

        return [c for c in chain if c]

    def _deduce(self, topic: str, rules: List[str]) -> str:
        """
        Прилага дедукция върху подадени правила.

        :param topic: Темата, върху която се прилага дедукция
        :param rules: Списък с логически правила
        :return: Логически извод на база първото правило или празен низ
        """
        if not rules:
            return ""

        selected_rule = rules[0]
        conclusion = f"{topic} следва строги причинно-следствени връзки"

        return self.TEMPLATES["deduction"].format(
            rule=selected_rule, topic=topic, conclusion=conclusion
        )

    def _induce(self, topic: str, context: str) -> str:
        """
        Прилага индукция на база контекст.

        :param topic: Темата, която се анализира
        :param context: Контекстуален текст
        :return: Извод на база открити шаблони
        """
        if not context:
            return ""

        found_patterns = [
            desc
            for pattern, desc in self.induction_patterns.items()
            if re.search(pattern, context, re.IGNORECASE)
        ]

        if found_patterns:
            patterns_desc = ", ".join(found_patterns[:2])
            conclusion = f"{topic} демонстрира ясно разпознаваеми модели"
        else:
            patterns_desc = "неясни параметри"
            conclusion = f"{topic} показва нестандартна структура"

        return self.TEMPLATES["induction"].format(
            topic=topic, patterns=patterns_desc, conclusion=conclusion
        )

    def _analogize(self, topic: str) -> str:
        """
        Прилага аналогия за дадена тема, ако има съвпадение в базата.

        :param topic: Темата, за която се търси аналогия
        :return: Текст с аналогия или алтернативно съобщение
        """
        data = self.ANALOGY_DB.get(topic.lower())
        if data:
            return self.TEMPLATES["analogy"].format(
                topic=topic, analogy=data["analogy"], reason=data["reason"]
            )
        return (
            f"За '{topic}' няма директна аналогия, "
            f"но се наблюдават паралели с други концепции."
        )

    def add_analogy(self, topic: str, analogy: str, reason: str) -> None:
        """
        Добавя нова аналогия към базата, ако не съществува вече.

        :param topic: Темата, за която се добавя аналогия
        :param analogy: Аналогията, с която се сравнява темата
        :param reason: Причината за съпоставката
        """
        key = topic.lower()
        if key not in self.ANALOGY_DB:
            self.ANALOGY_DB[key] = {"analogy": analogy, "reason": reason}

    def get_analogy(self, topic: str) -> Optional[Dict[str, str]]:
        """
        Връща аналогията за дадена тема, ако съществува.

        :param topic: Темата, която се проверява
        :return: Речник с analogy и reason или None
        """
        return self.ANALOGY_DB.get(topic.lower())
