import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

from webdriver_manager.chrome import ChromeDriverManager


class crawling:
    def __init__(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options, service=service)

    # def get_full_link(self, page_url):
    #     all_link = []
    #     self.driver.get(page_url)

    #     time.sleep(5)
    #     wait = WebDriverWait(self.driver, 30)

    #     while True:
    #         try:
    #             element = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
    #             print("Đã tìm thấy 'box-viewmore'")
    #             all_item = self.driver.find_elements(By.CLASS_NAME, 'box-category-item')

    #             for i in all_item:
    #                 a_tag = i.find_element(By.TAG_NAME, "a")
    #                 url = a_tag.get_attribute("href")
    #                 all_link.append(url)
    #             break
    #         except NoSuchElementException:
    #             self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    #             time.sleep(1)

    #     return all_link

    # def get_full_link(self, page_url):
    #     all_link = []
    #     self.driver.get(page_url)

    #     wait = WebDriverWait(self.driver, 30)

    #     # Cuộn xuống cho đến khi thấy nút 'box-viewmore' có thể bấm
    #     while True:
    #         try:
    #             box_viewmore = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
    #             if box_viewmore.is_displayed() and box_viewmore.is_enabled():
    #                 print("Nút 'box-viewmore' đã hiển thị và sẵn sàng.")
    #                 break
    #             else:
    #                 print("Đang cuộn xuống chờ 'box-viewmore' hiển thị...")
    #         except NoSuchElementException:
    #             print("Chưa tìm thấy 'box-viewmore', tiếp tục cuộn...")

    #         self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    #         time.sleep(1)

    #     # Sau khi thấy nút, lấy các link
    #     try:
    #         all_item = self.driver.find_elements(By.CLASS_NAME, 'box-category-item')
    #         for i in all_item:
    #             a_tag = i.find_element(By.TAG_NAME, "a")
    #             url = a_tag.get_attribute("href")
    #             all_link.append(url)
    #     except NoSuchElementException:
    #         print("Không tìm thấy 'box-category-item'.")

    #     return all_link

    def get_full_link(self, page_url, times, file_name):
        all_link = []
        self.driver.get(page_url)

        wait = WebDriverWait(self.driver, 30)

        # Bấm nút "box-viewmore" tối đa 20 lần
        # for i in range(20):
        #     while True:
        #         try:
        #             box_viewmore = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
        #             if box_viewmore.is_displayed() and box_viewmore.is_enabled():
        #                 print(f"[{i+1}/20] Nút 'box-viewmore' đã sẵn sàng.")
        #                 box_viewmore.click()
        #                 time.sleep(2)
        #                 break
        #             else:
        #                 print(f"[{i+1}/20] Đang chờ nút 'box-viewmore'...")
        #         except (NoSuchElementException, ElementClickInterceptedException):
        #             print(f"[{i+1}/20] Không tìm thấy hoặc không thể bấm nút, tiếp tục cuộn xuống.")
        #             self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        #             time.sleep(1)

        # Cuộn xuống cho đến khi thấy nút 'box-viewmore' có thể bấm
        for i in range(times):
            while True:
                try:
                    box_viewmore = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
                    if box_viewmore.is_displayed() and box_viewmore.is_enabled():
                        # print("Nút 'box-viewmore' đã hiển thị và sẵn sàng.")
                        print(f"[{i+1}/{times}] đã hiển thị và sẵn sàng")
                        box_viewmore = self.driver.find_element(By.CLASS_NAME, 'box-viewmore')
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", box_viewmore)
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(1)
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(1)
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(1)
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(1)
                        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(1)
                        time.sleep(1)  # wait for any animation
                        box_viewmore.click()
                        break
                    else:
                        print("Đang cuộn xuống chờ 'box-viewmore' hiển thị...")
                except NoSuchElementException:
                    print("Chưa tìm thấy 'box-viewmore', tiếp tục cuộn...")

                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)

        # Lấy các link sau khi đã mở rộng hết
        try:
            all_item = self.driver.find_elements(By.CLASS_NAME, 'box-category-item')
            for i in all_item:
                a_tag = i.find_element(By.TAG_NAME, "a")
                url = a_tag.get_attribute("href")
                if url and url not in all_link:
                    all_link.append(url)
        except NoSuchElementException:
            print("Không tìm thấy 'box-category-item'.")

        # Ghi tất cả link vào file
        with open(file_name, "w", encoding="utf-8") as f:
            for link in all_link:
                f.write(link + "\n")

        print(f"Đã lưu {len(all_link)} link vào file")
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

save_file = '/Users/nguyenthiphuongthao/Documents/NLP/SVS/crawl-ZingMP3/crawl_U/tuoi_tre/nang_luong_sach'
os.makedirs(save_file, exist_ok=True)
file_name = "/Users/nguyenthiphuongthao/Documents/NLP/SVS/crawl-ZingMP3/crawl_U/link/nang_luong_sach.txt"
times = 5

# bien doi khi hau
# url_page = 'https://tuoitre.vn/tim-kiem.htm?keywords=bi%E1%BA%BFn%20%C4%91%E1%BB%95i%20kh%C3%AD%20h%E1%BA%ADu'

# nang luong sach
url_page = 'https://tuoitre.vn/tim-kiem.htm?keywords=n%C4%83ng%20l%C6%B0%E1%BB%A3ng%20s%E1%BA%A1ch'

# get all the link needed first
# all_item = crawler.get_full_link(url_page, times, file_name)

# crawl all links one by one
with open(file_name, "r") as file:
    for line in file:
        processed_line = line.strip() # or line.rstrip('\n')
        print(processed_line)
        crawler.get_detail(processed_line, save_file)
