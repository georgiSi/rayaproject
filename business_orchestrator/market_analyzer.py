"""
Market Analyzer Module
Отговаря за вземане на пазарни сигнали на базата на исторически цени.
"""

import datetime
import logging

import matplotlib.pyplot as plt
import ccxt


class MarketAnalyzer:
    """
    Клас за анализ на пазарни данни и визуализация на сигнали.
    """

    def __init__(self, symbol="BTC/USDT"):
        self.symbol = symbol
        self.exchange = ccxt.binance()
        self.logger = logging.getLogger(__name__)
        self.history = []

    def fetch_binance_data(self):
        """
        Взима последните затварящи цени от Binance за даден символ.
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe="1m", limit=10)
            prices = [candle[4] for candle in ohlcv]
            return prices
        except ccxt.BaseError as e:
            self.logger.error("❌ Binance fetch error for %s: %s", self.symbol, str(e))
            return []

    def analyze_trend(self, prices):
        """
        Проста логика за buy/sell/wait сигнал.
        """
        if len(prices) < 3:
            return "wait"
        if prices[-1] > prices[-2] > prices[-3]:
            return "buy"
        if prices[-1] < prices[-2] < prices[-3]:
            return "sell"
        return "wait"

    def store_history(self, signal):
        """
        Запазва историята на сигналите и балансите по време.
        """
        now = datetime.datetime.now()
        balance = self.get_dummy_balance()
        self.history.append(
            {
                "timestamp": now.strftime("%H:%M:%S"),
                "signal": signal,
                "balance": balance,
            }
        )

    def get_dummy_balance(self):
        """
        Генерира примерен баланс за визуализация.
        """
        return 1000 + len(self.history) * 25

    def visualize_history(self):
        """
        Визуализира графично историята на баланса и сигналите.
        """
        if not self.history:
            self.logger.warning("⚠️ No history to visualize.")
            return

        timestamps = [entry["timestamp"] for entry in self.history]
        balances = [entry["balance"] for entry in self.history]
        signals = [entry["signal"] for entry in self.history]
        colors = {"buy": "green", "sell": "red", "wait": "orange"}

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, balances, label="💰 Balance", color="green")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.title("📈 Balance Over Time")
        plt.legend()
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 2))
        plt.bar(
            timestamps,
            [1] * len(signals),
            color=[colors.get(s, "gray") for s in signals],
        )
        plt.title("📊 Market Signals")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def run_analysis(self):
        """
        Основна функция за анализ и логване.
        """
        prices = self.fetch_binance_data()
        if not prices:
            self.logger.warning("❌ No prices fetched for %s, skipping.", self.symbol)
            return "wait"

        signal = self.analyze_trend(prices)
        self.logger.info("📡 Market signal for %s: %s", self.symbol, signal)
        self.store_history(signal)
        return signal


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyzer = MarketAnalyzer()

    for _ in range(5):
        analyzer.run_analysis()

    analyzer.visualize_history()
