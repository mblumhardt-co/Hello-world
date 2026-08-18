"""The order record the sell agent fills out.

Modeled as a pragmatic subset of a carrier ASR (Access Service Request) in
ASOG format for an Ethernet access circuit. Field names/defaults here are a
reasonable starting point, not a certified ASOG implementation -- validate
against your actual trading-partner spec before using this for real orders.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

# Fields the buyer must supply before an order can be submitted.
ESSENTIAL_FIELDS = [
    "pon",
    "bandwidth_mbps",
    "site_address",
    "desired_due_date",
    "contact_name",
    "contact_phone",
]

# Fields the agent derives/defaults on its own rather than asking the buyer.
ENRICHABLE_DEFAULTS = {
    "act": "N",
    "evc_type": "Point-to-Point",
    "class_of_service": "Best Effort",
}


@dataclass
class AsrOrder:
    pon: str

    # Activity / lifecycle
    act: str = "N"                     # N = new, C = change, D = disconnect
    status: str = "draft"              # draft -> submitted -> in_progress -> completed / cancelled

    # Buyer / contact
    buyer_company: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

    # Service basics (essential)
    bandwidth_mbps: Optional[int] = None
    site_address: Optional[str] = None
    desired_due_date: Optional[str] = None

    # Service basics (enriched/derived, not asked unless the buyer volunteers them)
    service_type: Optional[str] = None       # e.g. "Ethernet Private Line"
    evc_type: Optional[str] = None           # Point-to-Point / Point-to-Multipoint
    z_location: Optional[str] = None         # nearest carrier POP, derived from site_address
    vlan_id: Optional[int] = None
    cir_mbps: Optional[int] = None
    eir_mbps: Optional[int] = None
    class_of_service: Optional[str] = None

    special_instructions: Optional[str] = None

    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def missing_essential_fields(self) -> list[str]:
        return [f for f in ESSENTIAL_FIELDS if getattr(self, f) in (None, "")]

    def apply_enrichment_defaults(self) -> None:
        """Fill in derivable fields that are still empty, at submit time."""
        for key, value in ENRICHABLE_DEFAULTS.items():
            if getattr(self, key) in (None, ""):
                setattr(self, key, value)
        if not self.cir_mbps and self.bandwidth_mbps:
            self.cir_mbps = self.bandwidth_mbps
        if not self.eir_mbps and self.bandwidth_mbps:
            self.eir_mbps = self.bandwidth_mbps
        if not self.service_type and self.bandwidth_mbps:
            self.service_type = f"Ethernet Private Line - {self.bandwidth_mbps} Mbps"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AsrOrder":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in known})
