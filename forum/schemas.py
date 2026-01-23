from datetime import datetime

from ninja import Schema
from decimal import Decimal



class Newsout(Schema):
    id: int
    news_name: str
    description_of_news: str
    rate_for_news: int
    data_giving: datetime









