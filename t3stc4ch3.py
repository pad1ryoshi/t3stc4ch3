import requests
import argparse
import concurrent.futures
from itertools import product
from colorama import Fore, Style, init
import urllib3

# Initialize colorama
init(autoreset=True)

# Suppress only the single InsecureRequestWarning from urllib3 needed to verify=False.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_file(filename):
    """Load lines from a file into a list."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def send_request(url, headers):
    """Send an HTTP request to the URL with the provided headers."""
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        cache_status = response.headers.get('X-Cache') or response.headers.get('CF-Cache-Status')
        return url, headers, cache_status, response.status_code
    except requests.RequestException as e:
        return url, headers, None, str(e)

def check_cache(urls):
    """Function to check if caching is present."""
    for url in urls:
        headers = {}
        result = send_request(url, headers)
        url, headers, cache_status, status_code = result
        if cache_status == 'HIT':
            print(f'{Fore.GREEN}URL: {url}\nCache Status: {cache_status}\nStatus Code: {status_code}\n{Style.RESET_ALL}')
        elif cache_status is None:
            print(f'{Fore.YELLOW}URL: {url}\nCache Status: No caching headers detected\nStatus Code: {status_code}\n{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}URL: {url}\nCache Status: {cache_status}\nStatus Code: {status_code}\n{Style.RESET_ALL}')

def check_headers(urls, headers_list):
    """Function to test headers."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_request = {executor.submit(send_request, url, {header: 'test'}): (url, header) 
                             for url, header in product(urls, headers_list)}
        for future in concurrent.futures.as_completed(future_to_request):
            url, header = future_to_request[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
    
    for url, headers, cache_status, status_code in results:
        if cache_status == 'HIT':
            print(f'{Fore.GREEN}URL: {url}\nHeaders: {headers}\nCache Status: {cache_status}\nStatus Code: {status_code}\n{Style.RESET_ALL}')
        elif cache_status is None:
            print(f'{Fore.YELLOW}URL: {url}\nHeaders: {headers}\nCache Status: No caching headers detected\nStatus Code: {status_code}\n{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}URL: {url}\nHeaders: {headers}\nCache Status: {cache_status}\nStatus Code: {status_code}\n{Style.RESET_ALL}')

def main(url_file, headers_file, function):
    urls = load_file(url_file)
    
    if function == 'check_cache':
        check_cache(urls)
    elif function == 'check_headers':
        if headers_file is None:
            print(f'{Fore.RED}Headers file is required for check_headers function.{Style.RESET_ALL}')
            return
        headers_list = load_file(headers_file)
        check_headers(urls, headers_list)
    else:
        print(f'{Fore.RED}Function {function} not recognized. Use: check_cache or check_headers.{Style.RESET_ALL}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cache Poisoning Detection Tool')
    parser.add_argument('-u', '--url_file', required=True, help='File containing the list of URLs')
    parser.add_argument('-w', '--headers_file', help='File containing the wordlist of headers (only required for check_headers)')
    parser.add_argument('-f', '--function', required=True, help='Function to execute: check_cache or check_headers')
    
    args = parser.parse_args()
    main(args.url_file, args.headers_file, args.function)
