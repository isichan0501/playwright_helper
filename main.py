from playwright.sync_api import Playwright, sync_playwright, BrowserContext, Page, Response, expect,BrowserType, Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from xmlrpc.client import Boolean
# from playwright_stealth import stealth_sync
from playwright._impl._api_types import TimeoutError
from typing import Union, List, Set, Tuple, Dict, Optional, Callable, Generator
import re
from util_proxy import random_proxy, format_proxy
from util_device import random_device, generate_device_specs
from util_region import GetMap, convert_region_dict

import os
import sys

import loguru
from loguru import logger
import pysnooper
from importlib import reload
import time
import random
import constants
import asyncio
from dotenv import load_dotenv
import pysnooper
import util_playwright
from importlib import reload

from util_setup import get_browser, get_page, get_context
import happymail
import happy

# 環境変数を参照
load_dotenv()



def main():
    pass
    



if __name__ == '__main__':
    device_name = random_device(os_name='Android');print(device_name)
    device_name = "Nexus 6P"
    login_id, login_pw = "50019903596", "1634"

    from db_helper.util_db import Temple
    temple = Temple(cnm="mika")._get("Temple")
    # import pdb;pdb.set_trace()
    with sync_playwright() as playwright:
        #----debug------
        #----ブラウザ起動
        device = playwright.devices[device_name]
        browser = get_browser(playwright=playwright, device=device, use_headless=False)
        context = get_context(browser, device=device, proxy_info=None)
        page = get_page(context)
        #login
        login_page = happy.LoginPage(page, login_id, login_pw)
        login_page.login()
        #main
        # page.pause()
        # reload(happy)
        
        
        profile_search = happy.ProfileSearchPage(page=page)
        profile_search.select_order(order='登録順')
        profile_search.to_profile_detail()
        import pdb;pdb.set_trace()
        profile_detail = happy.ProfileDetailPage(page=page)
        profile_detail.view_profile()
        user_info = profile_detail.retrive_user_info()
        message_detail = happy.MessageDetailPage(page, temple)
        messages = message_detail.retrive_messages()
        import pdb;pdb.set_trace()
        res = message_detail.execute_action()
        
        context.close()
        browser.close()
        # res = happy.retrive_user_info()
        # print(text_content)