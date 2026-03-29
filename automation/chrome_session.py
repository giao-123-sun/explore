"""
Chrome Session — 复用 Chrome 已登录的 session
用法：
  python automation/chrome_session.py [url]
  python automation/chrome_session.py https://twitter.com --proxy
默认打开 baidu.com 验证登录状态（直连）
加 --proxy 走代理访问外网
"""

import sys
import shutil
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME_USER_DATA = Path(r"C:\Users\sunqi\AppData\Local\Google\Chrome\User Data")
PROXY_SERVER = "http://127.0.0.1:7890"
DEFAULT_URL = "https://www.baidu.com"


def copy_profile(src: Path, dst: Path):
    """选择性拷贝 Chrome profile 关键文件"""
    for item in [
        "Default/Cookies", "Default/Login Data", "Default/Preferences",
        "Default/Secure Preferences", "Default/Network/Cookies", "Local State",
    ]:
        s = src / item
        if s.exists():
            d = dst / item
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
    dd = dst / "Default"
    dd.mkdir(exist_ok=True)
    for f in (src / "Default").iterdir():
        if f.is_file() and f.stat().st_size < 10_000_000:
            shutil.copy2(f, dd / f.name)


def main():
    use_proxy = "--proxy" in sys.argv
    args_clean = [a for a in sys.argv[1:] if a != "--proxy"]
    url = args_clean[0] if args_clean else DEFAULT_URL

    tmp = Path(tempfile.mkdtemp(prefix="chrome_session_"))
    print(f"[*] 临时 profile: {tmp}")
    print(f"[*] 拷贝 Chrome profile...")
    copy_profile(CHROME_USER_DATA, tmp)

    try:
        with sync_playwright() as p:
            launch_args = ["--no-proxy-server"]
            kwargs = dict(
                user_data_dir=str(tmp),
                channel="chrome",
                headless=False,
                args=launch_args,
            )
            if use_proxy:
                # --no-proxy-server 屏蔽系统代理，proxy 参数走 Playwright 自己的代理
                kwargs["proxy"] = {"server": PROXY_SERVER}
                kwargs["args"] = []  # 不加 --no-proxy-server，让 Playwright proxy 生效
                # 但要屏蔽系统代理，改用 --proxy-server 强制指定
                kwargs["args"] = [f"--proxy-server={PROXY_SERVER}"]
                print(f"[*] 代理: {PROXY_SERVER}")
            else:
                print(f"[*] 直连（无代理）")

            ctx = p.chromium.launch_persistent_context(**kwargs)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            print(f"[*] 访问 {url} ...")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            print(f"[+] 页面标题: {page.title()}")

            cookies = ctx.cookies()
            print(f"[+] 总 cookie 数: {len(cookies)}")

            # 检查目标域名的 cookie
            from urllib.parse import urlparse
            domain = urlparse(url).hostname or ""
            domain_parts = domain.split(".")[-2:]  # 取主域名
            domain_key = ".".join(domain_parts)
            matched = [c for c in cookies if domain_key in c.get("domain", "")]
            if matched:
                print(f"[+] {domain_key} cookie: {len(matched)} 个 — 已登录")
                for c in matched[:5]:
                    print(f"    {c['name']}: {c['domain']}")
            else:
                print(f"[-] {domain_key} cookie: 0 — 未登录或无 cookie")

            print(f"\n[*] 浏览器已打开。按 Enter 关闭...")
            input()
            ctx.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
