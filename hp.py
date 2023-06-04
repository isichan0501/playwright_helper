from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Page, Response, expect,BrowserType, Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from xmlrpc.client import Boolean
# from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator
import re

from playwright.sync_api import sync_playwright

from playwright.sync_api import sync_playwright
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
    HOME_URL = "https://happymail.co.jp/sp/app/html/mbmenu.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.get_by_role("link", name="ホーム").click()

class AreaPage:
    HOME_URL = "https://happymail.co.jp/sp/app/html/area.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.locator("xpath=//div[@class='ds_header_td']").click()

    
    def move_temporarily(self):
        # 一時的な移動処理
        self.page.get_by_text("一時的に移動").click()
    
    def relocation(self, area="23", city="1050"):
        # 引っ越し処理
        self.page.get_by_text("引越し").click()
        self.page.locator("#area").select_option(area)
        self.page.locator("#city").select_option(city)
        self.page.locator("#data-btn-detail-area-select-decide").click()


class ProfileSearchPage:
    HOME_URL = "https://happymail.co.jp/sp/app/html/profile_list.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.get_by_role("link", name="プロフ検索").click()

    def select_order(self, order='登録順'):
        #kind=0:プロフ一覧
        self.page.locator("#kind_select").select_option("0")
        if order == '登録順':
            self.page.locator("#order_select").select_option("1")
        else:
            self.page.locator("#order_select").select_option("0")


class SearchConditionPage:
    HOME_URL = "https://happymail.co.jp/sp/app/html/profile_list_search.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            self.page.get_by_placeholder("検索条件を設定する").click()
            
    def set_conditions(self):
        # 検索条件の設定処理
        # self.page.locator("//div[@class='ds_user_display']").click()
        self.page.locator("//li[@id='search-interest_area']//a").click()
        

        pass

class ProfileDetailPage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://happymail.co.jp/sp/app/html/profile_detail_list.php?a=a&from=prof&idx=1")
    
    def view_profile(self):
        # プロフィールの詳細表示処理
        pass
    
    def register_no_watch(self):
        # 見ちゃいや登録処理
        pass
    
    def register_ignore(self):
        # 無視登録処理
        pass
    
    def register_memo(self):
        # メモ登録処理
        pass
    
    def view_message_detail(self):
        # メッセージの詳細表示処理
        pass

class BulletinBoardPage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://happymail.co.jp/sp/app/html/keijiban.php")
    
    def view_board(self):
        # 掲示板の表示処理
        pass
    
    def write_post(self):
        # 掲示板への書き込み処理
        pass

class MessagePage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://happymail.co.jp/sp/app/html/message_list.php")
    
    def view_unread(self):
        # 未読メッセージの表示処理
        pass

