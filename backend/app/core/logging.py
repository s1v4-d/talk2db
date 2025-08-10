"""Centralised logging setup for the backend."""

import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

# Create a module level logger for reuse
logger = logging.getLogger("talk_to_db")