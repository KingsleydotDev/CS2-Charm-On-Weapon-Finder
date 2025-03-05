# Kingsley Charm On Weapon Finder

## Description
This is a Python-based GUI application that searches the Steam Community Market for specific weapon listings that have a charm attached. The program automates the search process using Selenium and sends notifications via a Discord webhook.

## Features
- GUI built with Tkinter for easy user interaction.
- Automated searching on the Steam Marketplace using Selenium.
- Headless Chrome WebDriver for efficiency.
- Webhook notifications to Discord for found listings.
- Multi-page search functionality.

## Requirements
Before running the script, ensure you have the following dependencies installed:

```
pip install tkinter requests selenium webdriver-manager
```

Additionally, make sure you have Google Chrome installed, as Selenium will use it to perform the searches.

## Usage
1. Run the script using Python:
   ```
   python Kingsley Charm On Weapon Finder.py
   ```
2. Enter your Discord webhook URL in the provided text box.
3. Specify the weapon name exactly as it appears on the Steam Market.
4. Enter the number of pages to search.
5. Click the "Search" button.
6. The bot will send Discord messages when a matching weapon with the Kingsley charm is found.

## Notes
- The script runs in headless mode, meaning no browser window will appear during execution.
- The charm detection relies on Steam Market's listing structure, which may change over time.
- If you encounter issues, try updating Selenium and `webdriver-manager`.

## Author
Developed by **KingsleydotDev**.

## License
This project is licensed under the MIT License.