class MyPage:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://happymail.co.jp/sp/app/html/mypage.php")
    
    def view_images_and_videos(self):
        images_and_videos_page = MyPage.ImagesAndVideosPage(self.page)
        images_and_videos_page.view()

    def view_profile(self):
        profile_page = MyPage.ProfilePage(self.page)
        profile_page.view()

    def view_footprints(self):
        footprints_page = MyPage.FootprintsPage(self.page)
        footprints_page.view()

    def view_my_list(self):
        my_list_page = MyPage.MyListPage(self.page)
        my_list_page.view()

    class ImagesAndVideosPage:
        def __init__(self, page):
            self.page = page
            self.page.goto("https://happymail.co.jp/sp/app/html/my_profile_picture_and_movie.php")
        
        def view(self):
            # 画像や動画の表示処理
            pass

    class ProfilePage:
        def __init__(self, page):
            self.page = page
            self.page.goto("https://happymail.co.jp/sp/app/html/profile.php")
        
        def view(self):
            # プロフィールの表示処理
            pass

        def view_self_introduction(self):
            self_introduction_page = MyPage.ProfilePage.SelfIntroductionPage(self.page)
            self_introduction_page.view()

        def view_nickname(self):
            nickname_page = MyPage.ProfilePage.NicknamePage(self.page)
            nickname_page.view()

        class SelfIntroductionPage:
            def __init__(self, page):
                self.page = page
                self.page.goto("https://happymail.co.jp/sp/app/html/profileComment.php?a=a")
            
            def view(self):
                # 自己紹介の表示処理
                pass

        class NicknamePage:
            def __init__(self, page):
                self.page = page
                self.page.goto("https://happymail.co.jp/sp/app/html/nickname_setting.php")
            
            def view(self):
                # ニックネームの表示処理
                pass

    class FootprintsPage:
        def __init__(self, page):
            self.page = page
            self.page.goto("https://happymail.co.jp/sp/app/html/ashiato.php")
        
        def view(self):
            # 足あとの表示処理
            pass

        def view_profile_detail(self):
            profile_detail_page = MyPage.FootprintsPage.ProfileDetailPage(self.page)
            profile_detail_page.view()

        class ProfileDetailPage:
            def __init__(self, page):
                self.page = page
                self.page.goto("https://happymail.co.jp/sp/app/html/profile_detail.php?a=a&tid=51253842&nf=1")
            
            def view(self):
                # プロフィールの詳細表示処理
                pass

            def view_message_detail(self):
                message_detail_page = MyPage.FootprintsPage.ProfileDetailPage.MessageDetailPage(self.page)
                message_detail_page.view()

            class MessageDetailPage:
                def __init__(self, page):
                    self.page = page
                    self.page.goto("https://happymail.co.jp/sp/app/html/message_detail.php?mailID=EgdkgQXolM8J22F%2BJHiPjjFHpobeuVl%2FAiLxJxi9YIk%3D")
                
                def view(self):
                    # メッセージの詳細表示処理
                    pass

    class MyListPage:
        def __init__(self, page):
            self.page = page
            self.page.goto("https://happymail.co.jp/sp/app/html/my_list.php")
        
        def view(self):
            # マイリストの表示処理
            pass

        def view_board_history(self):
            board_history_page = MyPage.MyListPage.BoardHistoryPage(self.page)
            board_history_page.view()

        class BoardHistoryPage:
            def __init__(self, page):
                self.page = page
                self.page.goto("https://happymail.co.jp/sp/app/html/keijiban_write_log.php")
            
            def view(self):
                # 掲示板履歴の表示処理
                pass


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()

    # ログイン
    login_page = LoginPage(context.new_page())
    login_page.login()

    # ホーム
    home_page = HomePage(context.new_page())
    home_page.navigate()

    # エリア移動
    area_page = AreaPage(context.new_page())
    area_page.move_temporarily()
    area_page.move_with_move()

    # プロフ検索
    profile_search_page = ProfileSearchPage(context.new_page())
    profile_search_page.search()

    # 検索条件
    search_condition_page = SearchConditionPage(context.new_page())
    search_condition_page.set_conditions()

    # プロフィール詳細
    profile_detail_page = ProfileDetailPage(context.new_page())
    profile_detail_page.view_profile()
    profile_detail_page.register_watch()
    profile_detail_page.register_ignore()
    profile_detail_page.register_memo()
    profile_detail_page.view_message_detail()

    # 掲示板
    bulletin_board_page = BulletinBoardPage(context.new_page())
    bulletin_board_page.view_board()
    bulletin_board_page.write_post()

    # メッセージ
    message_page = MessagePage(context.new_page())
    message_page.view_unread()

    # マイページ
    mypage_page = MyPage(context.new_page())
    mypage_page.view_images_and_videos()
    mypage_page.view_profile()
    mypage_page.view_self_introduction()
    mypage_page.view_nickname()
    mypage_page.view_footprints()
    mypage_page.view_profile_detail()
    mypage_page.view_message_detail()
    mypage_page.view_my_list()
    mypage_page.view_board_history()

    # ブラウザの終了
    context.close()
    browser.close()
