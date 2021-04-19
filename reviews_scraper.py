from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

path = "/Users/macbookpro/Documents/ChromeDriver/chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.imdb.com/title/tt5052448/reviews?ref_=tt_urv")

movie_name = driver.find_element_by_class_name("parent").text
movie_name = movie_name.replace(" ", "_")
movie_name = movie_name.lower() + ".csv"

for i in range(64):
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "load-more-trigger"))
        )
        button.click()

    except:
        driver.implicitly_wait(5)


reviews = []
try:
    all_reviews = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "content"))
    )
    all_ratings = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "rating-other-user-rating"))
    )
    full_review = ""
    for i, j in zip(all_ratings,all_reviews):
        full_review = i.text + " | " + j.text
        reviews.append(full_review)

except:
    driver.quit()

df = pd.DataFrame(reviews)
df.rename(columns={0 : "Review"},inplace=True)
df.to_csv(movie_name)