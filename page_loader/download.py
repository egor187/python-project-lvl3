from bs4 import BeautifulSoup
from progress.spinner import Spinner
import requests
import os.path
import os
from urllib.parse import urlparse, urljoin
from page_loader.naming import get_filename_from_tag, get_filename_for_link
from page_loader.logging import logger


def img_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_img_list = []
    spinner = Spinner('Loading images')
    state = 'go'
    while state != 'FINISHED':
        for link in soup.find_all('img'):
            logger.debug('check for having "src" atribute in tag <img>')
            if link.get('src') and not urlparse(link.get('src')).scheme:

                try:
                    response = requests.get(
                        urljoin(
                            request.url,
                            link.get("src")
                        )
                    )
                    response.raise_for_status()
                except requests.HTTPError as r:
                    print(
                        f' Problem with response recieving from tag: '
                        f'{link.get("src")}. '
                        f'Error message: {r}')

                filename_from_img_link = get_filename_from_tag(
                    request.url,
                    link.get('src')
                )
                new_src_to_img_list.append(filename_from_img_link)
                if os.path.isfile(
                    os.path.join(
                        download_path,
                        filename_from_img_link
                    )
                ):
                    raise FileExistsError(
                        f'File {filename_from_img_link} already exists'
                    )

                with open(
                        os.path.join(
                        download_path,
                        filename_from_img_link
                        ),
                        "wb"
                ) as r:
                    logger.debug(f'downloading image "{link}"')
                    logger.debug(
                        'may occur error if dir for download already exist'
                    )
                    r.write(response.content)
                    spinner.next()
        state = "FINISHED"
    return new_src_to_img_list


def link_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_href_to_link_list = []
    spinner = Spinner('Loading links')
    state = 'go'
    while state != 'FINISHED':
        for link in soup.find_all('link'):
            file_name = get_filename_for_link(link, request)
            if not urlparse(link.get('href')).scheme \
                or urlparse(link.get('href')).scheme \
                and urlparse(link.get('href')).netloc \
                    == urlparse(request.url).netloc:

                try:
                    response = requests.get(
                        urljoin(
                            request.url,
                            link.get("href")
                        )
                    )
                    response.raise_for_status()
                except requests.HTTPError as r:
                    print(
                        f' Problem with response recieving from tag: '
                        f'{link.get("href")}. '
                        f'Error message: {r}')

                new_href_to_link_list.append(file_name)
                if os.path.isfile(os.path.join(download_path, file_name)):
                    raise FileExistsError(f'File {file_name} already exists')

                with open(os.path.join(download_path, file_name), "wb") as r:
                    logger.debug(
                        f'downloading link with href: "{link.get("href")}"'
                    )
                    r.write(response.content)
                    spinner.next()
        state = "FINISHED"
    return new_href_to_link_list


def script_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_script_list = []
    spinner = Spinner('Loading scripts')
    state = 'go'
    while state != 'FINISHED':
        for script in soup.find_all('script'):
            if script.get("src"):
                file_name = get_filename_from_tag(
                    request.url,
                    script.get('src')
                )

                if not urlparse(script.get('src')).scheme \
                    or urlparse(script.get('src')).scheme \
                    and urlparse(script.get('src')).netloc \
                        == urlparse(request.url).netloc:

                    try:
                        response = requests.get(
                            urljoin(
                                request.url,
                                script.get("src")
                            )
                        )
                        response.raise_for_status()
                    except requests.HTTPError as r:
                        print(
                            f' Problem with response recieving from tag: '
                            f'{script.get("src")}. '
                            f'Error message: {r}'
                        )

                    new_src_to_script_list.append(file_name)

                    if os.path.isfile(os.path.join(download_path, file_name)):
                        raise FileExistsError(
                            f'File {file_name} already exists'
                        )

                    with open(
                        os.path.join(
                            download_path,
                            file_name
                        ),
                        "w"
                    ) as r:
                        logger.debug(f'downloading script "{script}"')
                        r.write(response.text)
                        spinner.next()

        state = "FINISHED"
    return new_src_to_script_list
