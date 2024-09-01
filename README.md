# KKDAY Crawler

## Overview
The KKDAY Crawler is a project designed to collect price fluctuations of tickets and itineraries offered by KKday in specific cities across different currencies. The collected data is stored in a database for further analysis.

## Features
- Collects data from multiple cities.
- Supports various currencies.
- Configurable proxy settings for web scraping.
- Send Slack notification when the crawler is finished.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/KKDAY_crawler.git
   cd KKDAY_crawler
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the settings in `config/config.yml` as needed.

## Usage
To run the crawler, execute the following command:
```bash
python main.py
```

## Configuration
The configuration file `config/config.yml` allows you to specify:
- **Cities**: List of cities to scrape.
- **Currencies**: List of currencies to consider.
- **Proxy settings**: Options to use a proxy for requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.