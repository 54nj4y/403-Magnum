# 403 Magnum
--------------------------------------------------------------------------------------------------------------------------------------------

A powerful tool for bypassing 403 Forbidden responses. This tool attempts various techniques to bypass 403 access restrictions including:

- HTTP Method Fuzzing
- Header Manipulation 
- URL Path Variations
- Custom Bypass Techniques
  
This tool supports various fuzzing techniques and outputs detailed HTTP status codes for each request to help you analyze server behavior and response handling.

##Table of Contents
 - [ Installation ](#installation)
 - [Usage](#usage)

## Installation

Clone the repository
```
git clone https://github.com/54nj4y/403-Magnum.git
```
Navigate to the folder
```
cd 403-Magnum
```
Install requirements
```
pip install -r requirements.txt
```

## Usage

```
python3 403-Magnum.py [options]
```

Eg: python 403-Magnum.py -v -u https://website.com/403.log

Options:
  -h, --help         show this help message and exit
  -v, --verbose      Shows all responses
  -u URL, --url=URL  Url of website

![image](https://github.com/user-attachments/assets/eef7f78d-3083-48f5-b4f2-2457c628197d)