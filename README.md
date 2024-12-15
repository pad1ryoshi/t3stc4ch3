# t3stc4ch3

`t3stc4ch3.py` is a tool designed to test if URLs are being cached.

## Disclaimer
We're not responsible for the misuse of this tool. Be careful.

## Screenshot
![image](https://github.com/user-attachments/assets/70aec2de-0ffb-43af-adb7-0c620bade422)

## Features
- **Checking cache**: Verify if caching mechanisms are present for a given list of URLs.
- **Exclude Results**: Option to exclude results based on status codes.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/pad1ryoshi/t3stc4ch3.git
   cd t3stc4ch3
   ```

2. Install the required dependencies
      ```sh
   pip install -r requirements.txt
   ```
## Usage

1. Create a file containing the list of URLs (e.g., urls.txt):
   ```
   https://shopify.com
   https://att.com
   ```
   
2. Run the tool:
   - To open the menu help:
     ```
     python t3stc4ch3.py -h
     ```
   - To check cache:
     ```
     python t3stc4ch3.py -u urls.txt
     ```
   - To check cache and save the results to a file:
     ```
     python t3stc4ch3.py -u urls.txt -o resuls.txt
     ```
   - To check cache and exclude certain status code:
     ```
     python t3stc4ch3.py -u urls.txt -sc 404 500
     ```

## Requirements

  - requests
  - argparse
  - colorama
  - urllib3

## License

This project is licensed under the MIT License.
