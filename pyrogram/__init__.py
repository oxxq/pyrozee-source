__fork_name__ = "nekozee"
__version__ = "2"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "#  Copyright (C) 2024-present Z-Mirror <https://github.com/Dawn-India/Z-Mirror>"

from concurrent.futures.thread import ThreadPoolExecutor

class StopTransmission(Exception):
    pass

class StopPropagation(StopAsyncIteration):
    pass

class ContinuePropagation(StopAsyncIteration):
    pass

from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")
