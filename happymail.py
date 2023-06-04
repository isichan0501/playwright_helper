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
import time

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
        time.sleep(3)
        self.page.reload()
        return True
        # page.locator("[id=\"_information_dialog\"]").get_by_role("link").click(button="right")



class HomePage:
    """https://happymail.co.jp/sp/app/html/mbmenu.php

    import happymail
    hp = happymail.HomePage(page=page)

    """
    HOME_URL = "https://happymail.co.jp/sp/app/html/mbmenu.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.get_by_role("link", name="ホーム").click()


class AreaMove:
    """https://happymail.co.jp/sp/app/html/mbmenu.php

    import happymail
    hp = happymail.HomePage(page=page)

    """
    HOME_URL = "https://happymail.co.jp/sp/app/html/area.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.get_by_role("link", name="ホーム").click()

    def area_move(self):
        # xpath="*//a[@href=\"//happymail.co.jp/sp/app/html/area.php\"]"
        # self.page.locator("*//a[@href=\"//happymail.co.jp/sp/app/html/area.php\"]").click()
        self.page.get_by_role("link", name="東京都").click()
        
    def temporary_move(self):
        self.page.get_by_text("一時的に移動").click()
        print('temp')

    def relocation(self):
        self.page.get_by_text("引越し").click()
        self.page.locator("#area").select_option("23")
        self.page.locator("#city").select_option("1050")
        self.page.locator("#data-btn-detail-area-select-decide").click()
        

    


class ProfileSearchPage:
    def __init__(self, page):
        self.page = page
        page.get_by_role("link", name="プロフ検索").click()


    def select_order(self, order='登録順'):
        #kind=0:プロフ一覧
        self.page.locator("#kind_select").select_option("0")
        if order == '登録順':
            self.page.locator("#order_select").select_option("1")
        else:
            self.page.locator("#order_select").select_option("0")


    def search_conditions(self):
        page = self.page
        page.get_by_placeholder("検索条件を設定する").click()
        page.get_by_role("link", name="愛知県").click()
        page.get_by_role("term").filter(has_text="東海").locator("label").click()
        page.get_by_role("term").filter(has_text="岐阜県").locator("label").click()
        page.locator("label").filter(has_text="岐阜県").nth(1).click()
        page.get_by_role("term").filter(has_text="岐阜県").locator("label").click()
        page.get_by_role("term").filter(has_text="静岡県").locator("label").click()
        page.locator("label").filter(has_text="静岡県").nth(1).click()
        page.get_by_role("term").filter(has_text="静岡県").locator("label").click()
        page.get_by_role("term").filter(has_text="愛知県").locator("label").click()
        page.locator("label").filter(has_text="愛知県").nth(1).click()
        page.get_by_role("term").filter(has_text="愛知県").locator("label").click()
        page.get_by_role("term").filter(has_text="三重県").locator("label").click()
        page.locator("label").filter(has_text="三重県").nth(1).click()
        page.get_by_role("term").filter(has_text="三重県").locator("label").click()
        page.get_by_role("button", name="地域を決定する").click()
        page.get_by_text("さらにこだわる").click()
        page.get_by_role("button", name="この条件を保存する").click()
        page.get_by_placeholder("検索条件名(8文字まで)").click()
        page.get_by_placeholder("検索条件名(8文字まで)").fill("1")
        page.get_by_role("button", name="保存する", exact=True).click()



    def profile_details(self):
        self.page.get_by_role("dialog").get_by_role("img").click()
        self.page.get_by_role("link", name="♂ 勝男さん 60代以上 愛知県 06/03 13:09").click()
    def message_details():
        pass
        

class BulletinBoardPage:
    def __init__(self, page):
        self.page = page

    def bulletin_posting(self):
        def pure_bulletin_board():
            pass
        
        def other_bulletin_board():
            pass
        
        pure_bulletin_board()
        other_bulletin_board()

class MessagePage:
    def __init__(self, page):
        self.page = page

    def unread_messages(self):
        def message_details():
            pass
        
        message_details()

class MyPage:
    def __init__(self, page):
        self.page = page

    def images_and_videos(self):
        pass
    
    def self_introduction(self):
        pass
    
    def profile(self):
        self.self_introduction()
    
    def footprints(self):
        def profile_details():
            def message_details():
                pass
            
            message_details()
        
        profile_details()

    def my_list(self):
        def bulletin_board_history():
            pass
        
        bulletin_board_history()
    
class ProfileSearchPage:
    #https://happymail.co.jp/sp/app/html/profile_list.php
    class SearchConditions:
        #https://happymail.co.jp/sp/app/html/profile_list_search.php
        pass

    class ProfileDetails:
        class MessageDetails:
            pass

class BulletinBoardPage:
    class BulletinPosting:
        class PureBulletinBoard:
            pass

        class OtherBulletinBoard:
            pass

class MessagePage:
    class UnreadMessages:
        class MessageDetails:
            pass

class MyPage:
    class ImagesAndVideos:
        pass

    class Profile:
        class SelfIntroduction:
            pass

    class Footprints:
        class ProfileDetails:
            class MessageDetails:
                pass

    class MyList:
        class BulletinBoardHistory:
            pass