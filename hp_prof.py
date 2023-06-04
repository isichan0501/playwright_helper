from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Page, Response, expect,BrowserType, Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from xmlrpc.client import Boolean
# from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator
import re
import util_playwright
from importlib import reload
import hp_login



# https://happymail.co.jp/sp/app/html/mypage.php

class MyPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def set_image(self, img_path=None):
        
# https://happymail.co.jp/sp/app/html/my_profile_picture_and_movie.php


def run(page: Page) -> None:
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="編集する").click()
    try:
        
    # page.get_by_text("メイン設定中").click()
    page.get_by_role("img", name="photo").first.click()
    page.get_by_role("dialog").get_by_role("img").click()
    page.get_by_text("ファイルを選択").click()
    page.get_by_text("ja 戻る 画像を送信 ホーム プロフ検索 掲示板 メッセージ マイページN ファイルが選択されていません ファイルを選択 送信する ※3G回線の場合は送信する").set_input_files("resultt23.jpg")
    page.get_by_text("ファイルを選択").click()
    page.get_by_text("ja 戻る 画像を送信 ホーム プロフ検索 掲示板 メッセージ マイページN resultt23.jpg ファイルを選択 送信する ※3G回線の場合は送信するの").set_input_files("resultt23.jpg")
    page.get_by_text("ファイルを選択").click(button="right")
    page.get_by_text("ファイルを選択").click(button="right")
    page.get_by_role("button", name="送信する").click()
    page.get_by_role("button", name="OK").click()
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="編集する").click()
    page.get_by_role("img", name="photo").first.click()



with sync_playwright() as playwright:
    run(playwright)
