from ariadne import ScalarType
from datetime import datetime

datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime) -> str:
    return value.isoformat()
