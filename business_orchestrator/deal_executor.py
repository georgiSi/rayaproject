"""
deal_executor.py

Този модул съдържа класа DealExecutor, който изпълнява инвестиционни решения
като покупка, продажба или задържане на актив, базирани на предварително
взето решение от InvestmentAdvisor.
"""

import logging


class DealExecutor:
    """
    Клас за изпълнение на инвестиционни решения.
    """

    def __init__(self):
        """
        Инициализира изпълнителя и подготвя списъка с извършени сделки.
        """
        self.executed_trades = []

    def execute(self, decision: str):
        """
        Изпълнява дадено инвестиционно решение.

        :param decision: str – решение (напр. 'EXECUTE_BUY', 'EXECUTE_SELL', 'HOLD')
        """
        logging.info("[Executor] Получено решение за изпълнение: %s", decision)

        if decision == "EXECUTE_BUY":
            self.buy()
        elif decision == "EXECUTE_SELL":
            self.sell()
        elif decision == "HOLD":
            self.hold()
        else:
            logging.warning("[Executor] Непознато решение: %s", decision)

    def buy(self):
        """
        Изпълнява покупка на актив.
        """
        logging.info("[Executor] Извършена покупка на актив.")
        self.executed_trades.append("BUY")

    def sell(self):
        """
        Изпълнява продажба на актив.
        """
        logging.info("[Executor] Извършена продажба на актив.")
        self.executed_trades.append("SELL")

    def hold(self):
        """
        Задържа текущата позиция (не прави действие).
        """
        logging.info("[Executor] Задържане – без действие.")
        self.executed_trades.append("HOLD")
