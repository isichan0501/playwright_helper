from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Page, Response, expect,BrowserType, Browser
from playwright._impl._api_structures import ProxySettings
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


from xmlrpc.client import Boolean
# from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator

from .util_proxy import random_proxy, format_proxy
from .util_device import random_device, generate_device_specs
from .util_region import GetMap, convert_region_dict

import os
import sys

import loguru
from loguru import logger
import pysnooper
from importlib import reload
import time
import random
from . import constants
import asyncio
from dotenv import load_dotenv
import pysnooper

# 環境変数を参照
load_dotenv()
SMART_PROXY_JP = os.environ.get('SMART_PROXY_JP')


"""やること
random_deviceで使用可能なデバイス名を取得
device = playwright.devices[デバイス名]の
default_browser_type(chromium, webkit, firefox)をチェックして場合分け。
constants.py からブラウザ引数を取得。


"""

def get_browser(
    playwright: Playwright,
    device: Dict,
    use_headless: Boolean = False
    ) -> Browser:
    if device['default_browser_type'] == 'firefox':
        browser = playwright.firefox.launch(
            headless=use_headless,
            args=[
                '--start-maximized',
                '--foreground',
                '--disable-backgrounding-occluded-windows'
            ],
            firefox_user_prefs=constants.FIREFOX_SETTINGS
            # proxy=helpers.get_random_proxy(),
        )
        return browser
    elif device['default_browser_type'] == 'webkit':
        browser = playwright.webkit.launch(
            headless=use_headless,
            args=[
                '--start-maximized',
                '--foreground',
                '--disable-backgrounding-occluded-windows'
            ]
        )
        return browser

    else:
        browser = playwright.chromium.launch(
            headless=use_headless,
            args=[
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--allow-running-insecure-content',
            ],
            # devtools=True,
            chromium_sandbox=False
        )
        return browser


def get_context(
    browser: Browser,
    device: Dict,
    proxy_info: str = None
    ) -> BrowserContext:

    if proxy_info:
        context = browser.new_context(
            **device,
            accept_downloads=True,
            locale='ja-JP',
            timezone_id='Asia/Tokyo',
            # geolocation={"longitude": 136.881694, "latitude": 35.1706431},
            # permissions=["geolocation"],
            # java_script_enabled=True,
            ignore_https_errors=True,
            proxy=format_proxy(proxy_info=proxy_info)
        )
        return context
    else:
        context = browser.new_context(
            **device,
            accept_downloads=True,
            locale='ja-JP',
            timezone_id='Asia/Tokyo',
            # geolocation={"longitude": 136.881694, "latitude": 35.1706431},
            # permissions=["geolocation"],
            # java_script_enabled=True,
            ignore_https_errors=True
        )
        return context

def get_page(
    context: BrowserContext
    ) -> Page:
    page = context.new_page()
    page.add_init_script(script=constants.SPOOF_FINGERPRINT % generate_device_specs())
    return page

def run(
    playwright: Playwright, 
    device_name: str = None,
    use_headless: Boolean = False,
    proxy_info: str = None
    ) -> Boolean:
    
    device = playwright.devices[device_name]
    browser = get_browser(playwright=playwright, device=device, use_headless=use_headless)
    # Create a new context with the saved storage state.
    # context = browser.new_context(storage_state="state.json")
    context = get_context(browser, device=device, proxy_info=proxy_info)
    page = get_page(context)
    
    page.goto("https://gologin.com/ja/check-browser")
    page.pause()
    context.storage_state(path="state.json")


if __name__ == '__main__':
    device_name = random_device(os_name='Android')
    # import pdb;pdb.set_trace()
    with sync_playwright() as playwright:
        run(playwright, device_name=device_name)
        


