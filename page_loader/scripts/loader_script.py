#!usr/bin/env python3

import argparse
import os
import sys
import os.path
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
        print(download(ie_source, output))

    # except FileNotFoundError as fnfe:
    #     print(fnfe)
    #     sys.exit(1)

    # except PermissionError as pe:
    #     print(pe)
    #     sys.exit(1)

    # except NotADirectoryError as nade:
    #     print(nade)
    #     sys.exit(1)

    # except requests.exceptions.ConnectionError:
    #     print(f'Unable to connect to {ie_source}')
    #     sys.exit(1)

    # except ConnectionAbortedError as cae:
    #     print(cae)
    #     sys.exit(1)

    # except FileExistsError as fee:
    #     print(fee)
    #     sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
