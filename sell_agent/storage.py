"""Local JSON-file storage for orders, keyed by PON."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .asr import AsrOrder

ORDERS_DIR = Path(__file__).resolve().parent.parent / "orders"

# PONs become filenames, so restrict them to a safe character set.
_VALID_PON = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\-_.]{0,63}$")


def normalize_pon(pon: str) -> str:
    pon = (pon or "").strip()
    if not _VALID_PON.match(pon):
        raise ValueError(
            "PON must be 1-64 characters, starting with a letter or digit, "
            "using only letters, digits, '-', '_' or '.'"
        )
    return pon


def _path_for(pon: str) -> Path:
    return ORDERS_DIR / f"{normalize_pon(pon)}.json"


def order_exists(pon: str) -> bool:
    return _path_for(pon).exists()


def load_order(pon: str) -> Optional[AsrOrder]:
    path = _path_for(pon)
    if not path.exists():
        return None
    return AsrOrder.from_dict(json.loads(path.read_text()))


def save_order(order: AsrOrder) -> None:
    ORDERS_DIR.mkdir(parents=True, exist_ok=True)
    order.updated_at = datetime.now(timezone.utc).isoformat()
    path = _path_for(order.pon)
    path.write_text(json.dumps(order.to_dict(), indent=2))


def list_orders() -> list[AsrOrder]:
    if not ORDERS_DIR.exists():
        return []
    orders = [AsrOrder.from_dict(json.loads(p.read_text())) for p in ORDERS_DIR.glob("*.json")]
    return sorted(orders, key=lambda o: o.created_at, reverse=True)
