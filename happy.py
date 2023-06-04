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
import random
from pprint import pprint
import pysnooper
from util_playwright import get_next_message, extract_email, send_gmail


def select_option_if_not_selected(page, select_selector, option_value):
    # 選択されているoption要素のvalue属性を取得します
    selected_option_value = page.eval_on_selector(
        f'{select_selector} > option[selected]', 
        'option => option.value'
    )

    # 指定したオプションが選択されていない場合にだけ選択します
    if selected_option_value != option_value:
        page.select_option(select_selector, option_value)


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




    # ---------------------


@pysnooper.snoop()
def profile_detail(page: Page) -> None:

    if page.url != "https://happymail.co.jp/sp/app/html/profile_list.php":
        page.get_by_role("link", name="プロフ検索").click()

    page.wait_for_load_state('load')
    select_option_if_not_selected(page, select_selector="#kind_select", option_value="0")
    select_option_if_not_selected(page, select_selector="#order_select", option_value="1") # optin_value=0: ログイン順

    # page.locator("#kind_select").select_option("0")
    # page.locator("#order_select").select_option("1")
    users = page.locator("//*[@id=\"list-profile\"]/li").all()
    not_see_user = [elem for elem in users if "ds_user_post_link_item_r" == elem.get_attribute("class")]
    if len(not_see_user) == 0:
        page.reload()
        return None
    
    elem = random.choice(not_see_user)
    elem.click()

    def retrive_user_info():
        #user info
        elements = page.locator("xpath=//div[@class='swiper-slide swiper-slide-active']/input").all()
        user_dict = {x.get_attribute('name'):x.get_attribute('value') for x in elements}
        
        return user_dict


    
    def regist_no_watch():
        page.get_by_role("link", name="その他").click()

        #見ちゃいや登録
        page.get_by_role("link", name="見ちゃいや登録").click()
        # page.get_by_placeholder("メモ内容(250文字まで・空白可)").click()
        # page.get_by_placeholder("メモ内容(250文字まで・空白可)").fill("ok")
        page.get_by_role("button", name="登録").click()
        page.get_by_role("button", name="OK").click()


    # page.get_by_role("link", name="その他").click()
    # page.locator("#footer_menu").click()


    # ---------------------


def write_keijiban(page: Page) -> None:
    page.get_by_role("link", name="掲示板").click()
    page.get_by_role("figure", name="書く").get_by_role("link").click()
    page.get_by_text("その他掲示板", exact=True).click()
    page.get_by_text("ピュア掲示板", exact=True).click()
    page.get_by_placeholder("タイトル（全角30文字）").click()
    page.get_by_placeholder("タイトル（全角30文字）").fill("恋の予感...♥ #出逢いのヒロイン")
    page.get_by_placeholder("本文（全角800文字）").click()
    page.get_by_placeholder("本文（全角800文字）").fill("こんばんは！\nアパレル店員として働く24歳の「みか」だよ☆\nこのサイトに登録した理由は、新しい友達を作りたくて、彼氏も欲しいから（笑）💕\n\n身長は159cmで、普通体型。見た目は可愛い系で、ファッションセンスも自信あり◎\n友達とおしゃべりや映画鑑賞、食事に行くのが大好き！彼氏との理想のデートは、テーマパークや映画館、カフェ巡り♪\n\n気軽にメッセージ送ってね！よろしくお願いします♪✨")
    page.get_by_role("button", name="書き込む").click()

    # ---------------------


def message_list(page: Page) -> None:
    page.get_by_role("link", name="メッセージ").click()
    page.get_by_text("未読").click()
    page.get_by_role("link", name="♂ ぽん 30代半ば 名古屋市 06/03 14:28 かおりさん、こんにちは！\nたまたま暇してたらエッチしませんか？？？").click()

    #send message
    page.get_by_placeholder("メッセージ入力").click()
    page.get_by_placeholder("メッセージ入力").fill("いいですよー！")
    page.get_by_role("button", name="送信", exact=True).click()
    #mityaiya
    page.locator("#ds_js_media_display_btn div").click()
    page.get_by_role("link", name="見ちゃいや").click()
    page.get_by_role("button", name="登録").click()
    page.get_by_role("button", name="OK").click()
    #
    page.locator(".common__table__cell").click()
    page.locator("#ds_js_media_display_btn div").click()
    page.locator("#ds_js_media_display_btn div").click()

    # ---------------------


def images_and_videos(page: Page, img_path: str) -> None:
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="編集する").click()
    # page.get_by_text("メイン設定中").click()
    page.get_by_role("img", name="photo").first.click()
    # page.get_by_role("dialog").get_by_role("img").click()
    # page.get_by_text("ファイルを選択").click()
    page.locator("xpath=//input[@id=\"upload_file\"]").set_input_files(img_path)
    page.get_by_role("button", name="送信する").click()
    page.get_by_role("button", name="OK").click()


