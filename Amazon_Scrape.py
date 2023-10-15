from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()
scrape_url = f"https://www.amazon.com.tr/s?k=Protein"
protein_name = []
protein_price = []
driver.get(scrape_url+"&page=1")
driver.maximize_window()

pages = 3
last_page = int(pages-1)
time.sleep(2)
for i in range(1, last_page+1):
    time.sleep(2)
    proteins = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

    for protein in proteins:

        names = protein.find_elements(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']")
        for name in names:
            protein_name.append(name.text)

        try:
            if len(protein.find_elements(By.XPATH, ".//span[@class='a-price-whole']")) > 0:
                prices = protein.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
                for price in prices:
                    # print('the lenght is ===>',len(price.text))
                    protein_price.append(price.text)
            else:
                protein_price.append("0")
        except:
            pass
    print('no of proteins==>', len(protein_name))
    print('no of prices==>', len(protein_price))
    driver.quit()

    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get(scrape_url + "&page=" + str(i + 1))

    df = pd.DataFrame(zip(protein_name, protein_price), columns=['protein_name', 'protein_price'])

    df.to_excel(f'./amazon-data-scrape.xlsx', index=False)