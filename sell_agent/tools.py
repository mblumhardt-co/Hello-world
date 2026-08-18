"""Tool definitions the sell agent uses to record and persist order data.

The buyer never sees these names or schemas -- Claude calls them silently
while chatting in plain English.
"""

import json

from . import storage
from .asr import AsrOrder

# Fields the model is allowed to set via update_order_fields.
_EDITABLE_FIELDS = {
    "buyer_company",
    "contact_name",
    "contact_phone",
    "contact_email",
    "bandwidth_mbps",
    "site_address",
    "desired_due_date",
    "service_type",
    "evc_type",
    "z_location",
    "vlan_id",
    "cir_mbps",
    "eir_mbps",
    "class_of_service",
    "special_instructions",
}


class ToolError(Exception):
    pass


TOOLS = [
    {
        "name": "start_new_order",
        "description": (
            "Create a new draft order tracked by the buyer's PON (Purchase Order Number). "
            "Call this once, as soon as the buyer gives you a PON for a new order."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pon": {"type": "string", "description": "The buyer's PON for this order."},
            },
            "required": ["pon"],
            "additionalProperties": False,
        },
    },
    {
        "name": "lookup_order",
        "description": "Look up an order (new or existing) by its PON to check status and details.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pon": {"type": "string", "description": "The PON to look up."},
            },
            "required": ["pon"],
            "additionalProperties": False,
        },
    },
    {
        "name": "update_order_fields",
        "description": (
            "Save one or more pieces of order information as you learn them from the buyer. "
            "Call this incrementally -- don't wait until you have everything. Only include "
            "fields you actually have a value for; omit anything unknown."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pon": {"type": "string", "description": "The PON of the order to update."},
                "buyer_company": {"type": "string"},
                "contact_name": {"type": "string"},
                "contact_phone": {"type": "string"},
                "contact_email": {"type": "string"},
                "bandwidth_mbps": {"type": "integer", "description": "Requested port bandwidth in Mbps."},
                "site_address": {"type": "string", "description": "The buyer's service (A-end) location."},
                "desired_due_date": {"type": "string", "description": "Requested date the service should be turned up, e.g. an ISO date."},
                "service_type": {"type": "string"},
                "evc_type": {"type": "string", "description": "Point-to-Point or Point-to-Multipoint."},
                "z_location": {
                    "type": "string",
                    "description": "The carrier's nearest network point of presence serving the site -- derive this yourself from the site address, don't ask the buyer.",
                },
                "vlan_id": {"type": "integer"},
                "cir_mbps": {"type": "integer"},
                "eir_mbps": {"type": "integer"},
                "class_of_service": {"type": "string"},
                "special_instructions": {"type": "string"},
            },
            "required": ["pon"],
            "additionalProperties": False,
        },
    },
    {
        "name": "submit_order",
        "description": (
            "Finalize and submit the order once the buyer has confirmed the summary. "
            "Fails with a list of missing fields if required information is still outstanding."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pon": {"type": "string"},
            },
            "required": ["pon"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_recent_orders",
        "description": "List recent orders (PON and status only) -- useful if the buyer isn't sure of their PON.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


def _order_summary(order: AsrOrder) -> dict:
    return {
        "pon": order.pon,
        "status": order.status,
        "missing_essential_fields": order.missing_essential_fields(),
        "order": order.to_dict(),
    }


def execute_tool(name: str, tool_input: dict) -> dict:
    if name == "start_new_order":
        pon = storage.normalize_pon(tool_input["pon"])
        if storage.order_exists(pon):
            raise ToolError(f"An order with PON '{pon}' already exists. Use lookup_order instead.")
        order = AsrOrder(pon=pon)
        storage.save_order(order)
        return _order_summary(order)

    if name == "lookup_order":
        pon = storage.normalize_pon(tool_input["pon"])
        order = storage.load_order(pon)
        if order is None:
            raise ToolError(f"No order found with PON '{pon}'.")
        return _order_summary(order)

    if name == "update_order_fields":
        pon = storage.normalize_pon(tool_input["pon"])
        order = storage.load_order(pon)
        if order is None:
            raise ToolError(f"No order found with PON '{pon}'. Call start_new_order first.")
        for key, value in tool_input.items():
            if key == "pon":
                continue
            if key not in _EDITABLE_FIELDS:
                raise ToolError(f"Unknown field '{key}'.")
            setattr(order, key, value)
        storage.save_order(order)
        return _order_summary(order)

    if name == "submit_order":
        pon = storage.normalize_pon(tool_input["pon"])
        order = storage.load_order(pon)
        if order is None:
            raise ToolError(f"No order found with PON '{pon}'.")
        order.apply_enrichment_defaults()
        missing = order.missing_essential_fields()
        if missing:
            storage.save_order(order)
            raise ToolError(f"Cannot submit -- still missing: {', '.join(missing)}")
        order.status = "submitted"
        storage.save_order(order)
        return _order_summary(order)

    if name == "list_recent_orders":
        orders = storage.list_orders()[:20]
        return {"orders": [{"pon": o.pon, "status": o.status} for o in orders]}

    raise ToolError(f"Unknown tool '{name}'")


def run_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Returns (result_text, is_error) for use in a tool_result content block."""
    try:
        result = execute_tool(name, tool_input)
        return json.dumps(result), False
    except ToolError as e:
        return str(e), True
    except Exception as e:  # malformed input, unexpected errors
        return f"Unexpected error: {e}", True
