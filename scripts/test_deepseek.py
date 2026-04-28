from playwright.sync_api import sync_playwright
import time

TEST_PROMPT = """https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/INDEX.md

JSON 格式索引（解析更可靠）：https://cdn.jsdelivr.net/gh/bigmanBass666/jason-skill-hub@master/skills/skills.json

使用 awwwards-design 创建一个震撼的沉浸式开发者作品集网站"""

def test_deepseek():
    results = {
        "accessed_index": False,
        "recognized_awwwards": False,
        "got_skill_content": False,
        "got_reference": False,
        "generated_code": False,
        "full_response": ""
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        print("1. 打开 chat.deepseek.com...")
        page.goto('https://chat.deepseek.com')
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        print("2. 截图登录页面...")
        page.screenshot(path='d:/Working/programming_projects/jason-skill-hub/docs/deepseek_login.png', full_page=True)

        print("3. 等待用户登录...")

        input("请在浏览器中登录 DeepSeek，完成后按 Enter 继续...")

        print("4. 检查登录状态...")
        page.screenshot(path='d:/Working/programming_projects/jason-skill-hub/docs/deepseek_after_login.png', full_page=True)

        print("5. 定位输入框并发送测试提示词...")
        page.wait_for_selector('textarea', timeout=10000)
        page.fill('textarea', TEST_PROMPT)

        print("6. 点击发送按钮...")
        page.click('button:has-text("发送")')

        print("7. 等待 AI 开始回复...")
        page.wait_for_selector('.assistant-turn', timeout=30000)

        print("8. 等待 AI 回复完成（最多5分钟）...")
        start_time = time.time()
        max_wait = 300

        last_message_count = 0
        stable_count = 0

        while time.time() - start_time < max_wait:
            page.wait_for_timeout(5000)

            message_count = len(page.locator('.assistant-turn').all())
            print(f"   当前消息数: {message_count}, 已等待: {int(time.time() - start_time)}秒")

            if message_count > 0:
                last_div = page.locator('.assistant-turn').last
                content = last_div.inner_text()
                results["full_response"] = content

                if "index" in content.lower() or "skill" in content.lower():
                    results["accessed_index"] = True
                if "awwwards" in content.lower():
                    results["recognized_awwwards"] = True
                if "skill.md" in content.lower() or "工作流程" in content or "步骤" in content:
                    results["got_skill_content"] = True
                if "reference" in content.lower() or "参考" in content:
                    results["got_reference"] = True
                if "<html" in content.lower() or "<!doctype" in content.lower() or "```html" in content.lower():
                    results["generated_code"] = True

            if message_count == last_message_count and message_count > 0:
                stable_count += 1
                if stable_count >= 3:
                    print(f"   检测到回复已完成（连续{stable_count}次消息数稳定）")
                    break
            else:
                stable_count = 0
                last_message_count = message_count

        print("9. 截图最终结果...")
        page.screenshot(path='d:/Working/programming_projects/jason-skill-hub/docs/deepseek_result.png', full_page=True)

        elapsed = time.time() - start_time
        print(f"\n总等待时间: {int(elapsed)}秒")

        print("\n=== 测试结果 ===")
        print(f"1. 访问 INDEX.md: {'✅' if results['accessed_index'] else '❌'}")
        print(f"2. 识别 awwwards-design: {'✅' if results['recognized_awwwards'] else '❌'}")
        print(f"3. 获取 SKILL.md 内容: {'✅' if results['got_skill_content'] else '❌'}")
        print(f"4. 处理引用文件: {'✅' if results['got_reference'] else '❌'}")
        print(f"5. 生成网站代码: {'✅' if results['generated_code'] else '❌'}")

        passed = sum([
            results["accessed_index"],
            results["recognized_awwwards"],
            results["got_skill_content"],
            results["got_reference"],
            results["generated_code"]
        ])
        print(f"\n通过: {passed}/5")

        if results["full_response"]:
            print("\n=== AI 回复内容（前3000字符）===")
            print(results["full_response"][:3000])

        browser.close()

        return results

if __name__ == "__main__":
    test_deepseek()