def profile(page:Page):
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="プロフィール").click()
    page.get_by_role("link", name="かおり").click()
    page.get_by_text("かおり").click(click_count=3)
    page.get_by_text("かおり").fill("みか")
    page.locator("label").filter(has_text="保存").click()
    page.get_by_role("button", name="変更する").click()
    page.get_by_role("link", name="タップして設定する").click()
    page.get_by_placeholder("本文入力(500字以内)").click()
    page.get_by_placeholder("本文入力(500字以内)").fill("こんばんは！\nアパレル店員として働く24歳の「みか」だよ☆\nこのアプリに登録した理由は、新しい友達を作りたくて、彼氏も欲しいから（笑）💕\n\n身長は159cmで、普通体型。見た目は可愛い系で、ファッションセンスも自信あり◎\n友達とおしゃべりや映画鑑賞、食事に行くのが大好き！彼氏との理想のデートは、テーマパークや映画館、カフェ巡り♪\n\n気軽にメッセージ送ってね！よろしくお願いします♪✨")
    page.get_by_text("審査", exact=True).click()
    page.get_by_role("button", name="提出する").click()
    page.locator("select[name=\"member_birth_area\"]").select_option("35")
    page.locator("select[name=\"blood_type\"]").select_option("1")
    page.locator("select[name=\"constellation\"]").click()
    page.locator("select[name=\"constellation\"]").select_option("1")
    page.locator("select[name=\"height\"]").select_option("4")
    page.locator("select[name=\"style\"]").select_option("2")
    page.locator("select[name=\"type\"]").select_option("3")
    page.locator("select[name=\"job\"]").select_option("16")
    page.locator("select[name=\"marriage\"]").select_option("1")
    page.locator("select[name=\"housemate\"]").select_option("1")
    page.locator("select[name=\"first_date_cost\"]").select_option("3")
    page.locator("img:nth-child(5)").first.click()
    page.locator("div:nth-child(5) > div:nth-child(2) > .input__form__input > .ds_rating > img:nth-child(5)").click()
    page.locator("div:nth-child(6) > div:nth-child(2) > .input__form__input > .ds_rating > img:nth-child(5)").click()
    page.locator("select[name=\"hope_age_low\"]").select_option("1")
    page.locator("select[name=\"hope_height_high\"]").select_option("10")

    # ---------------------


def FootPrint(page: Page) -> None:
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="足あと 99+").click()
    page.get_by_role("link", name="プロフィールより ♂tk 20代半ば 名古屋市中村区 06/03 18:21 掲載 6").click()

    #メッセージ
    page.get_by_role("link", name="メールする").click()
    page.get_by_placeholder("メッセージ入力").click()
    page.get_by_placeholder("メッセージ入力").fill("はーい！")
    page.get_by_role("button", name="送信", exact=True).click()



def keijiban_write_log(page: Page) -> None:
    page.get_by_role("link", name="マイページ").click()
    page.get_by_role("link", name="マイリスト New").click()
    page.get_by_role("link", name="掲示板履歴").click()
    page.get_by_text("その他掲示板").click()
    page.locator("#adults-posting-list").click()
    page.get_by_text("トータル0件").click()
    page.get_by_text("ピュア掲示板").click()
    page.get_by_text("トータル1件").click()
    page.locator("#pure-posting-list").click()

    # ---------------------


from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt, stop_after_delay, wait_fixed, wait_random

