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
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
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

            # 随机延迟
            def random_delay(min_seconds=0.5, max_seconds=2.0):
                return random.uniform(min_seconds, max_seconds)

            # 随机移动鼠标
            async def random_move_mouse(page, x_min, x_max, y_min, y_max):
                x = random.randint(x_min, x_max)
                y = random.randint(y_min, y_max)
                await page.mouse.move(x, y)



            # 模拟用户行为
            await asyncio.sleep(1*random_delay())  # 随机延迟
            await page.mouse.move(50, 50)  # 随机移动鼠标
            await random_move_mouse(page, 0, 800, 0, 600)
            await asyncio.sleep(1*random_delay())
            await page.mouse.down()
            await asyncio.sleep(0.1*random_delay())
            await page.mouse.up()
            await asyncio.sleep(2*random_delay())
            await page.keyboard.press('ArrowDown')  # 模拟键盘操作
            await asyncio.sleep(1*random_delay())


            await page.close()
            await context.close()
            await browser.close()

            return result

        except Exception as e:
            logging.error(f"Error fetching page {url}: {str(e)}")
            raise