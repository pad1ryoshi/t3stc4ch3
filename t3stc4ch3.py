import requests
import argparse
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

def send_request(url):
    """Send an HTTP request to the URL."""
    try:
        response = requests.get(url, timeout=10, verify=False)
        cache_status = response.headers.get('X-Cache') or response.headers.get('CF-Cache-Status')
        return url, cache_status, response.status_code
    except requests.RequestException as e:
        return url, None, str(e)

def get_color_for_status_code(status_code):
    """Return the appropriate color for the given status code."""
    if 100 <= status_code < 200:
        return Fore.BLUE
    elif 200 <= status_code < 300:
        return Fore.GREEN
    elif 300 <= status_code < 400:
        return Fore.YELLOW
    elif 400 <= status_code < 500:
        return Fore.RED
    elif 500 <= status_code < 600:
        return Fore.MAGENTA
    else:
        return Fore.WHITE

def colorize_cache_status(cache_status):
    """Return the cache status with proper colors for each part."""
    if not cache_status:
        return f"{Fore.BLUE}UNKNOWN{Style.RESET_ALL}"
    
    statuses = cache_status.split(",")  
    colored_statuses = []
    for status in statuses:
        status = status.strip().upper()
        if "HIT" in status:
            colored_statuses.append(f"{Fore.GREEN}{status}{Style.RESET_ALL}")
        elif "MISS" in status:
            colored_statuses.append(f"{Fore.RED}{status}{Style.RESET_ALL}")
        elif "DYNAMIC" in status:
            colored_statuses.append(f"{Fore.YELLOW}{status}{Style.RESET_ALL}")
        else:
            colored_statuses.append(f"{Fore.CYAN}{status}{Style.RESET_ALL}")
    return ", ".join(colored_statuses)

def check_cache(urls, output_file=None, exclude_status=None):
    """Function to check if caching is present."""
    results = []
    for url in urls:
        result = send_request(url)
        url, cache_status, status_code = result
        
        if exclude_status and status_code in exclude_status:
            continue
        
        results.append((url, cache_status, status_code))
        
        color_status_code = get_color_for_status_code(status_code)
        colored_cache_status = colorize_cache_status(cache_status)

        print(
            f"{Fore.WHITE}URL: {url}{Style.RESET_ALL}\n"
            f"Cache Status: {colored_cache_status}\n"
            f"{color_status_code}Status Code: {status_code}{Style.RESET_ALL}"
        )
    
    if output_file:
        save_results(results, output_file)

def save_results(results, filename):
    """Save results to a file."""
    with open(filename, 'w') as f:
        for url, cache_status, status_code in results:
            f.write(f'URL: {url}\nCache Status: {cache_status}\nStatus Code: {status_code}\n\n')

def main(url_file, output_file=None, status_code=None):
    urls = load_file(url_file)
    check_cache(urls, output_file, status_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cache Detection Tool')
    parser.add_argument('-u', '--url_file', required=True, help='File containing the list of URLs')
    parser.add_argument('-o', '--output_file', help='Output file to save the results')
    parser.add_argument('-sc', '--status_code', type=int, nargs='*', help='Status codes to exclude from the results')
    
    args = parser.parse_args()
    main(args.url_file, args.output_file, args.status_code)
