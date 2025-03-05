import tkinter as tk
from tkinter import ttk
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

# Function to send a message to the webhook URL
def send_webhook_message(webhook_url, message):
    try:
        requests.post(webhook_url, json={"content": message})
    except Exception as e:
        print("Error sending webhook:", e)

# Function to search the Steam Marketplace
def search_weapons():
    threading.Thread(target=search_weapons_thread, daemon=True).start()

def search_weapons_thread():
    weapon = weapon_textbox.get("1.0", "end-1c")  # Get the weapon entered in the textbox
    pages = int(pages_entry.get())
    webhook_url = webhook_textbox.get("1.0", "end-1c")  # Get the webhook URL from the textbox
    
    send_webhook_message(webhook_url, "✅ **Kingsley Charm On Weapon Finder Started!**")
    send_webhook_message(webhook_url, f"🔍 Searching for listings of: {weapon}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    
    base_url = "https://steamcommunity.com/market/listings/730/"
    weapon_url = f"{base_url}{weapon.replace(' ', '%20')}"
    
    for page in range(pages):
        driver.get(f"{weapon_url}?start={page * 10}&count=10")
        time.sleep(3)
        
        listings = driver.find_elements(By.CLASS_NAME, "market_listing_row")
        for listing in listings:
            try:
                title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "market_listing_item_name"))).text
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                # Look for the keychain div (which contains the charm)
                try:
                    keychain_div = listing.find_element(By.ID, "keychain_info")
                    if keychain_div:
                        # Extract the name of the charm from the image alt or src attribute
                        charm_name = keychain_div.find_element(By.TAG_NAME, "img").get_attribute("alt")
                        if not charm_name:
                            # If no alt attribute is found, use the image src as the charm name
                            charm_name = keychain_div.find_element(By.TAG_NAME, "img").get_attribute("src").split("/")[-1].split(".")[0]
                        
                        # Send a message with the charm's page number and name
                        message = f"🎯 **Weapon Found with Charm!**\n**Weapon:** {title}\n**Charm Name:** {charm_name}\n**Page:** {page + 1}\n🔗 [View Listing]({link})"
                        send_webhook_message(webhook_url, message)
                except:
                    # No charm found, do nothing
                    pass
            except Exception as e:
                print("Error parsing listing:", e)
    
    driver.quit()
    send_webhook_message(webhook_url, "✅ **Search Complete!**")

# GUI setup
root = tk.Tk()
root.title("Kingsley Charm On Weapon Finder")

# Discord Webhook URL textbox
webhook_label = tk.Label(root, text="Enter Discord Webhook URL:")
webhook_label.grid(row=0, column=0, padx=10, pady=5)
webhook_textbox = tk.Text(root, height=1, width=40)  # A larger textbox for webhook URL input
webhook_textbox.grid(row=0, column=1, padx=10, pady=5)
webhook_textbox.insert("1.0", "discord webhook url")  # Set the default value

# Weapon textbox
weapon_label = tk.Label(root, text="Enter weapon:")
weapon_label.grid(row=1, column=0, padx=10, pady=5)
weapon_textbox = tk.Text(root, height=1, width=40)  # A larger textbox for weapon input
weapon_textbox.grid(row=1, column=1, padx=10, pady=5)
weapon_textbox.insert("1.0", "StatTrak™ MAC-10 | Heat (Factory New)")  # Set the default value

# Pages textbox
pages_label = tk.Label(root, text="Pages:")
pages_label.grid(row=2, column=0, padx=10, pady=5)
pages_entry = tk.Entry(root, width=10)
pages_entry.grid(row=2, column=1, padx=10, pady=5)
pages_entry.insert(0, "1")

# Search button
search_button = tk.Button(root, text="Search", command=search_weapons)
search_button.grid(row=3, column=0, columnspan=2, pady=10)

# Credits label
credits_label = tk.Label(root, text="By KingsleydotDev", font=("Arial", 8), fg="gray")
credits_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
