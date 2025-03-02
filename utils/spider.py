import asyncio
import random
import logging
from pyppeteer import launch
from config.settings import USER_AGENTS, BROWSER_CONFIG


class Spider:
    @staticmethod
    async def create_browser(proxy=None):
        """创建浏览器实例"""
        launch_args = [
            '--disable-infobars',
            f'--window-size={BROWSER_CONFIG["window_size"]["width"]},{BROWSER_CONFIG["window_size"]["height"]}'
        ]

        if proxy:
            launch_args.append(f'--proxy-server={proxy}')

        browser = await launch(
            headless=BROWSER_CONFIG['headless'],
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            args=launch_args
        )
        return browser

    @staticmethod
    async def setup_page(context, cookies=None, user_agent=None):
        """设置页面配置"""
        page = await context.newPage()
        await page.evaluateOnNewDocument(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        )

        if cookies:
            await page.setCookie(*cookies)

        if not user_agent:
            user_agent = random.choice(USER_AGENTS)
        await page.setUserAgent(user_agent)

        return page, user_agent

    @staticmethod
    async def fetch_page(url, cookies=None, proxy=None, user_agent=None):
        """获取页面内容"""
        try:
            browser = await Spider.create_browser(proxy)
            context = await browser.createIncognitoBrowserContext()

            page, used_ua = await Spider.setup_page(context, cookies, user_agent)

            await page.goto(url, {'waitUntil': 'networkidle2'})
            content = await page.content()
            current_cookies = await page.cookies()

            result = {
                'content': content,
                'cookie': current_cookies,
                'ua': used_ua
            }

            await page.close()
            await context.close()
            await browser.close()

            return result

        except Exception as e:
            logging.error(f"Error fetching page {url}: {str(e)}")
            raise