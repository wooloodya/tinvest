from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel  # pylint: disable=E0611


class CandleResolution(str, Enum):
    min1 = '1min'
    min2 = '2min'
    min3 = '3min'
    min5 = '5min'
    min10 = '10min'
    min15 = '15min'
    min30 = '30min'
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'


class Currency(str, Enum):
    rub = 'RUB'
    usd = 'USD'
    eur = 'EUR'


class InstrumentType(str, Enum):
    stock = 'Stock'
    currency = 'Currency'
    bond = 'Bond'
    etf = 'Etf'


class OperationStatus(str, Enum):
    done = 'Done'
    decline = 'Decline'
    progress = 'Progress'


class OperationType(str, Enum):
    buy = 'Buy'
    sell = 'Sell'


class OperationTypeWithCommission(str, Enum):
    buy = 'Buy'
    sell = 'Sell'
    broker_commission = 'BrokerCommission'
    exchange_commission = 'ExchangeCommission'
    service_commission = 'ServiceCommission'
    margin_commission = 'MarginCommission'
    other_commission = 'OtherCommission'
    pay_in = 'PayIn'
    pay_out = 'PayOut'
    tax = 'Tax'
    tax_lucre = 'TaxLucre'
    tax_dividend = 'TaxDividend'
    tax_coupon = 'TaxCoupon'
    tax_back = 'TaxBack'
    repayment = 'Repayment'
    part_repayment = 'PartRepayment'
    coupon = 'Coupon'
    dividend = 'Dividend'
    security_in = 'SecurityIn'
    security_out = 'SecurityOut'


class OrderStatus(str, Enum):
    new = 'New'
    partially_fill = 'PartiallyFill'
    fill = 'Fill'
    cancelled = 'Cancelled'
    replaced = 'Replaced'
    pending_cancel = 'PendingCancel'
    rejected = 'Rejected'
    pending_replace = 'PendingReplace'
    pending_new = 'PendingNew'


class OrderType(str, Enum):
    limit = 'Limit'
    market = 'Market'


class SandboxCurrency(str, Enum):
    rub = 'RUB'
    usd = 'USD'
    eur = 'EUR'


class TradeStatus(str, Enum):
    normal_trading = 'NormalTrading'
    not_available_for_trading = 'NotAvailableForTrading'


class MoneyAmount(BaseModel):
    currency: Currency
    value: float


class MarketInstrument(BaseModel):
    currency: Optional[Currency]
    figi: str
    isin: Optional[str]
    lot: int
    min_price_increment: Optional[float]
    name: str
    ticker: str

    class Config:
        fields = {'min_price_increment': {'alias': 'minPriceIncrement'}}


class OrderResponse(BaseModel):
    price: float
    quantity: int


class Candle(BaseModel):
    c: float
    figi: str
    h: float
    interval: CandleResolution
    l: float
    o: float
    time: str
    v: int


class CurrencyPosition(BaseModel):
    balance: float
    blocked: Optional[float]
    currency: Currency


class Candles(BaseModel):
    candles: List[Candle]
    figi: str
    interval: CandleResolution


class Currencies(BaseModel):
    currencies: List[CurrencyPosition]


class MarketInstrumentList(BaseModel):
    instruments: List[MarketInstrument]
    total: float


class OperationTrade(BaseModel):
    date: str
    price: float
    quantity: int
    trade_id: str

    class Config:
        fields = {'trade_id': {'alias': 'tradeId'}}


class Operation(BaseModel):
    commission: Optional[MoneyAmount]
    currency: Currency
    date: str
    figi: Optional[str]
    id: str
    instrument_type: Optional[InstrumentType]
    is_margin_call: bool
    operation_type: Optional[OperationTypeWithCommission]
    payment: float
    price: Optional[float]
    quantity: Optional[int]
    status: OperationStatus
    trades: Optional[List[OperationTrade]]

    class Config:
        fields = {
            'instrument_type': {'alias': 'instrumentType'},
            'is_margin_call': {'alias': 'isMarginCall'},
            'operation_type': {'alias': 'operationType'},
        }


class Operations(BaseModel):
    operations: List[Operation]