class ProfileSearchPage:
    HOME_URL = "https://happymail.co.jp/sp/app/html/profile_list.php"
    def __init__(self, page):
        self.page = page
        self.navigate()

    def navigate(self):
        if self.page.url != self.HOME_URL:
            if len(self.page.get_by_role("link", name="プロフ検索").all()) == 0:
                self.page.get_by_alt_text("ハッピーメール").click()
            self.page.get_by_role("link", name="プロフ検索").click(timeout=3000)
            self.page.wait_for_load_state('load')

    def select_order(self, order='登録順'):
        self.navigate()
        #kind=0:プロフ一覧
        select_option_if_not_selected(self.page, select_selector="#kind_select", option_value="0")
        # optin_value=0: ログイン順
        if order == '登録順':
            select_option_if_not_selected(self.page, select_selector="#order_select", option_value="1")
        else:
            select_option_if_not_selected(self.page, select_selector="#order_select", option_value="0")


    def to_profile_detail(self):
        self.navigate()
        users = self.page.locator("//*[@id=\"list-profile\"]/li").all()
        not_see_user = [elem for elem in users if "ds_user_post_link_item_r" == elem.get_attribute("class")]
        if len(not_see_user) == 0:
            self.page.reload()
            return None
        elem = random.choice(not_see_user)
        elem.click()
        self.page.wait_for_load_state('load')


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
        page = self.page
        page.get_by_role("link", name="プロフ検索").click()
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
        page.get_by_role("term").filter(has_text="愛知県").locator("label").click()
        page.get_by_role("term").filter(has_text="三重県").locator("label").click()
        page.locator("label").filter(has_text="三重県").nth(1).click()
        page.get_by_role("term").filter(has_text="三重県").locator("label").click()
        page.get_by_role("button", name="地域を決定する").click()
        page.locator("#search-form").get_by_text("指定しない 18～19歳20代前半20代半ば20代後半30代前半30代半ば30代後半40代前半40代半ば40代後半50代前半50代半ば50代後半60代以上 ～ ").click()
        page.locator("#search-form select[name=\"interest_age_high\"]").select_option("10")
        page.locator("#search-form select[name=\"interest_age_low\"]").select_option("1")
        page.get_by_role("button", name="この条件を保存する").click()
        page.get_by_placeholder("検索条件名(8文字まで)").click()
        page.get_by_placeholder("検索条件名(8文字まで)").fill("1")
        page.get_by_role("button", name="保存する", exact=True).click()
        page.locator("#kind_select").select_option("0")
        page.locator("#order_select").select_option("1")
        self.page.locator("//li[@id='search-interest_area']//a").click()
        

import difflib



class MessageDetailPage:
    
    def __init__(self, page, temple):
        self.page = page
        self.temple = temple
        self.formurl = temple['formurl']
        self.sender_name = temple['namae']
        self.money = temple['money']
        self.mailado = temple['mailado']
        self.kenmei = temple['kenmei']
        self.meruado = temple['meruado']
        self.after_mail = temple['after_mail']
        self.hajime = temple['hajime']
        self.asiato = temple['asiato']

    def navigate(self):
        if 'profile_detail_list' in self.page.url:
            if len(self.page.get_by_role("link", name="メールする").all()) > 0:
                self.page.get_by_role("link", name="メールする").click()

    def retrive_messages(self):
        """message['content']に声通話の申請を含むものをはじく"""
        #送受信メッセージ
        elements = self.page.locator("#list_message_detail > div").filter(has=self.page.locator('[class*="message__block"]')).all()
        #受信か送信か
        message_history = []
        for elem in elements:
            #時間
            timestamp = self.page.locator('#list_message_detail > div.message__date').text_content().strip() + elem.locator('div.message__block__body__time').text_content().strip()
            message_schema = {
                "type": elem.get_attribute('class').split('--')[-1],
                "content": elem.locator('div.message__block__body__text').text_content().strip(),
                "timestamp": timestamp
            }
            message_history.append(message_schema)
        return message_history

    def regist_no_watch(self):
        self.page.locator("#ds_js_media_display_btn div").click()
        self.page.get_by_role("link", name="見ちゃいや").click()
        self.page.get_by_role("button", name="登録").click()
        self.page.get_by_role("button", name="OK").click()
    
    def execute_action(self):
        #Gmail送信用
        #使うテンプレ
        message_templates = [self.meruado, self.after_mail]
        #メッセージ一覧
        messages = self.retrive_messages()
        #名前取得
        namae = self.page.locator('#main-contents-message-header > label.app__navbar__item.app__navbar__item--title').text_content().strip()
        # message = message.replace('namae', namae)
        message_templates = [msg.replace('namae', namae) for msg in message_templates]
        #送信メッセージのコンテンツのみ
        messages = [m['content'] for m in messages if m['type'] == 'send']
        #未使用のテンプレート（次に送るテンプレート)
        message_template = get_next_message(messages=messages, message_templates=message_templates, similarity_threshold=0.8)
        #aftermailも送信済みなら終了
        if not message_template:
            print('end')
            return None

        receives = "\n".join([m['content'] for m in messages if m['type'] != 'send'])
        email_address = extract_email(search_txt=receives)
        if email_address:
            print('email found')
            #Email送信
            kenmei = self.kenmei.replace('namae', namae)
            for _ in range(3):
                is_success = send_gmail(formurl=self.formurl, sender_name=self.sender_name, money=self.money, mailado=email_address, kenmei=kenmei)
                if is_success:
                    break
            #after_mail送信
            self.send_message(message=message_template)
            
            #みちゃいや登録
            self.regist_no_watch()
            return None

        #残りのテンプレートがafter_mailのみ=メルアド落とし送信済みの場合
        if len(message_template) == 1:
            print('メルアド落ちない.end')
            return None

        #メルアド落とし未送信
        self.send_message(message=message_template)
        print('メルアド落とし送信')
        return None
        

    def send_message(self, message):
        #新規メッセージ
        # page.get_by_placeholder("メッセージ入力").click()
        self.page.get_by_placeholder("メッセージ入力").fill(message)
        self.page.get_by_role("button", name="送信", exact=True).click()
        #popup
        self.page.get_by_role("button", name="はい(メッセージ送信)").click()


