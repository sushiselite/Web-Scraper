import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def scrape_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        data = [title.text for title in soup.find_all("h3")]
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
    table["columns"] = ("Data")

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
    url = "https://www.reddit.com/"  # Example URL for Reddit homepage
    data = scrape_url(url)
    show_dataset(data)
    export_dataset(data, "dataset.csv")

if __name__ == "__main__":
    main()
