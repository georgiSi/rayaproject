"""
binance_tradet.py - Управление на реални и симулирани поръчки към Binance API.
"""

import time
import hmac
import hashlib
import os
from urllib.parse import urlencode
import logging
import requests
from dotenv import load_dotenv

load_dotenv()


class BinanceTrader:
    """Клас за изпращане на поръчки към Binance и симулация на търговия."""

    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET").encode()
        self.base_url = "https://api.binance.com"

    def _get_timestamp(self):
        """Връща текущия Unix timestamp в милисекунди."""
        return int(time.time() * 1000)

    def _sign(self, params):
        """Подписва параметрите с HMAC-SHA256."""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret, query_string.encode(), hashlib.sha256
        ).hexdigest()

    def _headers(self):
        """Връща хедърите за заявката."""
        return {"X-MBX-APIKEY": self.api_key}

    def _send_order(self, side, quantity=0.001):
        """Изпраща пазарна поръчка към Binance (BUY или SELL)."""
        endpoint = "/api/v3/order"
        url = self.base_url + endpoint
        params = {
            "symbol": self.symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": self._get_timestamp(),
        }
        params["signature"] = self._sign(params)

        try:
            response = requests.post(
                url, headers=self._headers(), params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("[REAL] ✅ Order executed: %s %s BTC", side, quantity)
            return response.json()
        except requests.RequestException as e:
            logging.error("❌ Order failed: %s", str(e))
            return {"status": "error", "error": str(e)}

    def buy(self, quantity=0.001):
        """Стартира поръчка за покупка."""
        return self._send_order("BUY", quantity)

    def sell(self, quantity=0.001):
        """Стартира поръчка за продажба."""
        return self._send_order("SELL", quantity)
