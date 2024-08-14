
# Mir4 Magic Stone Bot

This bot is designed to retrieve and display Magic Stones from NFTs in the MMORPG game **Mir4**. By providing a link to an NFT on the **XDraco** platform, the bot fetches detailed information about the Magic Stones associated with that NFT. The bot processes the data and generates a downloadable CSV file containing the relevant details, such as item names and option values. The CSV is formatted using commas as decimal separators for percentages and semicolons as column separators to ensure compatibility with various spreadsheet software.

### Features:
- **Magic Stone Filtering:** Extracts Magic Stones with specific names from the NFT inventory, focusing on `[L] Magic Stone` and `[E] Magic Stone`.
- **API Integration:** Connects to Mir4’s API to retrieve detailed item data, including item options and values.
- **CSV Generation:** Creates a downloadable CSV file with all the extracted Magic Stone data, ready for analysis in Excel, Google Sheets, or other spreadsheet tools.
- **Queue Management:** Handles multiple user requests with a queue system, ensuring that each request is processed in turn without overloading the API.

### How It Works:
1. **User Input:** The bot listens for a URL link to a specific NFT on the XDraco platform.
2. **Data Retrieval:** The bot fetches the NFT's summary and inventory data from Mir4’s API.
3. **Magic Stone Processing:** It filters the inventory to find relevant Magic Stones and retrieves detailed stats for each one.
4. **CSV Creation:** The bot formats the data and generates a CSV file with proper formatting, including commas for decimal percentages and semicolons as column delimiters.
5. **Response:** The bot sends the CSV file as a response to the user in the Discord channel.

### Requirements:
- Python 3.8+
- Discord.py
- Requests

### Usage:
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/naustagic/MiR4_NFT_Stones.git
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the Bot:**
   - Set your bot token and channel ID in the script.
4. **Run the Bot:**
   ```bash
   python bot.py
   ```

This bot is an efficient tool for players and collectors who want to quickly access and organize Magic Stone data for their NFTs in Mir4.
