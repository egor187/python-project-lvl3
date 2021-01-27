#!usr/bin/env python3

import argparse
import os
import sys
import os.path
import requests
import logging
from page_loader import download

logger = logging.getLogger()
handler = logging.FileHandler(filename='./logging_debug.log')
logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(
        description="Download HTML-page into file"
        )
    parser.add_argument(
        "web_source",
        type=str, help="destination of resource to download"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="'path_to_file' - destination to download HTML-page."
        "(Default: 'cwd')",
        default=os.getcwd()
    )
    parser.parse_args()
    ie_source = parser.parse_args().web_source
    output = parser.parse_args().output
    
    try:
        download(ie_source, output)

    except TypeError as tr:
        print(tr)

    except ConnectionAbortedError as conn_exc:
        logger.exception(msg='exception about status_code')
        print(conn_exc)

    except requests.exceptions.ConnectionError as exc:
        print(
            f"Some serious problems with connection occur. Error is: {exc}. "
            f"Check out your connection"
        )
    except OSError as e:
        print(e)

    #except OSError as os_error:
    #    if os_error.errno == 2:
    #        print(
    #            f"There is no such file or directory. "
    #            f"Error is: {os_error}"
    #        )
    #    elif os_error.errno == 20:
    #        print(
    #            f"Path to download isn't correct. "
    #            f"It's not a directory. Error is: {os_error}."
    #        )
    #    elif os_error.errno == 17:
    #        print(
    #            f"Same file already exist. "
    #            f"Try another file_name. Error is: {os_error}."
    #        )

    #except Exception as x:
    #    print(f'Some serious problem occur with name: {x}')

    #else:
    #    sys.exit(0)

if __name__ == "__main__":
    main()
