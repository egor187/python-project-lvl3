#!usr/bin/env python3

import argparse
import os
import os.path
#from page_loader.page_loader import download
from page_loader import download

def main():
    parser = argparse.ArgumentParser(description="Download HTML-page into file")
    parser.add_argument("web_source", type=str, help="destination of resource to download")
    parser.add_argument("-o", "--output", type=str, help="'path_to_file' - destination to download HTML-page. (Default: 'cwd')", default=os.getcwd())
    parser.parse_args()
    ie_source = parser.parse_args().web_source
    output = parser.parse_args().output


    print(download(ie_source, output))


if __name__ == "__main__":
    main()
