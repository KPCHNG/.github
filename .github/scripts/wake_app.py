from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import time

STREAMLIT_URL = os.environ.get("STREAMLIT_URL", "")

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    print("🚀 Starting Chrome driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 1 - Open the URL
        print(f"🌐 Opening {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        print(f"📄 Page title: {driver.title}")
        print(f"🔗 Current URL: {driver.current_url}")

        # Step 2 - Wait for page to fully render
        print("⏳ Waiting 5 seconds for page to render...")
        time.sleep(5)

        # Step 3 - Look for wake button
        print("🔍 Looking for wake-up button...")
        wait = WebDriverWait(driver, 30)

        try:
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("✅ Wake-up button found!")

            # Step 4 - Click the button
            print("👆 Clicking the wake-up button...")
            button.click()

            print("⏳ Waiting 1 minute for app to wake up...")
            time.sleep(60)

            # Step 6 - Reload and verify
            print("🔄 Reloading page to verify app is awake...")
            driver.get(STREAMLIT_URL)
            time.sleep(10)

            # Step 7 - Final check
            print("🔍 Checking if app is fully awake...")
            time.sleep(10)

            if "Yes, get this app back up" in driver.page_source:
                print("❌ App still sleeping after 2 minutes!")
                exit(1)
            else:
                print("🎉 App is fully awake and running!")

        except TimeoutException:
            print("ℹ️ No wake-up button found.")
            if "Yes, get this app back up" in driver.page_source:
                print("❌ App is sleeping but button not clickable!")
                exit(1)
            else:
                print("✅ App is already awake!")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)

    finally:
        driver.quit()
        print("🏁 Script finished.")

if __name__ == "__main__":
    main()
