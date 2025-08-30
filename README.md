# eBay Scraper

A Python project to scrape eBay listings automatically.  
It includes a **Flask backend** for API handling and a **PyQt6 GUI** for easy interaction.  

> ⚠️ Some scripts (like `run_backend.py`) are for debugging purposes only.
> ⚠️ When you create a request, you should be as precise as possible in your product name and be sure to write more details.
- Even though I’ve tried try to get the best results for each product, i'm not responsable for sales announcement from the eBay website and disappointment could be arrived

---

## Features

- Possibilities for user to create "requests" and interact with them (read,delete...)
- Automatic product search on eBay browse API and receive data from the twelve most appropriate items
- Category suggestions using eBay taxonomy API
- Create BUY or SELL options for each product and receive an alert when the price reaches the price in the user request
> **Receive product with minimum value and his URL for BUY option and products with minimum/maximum values and median of all products with their URL for SELL option**
> *The alert is triggered for the SELL option if the price is within ±15% of the reference value during 5 days in a row*
> *The alert is triggered for the BUY option if the price is under the reference value*
- Flask backend API
- PyQt6 GUI for local interaction
- Easy to configure for your own API keys
- Receive data on your Discord using webhook

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hanto-13th/Ebay-Scraper.git
cd Ebay-Scraper
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Add your .env file with your API keys (not included in repo) following the .env_exemple (copy .env_example to .env and fill your keys):

EBAY_API_KEY=your_ebay_api_key
DISCORD_WEBHOOK_URL=your_discord_webhook

---

## Usage

- Run the APP:
```bash
python run_scraper_app.py
```
- Run each part independently (for debugging purposes)
```bash
python run_backend.py
```
```bash
python run_db.py
```
> ⚠️ It is important that the backend is running first as the GUI communicates with it.

---

## Example Usage

- Using the GUI:
1. Launch it with python run_scraper_app.py
2. Create a request: Enter a product name , a price to reach and a option BUY or SELL 
3. Click "Send the EBAY Data to Discord", wait and view the results directly in your own Discord.

---

## Structure

.
|
|-- backend
|   |-- __init__.py
|   |-- analyze_func.py 
|   |-- discord_webhook.py
|   |-- ebay_call.py
|   |-- main.py
|   `-- product_class.py
|-- db
|   |-- __init__.py
|   |-- database.py
|   `-- main.py
|-- gui
|   |-- __init__.py
|   |-- main.py
|   |-- templates.py
|   `-- windows.py
|
|-- Ebay Scraper.db
|-- README.md
|-- requirements.txt
|-- run_backend.py
|-- run_db.py
|-- run_scraper_app.py

---

## Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

---

## Author

Hanto_13th - no professional mail yet

---

## License

This project is licensed under the MIT License.
