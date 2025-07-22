# aicore/data_collector.py

import datetime
import logging
import random
import re
from typing import Optional, List, Tuple

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import requests
except ImportError:
    requests = None

try:
    from newsapi import NewsApiClient
except ImportError:
    NewsApiClient = None


class DataCollector:
    """
    Реален модул за събиране на данни:
    - Цени и информация от yfinance
    - Новини от NewsAPI
    - Уеб търсене чрез DuckDuckGo
    """

    def __init__(
        self,
        use_mock: bool = False,
        enable_yfinance: bool = True,
        enable_newsapi: bool = True,
        newsapi_key: Optional[str] = None,
    ):
        self.use_mock = use_mock
        self.enable_yfinance = enable_yfinance and yf is not None
        self.enable_newsapi = (
            enable_newsapi and NewsApiClient is not None and newsapi_key is not None
        )
        self.newsapi_key = newsapi_key

        self.newsapi_client = (
            NewsApiClient(api_key=newsapi_key) if self.enable_newsapi else None
        )

        self.last_topic: Optional[str] = None
        self.log: List[Tuple[str, str]] = []

        self.logger = logging.getLogger("DataCollector")
        if not self.logger.hasHandlers():
            logging.basicConfig(level=logging.INFO)

    def collect(self, topic: str) -> str:
        self.last_topic = topic
        timestamp = datetime.datetime.now().isoformat()
        self.log.append((timestamp, topic))

        if self.use_mock:
            self.logger.info(f"[MOCK] Данни за: {topic}")
            return self._generate_mock_data(topic)

        if self.enable_yfinance:
            result = self._fetch_yfinance_data(topic)
            if result:
                return result

        if self.enable_newsapi:
            result = self._fetch_newsapi_data(topic)
            if result:
                return result

        result = self._fetch_web_data(topic)
        if result:
            return result

        return f"[!] Неуспешно събиране на реални данни за: {topic}"

    def _generate_mock_data(self, topic: str) -> str:
        samples = [
            f"{topic} е ключов фактор за съвременната икономика.",
            f"{topic} се следи от големите инвеститори.",
            f"Промените в {topic} влияят върху глобалните пазари.",
        ]
        return random.choice(samples)

    def _fetch_yfinance_data(self, topic: str) -> Optional[str]:
        try:
            ticker = yf.Ticker(topic)
            info = ticker.info
            summary = info.get("longBusinessSummary") or info.get("shortName") or ""
            price = info.get("currentPrice")
            currency = info.get("currency", "")
            if not summary:
                return None
            result = f"[YF] {summary.strip()}"
            if price:
                result += f" Текуща цена: {price} {currency}."
            return result
        except Exception as e:
            self.logger.warning(f"YF грешка: {e}")
            return None

    def _fetch_newsapi_data(self, topic: str) -> Optional[str]:
        try:
            articles = self.newsapi_client.get_everything(
                q=topic, language="en", page_size=3
            )
            if articles.get("status") != "ok" or not articles.get("articles"):
                return None
            headlines = [a["title"] for a in articles["articles"] if "title" in a]
            if not headlines:
                return None
            return f"[News] {topic}: " + "; ".join(headlines)
        except Exception as e:
            self.logger.warning(f"NewsAPI грешка: {e}")
            return None

    def _fetch_web_data(self, topic: str) -> Optional[str]:
        if requests is None:
            return None
        try:
            url = f"https://duckduckgo.com/html/?q={topic}"
            headers = {"User-Agent": "Mozilla/5.0 (compatible; DataCollector/1.0)"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                return None
            titles = re.findall(
                r'<a.*?class="result__a".*?>(.*?)</a>', response.text, re.DOTALL
            )
            if titles:
                clean_titles = [re.sub("<.*?>", "", t).strip() for t in titles[:3]]
                return f"[Web] Резултати за '{topic}': " + "; ".join(clean_titles)
        except Exception as e:
            self.logger.warning(f"Web грешка: {e}")
        return None

    def get_last_topic(self) -> Optional[str]:
        return self.last_topic

    def get_log(self) -> List[Tuple[str, str]]:
        return self.log

    def enable_real_mode(self):
        self.use_mock = False

    def enable_mock_mode(self):
        self.use_mock = True