class Order(BaseModel):
    executed_lots: int
    figi: str
    operation: OperationType
    order_id: str
    price: float
    requested_lots: int
    status: OrderStatus
    type_: OrderType

    class Config:
        fields = {
            'executed_lots': {'alias': 'executedLots'},
            'order_id': {'alias': 'orderId'},
            'requested_lots': {'alias': 'requestedLots'},
            'type_': {'alias': 'type'},
        }


class Orderbook(BaseModel):
    asks: List[OrderResponse]
    bids: List[OrderResponse]
    close_price: Optional[float]
    depth: int
    figi: str
    last_price: Optional[float]
    limit_down: Optional[float]
    limit_up: Optional[float]
    min_price_increment: float
    trade_status: TradeStatus

    class Config:
        fields = {
            'close_price': {'alias': 'closePrice'},
            'last_price': {'alias': 'lastPrice'},
            'limit_down': {'alias': 'limitDown'},
            'limit_up': {'alias': 'limitUp'},
            'min_price_increment': {'alias': 'minPriceIncrement'},
            'trade_status': {'alias': 'tradeStatus'},
        }


class PlacedLimitOrder(BaseModel):
    commission: Optional[MoneyAmount]
    executed_lots: int
    operation: OperationType
    order_id: str
    reject_reason: Optional[str]
    requested_lots: int
    status: OrderStatus

    class Config:
        fields = {
            'executed_lots': {'alias': 'executedLots'},
            'order_id': {'alias': 'orderId'},
            'reject_reason': {'alias': 'rejectReason'},
            'requested_lots': {'alias': 'requestedLots'},
        }


class PortfolioPosition(BaseModel):
    average_position_price: Optional[MoneyAmount]
    average_position_price_no_nkd: Optional[MoneyAmount]
    balance: float
    blocked: Optional[float]
    expected_yield: Optional[MoneyAmount]
    figi: str
    instrument_type: InstrumentType
    isin: Optional[str]
    lots: int
    ticker: Optional[str]

    class Config:
        fields = {
            'average_position_price': {'alias': 'averagePositionPrice'},
            'average_position_price_no_nkd': {'alias': 'averagePositionPriceNoNkd'},
            'expected_yield': {'alias': 'expectedYield'},
            'instrument_type': {'alias': 'instrumentType'},
        }


class Portfolio(BaseModel):
    positions: List[PortfolioPosition]


class CandlesResponse(BaseModel):
    payload: Candles
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class Empty(BaseModel):
    payload: Dict[str, Any]
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class Error(BaseModel):
    payload: Dict[str, Any]
    status: str = 'Error'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class LimitOrderRequest(BaseModel):
    lots: int
    operation: OperationType
    price: float


class LimitOrderResponse(BaseModel):
    payload: PlacedLimitOrder
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class MarketInstrumentListResponse(BaseModel):
    payload: MarketInstrumentList
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class MarketInstrumentResponse(BaseModel):
    payload: MarketInstrument
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class OperationsResponse(BaseModel):
    payload: Operations
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class OrderbookResponse(BaseModel):
    payload: Orderbook
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class OrdersResponse(BaseModel):
    payload: List[Order]
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class PortfolioCurrenciesResponse(BaseModel):
    payload: Currencies
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class PortfolioResponse(BaseModel):
    payload: Portfolio
    status: str = 'Ok'
    tracking_id: str

    class Config:
        fields = {'tracking_id': {'alias': 'trackingId'}}


class SandboxSetCurrencyBalanceRequest(BaseModel):
    balance: float
    currency: SandboxCurrency


class SandboxSetPositionBalanceRequest(BaseModel):
    balance: float
    figi: Optional[str]


class InstrumentInfoStreamingSchema(BaseModel):
    figi: str
    trade_status: str
    min_price_increment: float
    lot: float
    accrued_interest: Optional[float]
    limit_up: Optional[float]
    limit_down: Optional[float]


class OrderbookStreamingSchema(BaseModel):
    figi: str
    depth: int
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]


class ErrorStreamingSchema(BaseModel):
    error: str
    request_id: Optional[str]


CandleStreamingSchema = Candle
