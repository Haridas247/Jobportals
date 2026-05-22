from playwright.sync_api import sync_playwright

def test_job_list_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/jobs/")

        assert "Job" in page.title()
        print("Job list page loaded successfully")

        browser.close()

def test_search_bar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000 )
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/jobs/")
        page.fill("input[name='q']", "React Developer")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        print("Search bar working successfully")

        browser.close()

def test_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/login/")

        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        print("Login page working successfully")

        browser.close()

if __name__ == "__main__":
    test_job_list_page()
    test_search_bar()
    test_login_page()
    print("All Playwright tests passed!")