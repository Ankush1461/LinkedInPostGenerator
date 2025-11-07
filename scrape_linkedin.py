# scrape_linkedin.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os


def scrape_linkedin(email, password, profile_url, max_scroll=5, headless=True):
    os.makedirs("data", exist_ok=True)

    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # --- LinkedIn Login ---
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # --- Navigate to profile posts ---
        if not profile_url.endswith("/"):
            profile_url += "/"
        posts_url = profile_url + "detail/recent-activity/shares/"
        driver.get(posts_url)
        time.sleep(5)

        # --- Scroll to load more posts ---
        for _ in range(max_scroll):
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(2)

        posts_data = []
        posts = driver.find_elements(By.CLASS_NAME, "update-components-text")

        for post in posts:
            try:
                text = post.text.strip()
                if not text:
                    continue

                container = post.find_element(By.XPATH, "./ancestor::div[contains(@class, 'occludable-update')]")

                try:
                    likes_elem = container.find_element(By.XPATH,
                                                        ".//button[contains(@aria-label,'like') or contains(@aria-label,'Like')]")
                    likes_text = likes_elem.get_attribute("aria-label")
                    likes = int(''.join(filter(str.isdigit, likes_text))) if any(
                        ch.isdigit() for ch in likes_text) else 0
                except NoSuchElementException:
                    likes = 0

                try:
                    comments_elem = container.find_element(By.XPATH,
                                                           ".//button[contains(@aria-label,'comment') or contains(@aria-label,'Comment')]")
                    comments_text = comments_elem.get_attribute("aria-label")
                    comments = int(''.join(filter(str.isdigit, comments_text))) if any(
                        ch.isdigit() for ch in comments_text) else 0
                except NoSuchElementException:
                    comments = 0

                posts_data.append({
                    "text": text,
                    "engagement": {
                        "likes": likes,
                        "comments": comments
                    }
                })
            except Exception:
                continue

        # Save JSON
        json_path = "data/rawpost.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=4)

        return json_path, len(posts_data)

    finally:
        driver.quit()
