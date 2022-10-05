from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "D:\Program Files\Google\Chrome\Application\chrome.exe"



wd = webdriver.Chrome(chrome_options = options, executable_path='D:\Personal Files\Project\chromedriver.exe')

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q=sebastian+vettel&tbm=isch&ved=2ahUKEwiz57G-o6b5AhXMjtgFHUU5B8AQ2-cCegQIABAA&oq=seb&gs_lcp=CgNpbWcQARgAMgoIABCxAxCDARBDMgQIABBDMgQIABBDMgoIABCxAxCDARBDMgQIABBDMgcIABCxAxBDMgQIABBDMggIABCABBCxAzIECAAQQzIECAAQQzoLCAAQgAQQsQMQgwE6CAgAELEDEIMBOgUIABCABFC2C1j7EGDzGWgAcAB4AIABgAGIAd8DkgEDMC40mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=KhzoYrOqMsyd4t4PxfKcgAw&bih=792&biw=1536"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 0.5, 90)

for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg")

wd.quit()