from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Page, Response, expect,BrowserType, Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from xmlrpc.client import Boolean
# from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator
import re



class LoginPage:

    def __init__(self, page: Page, login_id: str, login_pw: str) -> None:
        self.page = page
        self.login_id = login_id
        self.login_pw = login_pw

    def login(self) -> Boolean:
        self.page.goto("https://happymail.co.jp/login/")
        self.page.get_by_placeholder("電話番号／会員番号").fill(self.login_id)
        self.page.get_by_role("textbox", name="暗証番号").fill(self.login_pw)
        self.page.locator("#login_btn").click()
        expect(self.page).to_have_url(re.compile(r".*/mbmenu"))
        return True
        # page.locator("[id=\"_information_dialog\"]").get_by_role("link").click(button="right")