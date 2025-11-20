#!/usr/bin/env python3
"""
Cookie获取工具
用于获取登录后的所有cookie
"""

import json
import os
import sys
import time
from typing import Dict

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


class CookieGetter:
    def __init__(self, target_url: str = "https://xxx"):
        self.target_url = target_url
        self.driver = None
        self.cookies = {}

    def setup_driver(self, headless: bool = False) -> webdriver.Chrome:
        """设置Chrome浏览器驱动"""
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        # 添加一些常用的Chrome选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # 设置用户代理
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return self.driver
        except WebDriverException as e:
            print(f"❌ Chrome驱动启动失败: {e}")
            print("请确保已安装Chrome浏览器和chromedriver")
            print("如果selenium未安装，请运行: uv add selenium")
            sys.exit(1)

    def wait_for_login(self, timeout: int = 300) -> bool:
        """等待用户完成登录"""
        print(f"🔄 正在访问 {self.target_url}")
        self.driver.get(self.target_url)

        print("⏳ 请在浏览器中完成登录...")
        print(f"⏰ 等待超时时间: {timeout}秒")

        start_time = time.time()

        while time.time() - start_time < timeout:
            current_url = self.driver.current_url

            # 检查是否已经登录成功（不再是登录页面）
            if "login" not in current_url.lower():
                # 额外等待页面完全加载
                time.sleep(3)

                # 检查是否有登录相关的cookie
                cookies = self.driver.get_cookies()
                if cookies:
                    print("✅ 检测到登录成功！")
                    return True

            time.sleep(2)

        print("⏰ 登录超时")
        return False

    def get_cookies(self) -> Dict[str, str]:
        """获取所有cookie"""
        cookies = self.driver.get_cookies()
        cookie_dict = {}

        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        self.cookies = cookie_dict
        return cookie_dict

    def print_all_cookies(self):
        """打印所有cookie信息"""
        print("\n🔐 所有Cookie信息:")
        print("-" * 50)

        if self.cookies:
            for cookie_name, cookie_value in self.cookies.items():
                print(f"  {cookie_name}: {cookie_value}")
        else:
            print("  ⚠️ 未找到任何cookie")

        print("-" * 50)

    def save_cookies_to_file(self, filename: str = "all_cookies.json") -> str:
        """保存所有cookie到文件"""
        filepath = os.path.join(os.path.dirname(__file__), filename)

        # 保存所有cookie
        cookie_data = {
            'url': self.target_url,
            'timestamp': time.time(),
            'cookies': self.cookies
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)

        return filepath

    def format_cookie_header(self) -> str:
        """格式化cookie为HTTP请求头格式"""
        return '; '.join([f"{name}={value}" for name, value in self.cookies.items()])

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='获取登录后的所有cookie')
    parser.add_argument('--url', default='https://xxx',
                        help='目标URL (默认: https://xxx)')
    parser.add_argument('--headless', action='store_true',
                        help='无头模式运行')
    parser.add_argument('--timeout', type=int, default=300,
                        help='登录超时时间(秒) (默认: 300)')
    parser.add_argument('--output', default='all_cookies.json',
                        help='输出文件名 (默认: all_cookies.json)')

    args = parser.parse_args()

    print("🚀 Cookie获取工具启动")
    print(f"📍 目标URL: {args.url}")

    getter = CookieGetter(args.url)

    try:
        # 设置浏览器驱动
        getter.setup_driver(headless=args.headless)

        # 等待用户登录
        if getter.wait_for_login(timeout=args.timeout):
            # 获取cookie
            cookies = getter.get_cookies()

            if cookies:
                print(f"🍪 获取到 {len(cookies)} 个cookie:")
                for name, value in cookies.items():
                    print(f"  - {name}: {value[:20]}...")

                # 打印所有cookie信息
                getter.print_all_cookies()

                # 保存到文件
                filepath = getter.save_cookies_to_file(args.output)
                print(f"💾 Cookie已保存到: {filepath}")

                # 输出HTTP请求头格式
                cookie_header = getter.format_cookie_header()
                print(f"\n📋 HTTP Cookie请求头:")
                print(f"Cookie: {cookie_header}")

                # 输出使用示例
                print(f"\n📖 使用示例:")
                print(f"curl -H 'Cookie: {cookie_header}' {args.url}")

            else:
                print("❌ 未获取到任何cookie")
                sys.exit(1)
        else:
            print("❌ 登录失败或超时")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)
    finally:
        getter.close()
        print("👋 程序结束")


if __name__ == "__main__":
    main()
