import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class crawling:
    def __init__(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options, service=service)

    def get_full_link(self, page_url):
        all_link = []
        self.driver.get(page_url)

        time.sleep(5)
        wait = WebDriverWait(self.driver, 30)

        while True:
            try:
                element = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
                print("Đã tìm thấy 'box-viewmore'")
                all_item = self.driver.find_elements(By.CLASS_NAME, 'box-category-item')

                for i in all_item:
                    a_tag = i.find_element(By.TAG_NAME, "a")
                    url = a_tag.get_attribute("href")
                    all_link.append(url)
                break
            except NoSuchElementException:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)

        return all_link

    def get_detail(self, page_url, save_file):
        try:
            self.driver.get(page_url)
            time.sleep(10)
            wait = WebDriverWait(self.driver, 30)

            try:
                main_page = self.driver.find_element(By.ID, 'main-detail')
            except NoSuchElementException:
                print(f"[SKIPPED] Không tìm thấy 'main-detail' ở trang: {page_url}")
                return  # Skip this page

            all = [page_url]

            title = main_page.find_element(By.TAG_NAME, 'h1').text
            all.append(title)

            pub_t = main_page.find_element(By.CLASS_NAME, 'detail-time').text
            all.append(pub_t)

            full_text = []
            text1 = main_page.find_element(By.CLASS_NAME, 'detail-sapo').text
            full_text.append(text1)

            text2 = main_page.find_element(By.CLASS_NAME, "detail-cmain")
            text2 = text2.find_element(By.CLASS_NAME, 'detail-content')
            text2 = text2.find_elements(By.TAG_NAME, 'p')
            for i in text2:
                full_text.append(i.text)

            text_body = ' '.join(full_text)
            all.append(text_body)

            name_file = title.replace(" ", "_").replace("/", "_").lower()
            save_file_path = f"{save_file}/{name_file}.txt"

            if os.path.exists(save_file_path):
                print(f"[EXISTS] File đã tồn tại, bỏ qua: {save_file_path}")
                return  # Skip saving if file exists

            with open(save_file_path, 'w') as file:
                for line in all:
                    file.write(line + "\n")

            print(f"[SAVED] Đã lưu: {save_file_path}")

        except Exception as e:
            print(f"[ERROR] Lỗi khi xử lý {page_url}: {e}")


# --- CHẠY CODE ---
crawler = crawling()

save_file = '/Users/nguyenthiphuongthao/Documents/NLP/SVS/crawl-ZingMP3/crawl_U/tuoi_tre'
os.makedirs(save_file, exist_ok=True)

url_page = 'https://tuoitre.vn/tim-kiem.htm?keywords=bi%E1%BA%BFn%20%C4%91%E1%BB%95i%20kh%C3%AD%20h%E1%BA%ADu'
all_item = crawler.get_full_link(url_page)

for i in all_item[1:]:  # bỏ qua link đầu tiên nếu cần
    crawler.get_detail(i, save_file)
