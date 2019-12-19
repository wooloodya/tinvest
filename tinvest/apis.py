class SandboxApi:
    """"Операция в sandbox"""

    def __init__(self, client):
        self._client = client

    def sandbox_register_post(self, **kwargs):
        """POST /sandbox/register Регистрация клиента в sandbox"""
        return self._client.request("POST", "/sandbox/register", **kwargs)

    def sandbox_currencies_balance_post(self, **kwargs):
        """POST /sandbox/currencies/balance Выставление баланса по валютным позициям"""
        return self._client.request("POST", "/sandbox/currencies/balance", **kwargs)

    def sandbox_positions_balance_post(self, **kwargs):
        """POST /sandbox/positions/balance Выставление баланса по инструментным позициям"""
        return self._client.request("POST", "/sandbox/positions/balance", **kwargs)

    def sandbox_clear_post(self, **kwargs):
        """POST /sandbox/clear Удаление всех позиций"""
        return self._client.request("POST", "/sandbox/clear", **kwargs)


class OrdersApi:
    """"Операции заявок"""

    def __init__(self, client):
        self._client = client

    def orders_get(self, **kwargs):
        """GET /orders Получение списка активных заявок"""
        return self._client.request("GET", "/orders", **kwargs)

    def orders_limit_order_post(self, **kwargs):
        """POST /orders/limit-order Создание лимитной заявки"""
        return self._client.request("POST", "/orders/limit-order", **kwargs)

    def orders_cancel_post(self, **kwargs):
        """POST /orders/cancel Отмена заявки"""
        return self._client.request("POST", "/orders/cancel", **kwargs)


class PortfolioApi:
    """"Операции с портфелем пользователя"""

    def __init__(self, client):
        self._client = client

    def portfolio_get(self, **kwargs):
        """GET /portfolio Получение портфеля клиента"""
        return self._client.request("GET", "/portfolio", **kwargs)

    def portfolio_currencies_get(self, **kwargs):
        """GET /portfolio/currencies Получение валютных активов клиента"""
        return self._client.request("GET", "/portfolio/currencies", **kwargs)


class MarketApi:
    """"Получении информации по бумагам"""

    def __init__(self, client):
        self._client = client

    def market_stocks_get(self, **kwargs):
        """GET /market/stocks Получение списка акций"""
        return self._client.request("GET", "/market/stocks", **kwargs)

    def market_bonds_get(self, **kwargs):
        """GET /market/bonds Получение списка облигаций"""
        return self._client.request("GET", "/market/bonds", **kwargs)

    def market_etfs_get(self, **kwargs):
        """GET /market/etfs Получение списка ETF"""
        return self._client.request("GET", "/market/etfs", **kwargs)

    def market_currencies_get(self, **kwargs):
        """GET /market/currencies Получение списка валютных пар"""
        return self._client.request("GET", "/market/currencies", **kwargs)

    def market_orderbook_get(self, **kwargs):
        """GET /market/orderbook Получение стакана"""
        return self._client.request("GET", "/market/orderbook", **kwargs)

    def market_candles_get(self, **kwargs):
        """GET /market/candles Получение исторических свечей по FIGI"""
        return self._client.request("GET", "/market/candles", **kwargs)

    def market_search_by_figi_get(self, **kwargs):
        """GET /market/search/by-figi Получение инструмента по FIGI"""
        return self._client.request("GET", "/market/search/by-figi", **kwargs)

    def market_search_by_ticker_get(self, **kwargs):
        """GET /market/search/by-ticker Получение инструмента по тикеру"""
        return self._client.request("GET", "/market/search/by-ticker", **kwargs)


class OperationsApi:
    """"Получении информации по операциям"""

    def __init__(self, client):
        self._client = client

    def operations_get(self, **kwargs):
        """GET /operations Получение списка операций"""
        return self._client.request("GET", "/operations", **kwargs)

