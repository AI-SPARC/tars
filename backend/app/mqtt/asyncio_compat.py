import asyncio
import sys
import warnings


def configure_windows_selector_event_loop_policy() -> None:
    """Use selector loops on Windows because aiomqtt/paho needs add_reader/add_writer."""
    if sys.platform != "win32":
        return
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="asyncio")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
