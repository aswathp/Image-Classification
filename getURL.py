import time
from attr import attributes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import io
from PIL import Image

options = Options()
options.binary_location = "D:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options = options, executable_path='D:\Personal Files\Project\chromedriver.exe')
wd = driver

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    url = "https://www.google.com/search?q=max+verstappen&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiPyp_92qX5AhWSTGwGHTinAzEQ_AUoAnoECAIQBA&biw=1536&bih=747&dpr=1.25"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips :max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb KAlRDb")        
            for image in images:
                if image.get_attributes('src') in image_urls:
                    max_images+=1
                    skips +=1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    #print(f"Found {len(image_urls)}")
    return image_urls




#image_url = "https://www.formula1.com/content/fom-website/en/drivers/max-verstappen/_jcr_content/image.img.640.medium.jpg/1646819045507.jpg"

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
        print('FAILED -',e)

#download_image("", image_url, "max.jpg")

urls = get_images_from_google(wd, 1, 10)
#print(urls)
for i, url in enumerate(urls):
    download_image("Max Verstappe/",url, str(i)+".jpg")

wd.quit()