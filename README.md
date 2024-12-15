# t3stc4ch3

`t3stc4ch3.py` is a tool designed to test if URLs are being cached and perform brute force on possible unkeyed headers.

## Disclaimer
We're not responsible for the misuse of this tool. Be careful.

## Screenshot
![image](https://github.com/user-attachments/assets/e91c3a17-1e71-4de2-a986-47c3615c9f0d)



## Features
- **check_cache**: Verify if caching mechanisms are present for a given list of URLs.
- **check_headers**: Test a variety of HTTP headers to identify their impact on caching behavior and detect potential unkeyed headers.

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

2. For checking headers, create a file containing the list of headers (e.g., headers.txt):
    ```
    x-forwarded-scheme
    x-forwarded-host
    x-forwarded-proto
    x-http-method-override
    x-amz-website-redirect-location
    authorization
    x-rewrite-url
    x-host
    user-agent
    handle
    x-original-url
    x-original-host
    x-forwarded-prefix
    x-amz-server-side-encryption
    trailer
    fastly-ssl
    fastly-host
    fastly-ff
    fastly-client-ip
    content-type
    api-version
    acunetix-header
    accept-version
    ```
3. Run the tool:
  - To check cache:
     ```
     python t3stc4ch3.py -u urls.txt -f check_cache
     ```
  - To check headers:
    ```
    python t3stc4ch3.py -u urls.txt -w headers.txt -f check_headers
    ```

## Requirements

  - requests
  - argparse
  - colorama

## License

This project is licensed under the MIT License.
