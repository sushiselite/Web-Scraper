import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_reddit(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Scroll down to load more content
        SCROLL_PAUSE_TIME = 2

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(SCROLL_PAUSE_TIME)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = [title.text for title in soup.find_all("h3")]
        if len(data) == 0:
            print("No data found.")
        return data
    except Exception as e:
        print("Error occurred:", e)
        return []
    
def show_dataset(data):
    window = tk.Tk()
    window.title("Dataset")

    if len(data) == 0:
        print("No data found.")
        return

    table = ttk.Treeview(window)
    table["columns"] = ("Data")

    table.column("Data", width=200)
    table.heading("Data", text="Data")

    for row in data:
        table.insert("", "end", values=(row,))

    table.pack()
    window.mainloop()

def export_dataset(data, filename):
    import csv
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Data"])
        for row in data:
            writer.writerow([row])


def main():
    url = "https://www.reddit.com/"  # Example URL for Reddit homepage
    data = scrape_reddit(url)
    show_dataset(data)
    export_dataset(data, "dataset.csv")

if __name__ == "__main__":
    main()