class ProfileDetailPage(ProfileSearchPage):
    def __init__(self, page):
        self.page = page
        # self.page.goto("https://happymail.co.jp/sp/app/html/profile_detail_list.php?a=a&from=prof&idx=1")
        super().__init__(page=self.page)

    def view_profile(self):
        # プロフィールの詳細表示処理
        super().select_order(order='登録順')
        super().to_profile_detail()

    @classmethod
    def get_dict_from_profile_content(cls, profile_content):
        vals = profile_content.split()
        while len(vals) > 0:
            k = vals.pop(0)
            v = vals.pop(0)
            yield (k,v)

    # res=happy.extract_text_content(page)
    def extract_text_content(self, page):
        head_selector_base = '#list-profile-detail > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > div.ds_link_tab_content.fade.in > div'
        body_selector_base = '#list-profile-detail > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > div.ds_link_tab_content.fade.in > div'
        child_range = range(len(page.locator(head_selector_base).all()))
        result = {}
        for i in child_range:
            try:
                head_selector = f'{head_selector_base}:nth-child({i}) > div.ds_common_head'
                body_selector = f'{body_selector_base}:nth-child({i}) > div.ds_common_body'

                head_value = page.eval_on_selector(head_selector, 'element => element.innerText')
                body_value = page.eval_on_selector(body_selector, 'element => element.innerText')

                result[head_value] = body_value
            except Exception:
                print('end')

        #自己紹介以外は辞書の値が辞書になるよう変換
        for k,v in result.items():
            if '自己紹介' in k:
                continue
            result[k] = dict(self.get_dict_from_profile_content(profile_content=v))

        return result

    def retrive_user_info(self):
        #user info
        page = self.page
        elements = self.page.locator("xpath=//div[@class='swiper-slide swiper-slide-active']/input").all()
        #['seq_id', 'sex', 'member_sex_number', 'name', 'favorite_url', 'memo_url', 'member_memo', 'member_memo_category', 
        # 'mail_url', 'like_on', 'tel_on', 'type_on', 'age_confirmed', 'idx', 'member_beginner', 'musi_url', 'musi_text', 
        # 'michaiya_url', 'michaiya_text', 'tuho_url', 'mail_history', 'taikai']
        user_dict = {x.get_attribute('name'):x.get_attribute('value') for x in elements}
        text_content = self.extract_text_content(page)
        user_dict.update(text_content)
        return user_dict


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
        if len(self.page.get_by_role("link", name="メールする").all()) > 0:
            self.page.get_by_role("link", name="メールする").click()


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


# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     context = browser.new_context()

#     # ログイン
#     login_page = LoginPage(context.new_page())
#     login_page.login()

#     # ホーム
#     home_page = HomePage(context.new_page())
#     home_page.navigate()

#     # エリア移動
#     area_page = AreaPage(context.new_page())
#     area_page.move_temporarily()
#     area_page.move_with_move()

#     # プロフ検索
#     profile_search_page = ProfileSearchPage(context.new_page())
#     profile_search_page.search()

#     # 検索条件
#     search_condition_page = SearchConditionPage(context.new_page())
#     search_condition_page.set_conditions()

#     # プロフィール詳細
#     profile_detail_page = ProfileDetailPage(context.new_page())
#     profile_detail_page.view_profile()
#     profile_detail_page.register_watch()
#     profile_detail_page.register_ignore()
#     profile_detail_page.register_memo()
#     profile_detail_page.view_message_detail()

#     # 掲示板
#     bulletin_board_page = BulletinBoardPage(context.new_page())
#     bulletin_board_page.view_board()
#     bulletin_board_page.write_post()

#     # メッセージ
#     message_page = MessagePage(context.new_page())
#     message_page.view_unread()

#     # マイページ
#     mypage_page = MyPage(context.new_page())
#     mypage_page.view_images_and_videos()
#     mypage_page.view_profile()
#     mypage_page.view_self_introduction()
#     mypage_page.view_nickname()
#     mypage_page.view_footprints()
#     mypage_page.view_profile_detail()
#     mypage_page.view_message_detail()
#     mypage_page.view_my_list()
#     mypage_page.view_board_history()

#     # ブラウザの終了
#     context.close()
#     browser.close()
