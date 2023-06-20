import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def scrape_url(url, what_to_scrape):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP requests
        soup = BeautifulSoup(response.content, "html.parser")
        data = [tag.text for tag in soup.find_all(what_to_scrape, class_="s1t1hnwn-2")]
        if len(data) == 0:
            print("No data found.")
        return data
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print("Error occurred:", e)
        return []

def show_dataset(data):
    window = tk.Tk()
    window.title("Dataset")

    if len(data) == 0:
        print("No data found.")
        return

    table = ttk.Treeview(window)
    table.column("Data", width=200)
    table.heading("Data", text="Data")

    for row in data:
        table.insert("", "end", values=(row,))

    table.pack()
    window.mainloop()

def export_dataset(data, filename):
    import csv
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Data"])
        for row in data:
            writer.writerow([row])

def main():
    url = input("Enter the URL: ")
    what_to_scrape = input("What do you want to scrape? (e.g., h1, p, etc.): ")
    data = scrape_url(url, what_to_scrape)
    show_dataset(data)
    export_dataset(data, "dataset.csv")

if __name__ == "__main__":
    main()
