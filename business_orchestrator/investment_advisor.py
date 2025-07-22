"""
investment_advisor.py

Този модул съдържа класа InvestmentAdvisor, който взема решение въз основа
на анализиран пазарен сигнал.
"""

import logging


class InvestmentAdvisor:
    """
    Клас за вземане на инвестиционно решение въз основа на входен сигнал.
    """

    def __init__(self, buy_threshold=0.7, sell_threshold=0.6):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def evaluate(self, signal):
        """
        Оценява входния сигнал и връща съответно решение.
        :param signal: str – сигнал от анализатора (напр. 'buy:0.85', 'sell:0.4')
        :return: str – решение (напр. 'EXECUTE_BUY', 'EXECUTE_SELL', 'HOLD')
        """
        try:
            logging.info("[Advisor] Получен сигнал: %s", signal)

            parts = signal.split(":")
            signal_type = parts[0].strip().lower()
            confidence = float(parts[1].strip()) if len(parts) > 1 else 0.0

            if signal_type == "buy" and confidence >= self.buy_threshold:
                decision = "EXECUTE_BUY"
            elif signal_type == "sell" and confidence >= self.sell_threshold:
                decision = "EXECUTE_SELL"
            elif signal_type in ["hold", "buy", "sell"]:
                decision = "HOLD"
            else:
                decision = "INVALID_SIGNAL"

        except (ValueError, IndexError) as e:
            logging.error("[Advisor] Грешка при обработка на сигнал: %s", e)
            decision = "INVALID_SIGNAL"

        logging.info("[Advisor] Върнато решение: %s", decision)
        return decision
