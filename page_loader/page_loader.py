import os
import os.path
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from progress.spinner import Spinner
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler(filename='./logging_debug.log', mode='w')
debug_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

debug_formatter = logging.Formatter(
    '%(asctime)s -%(name)s - %(levelname)s - %(message)s'
)
stream_formatter = logging.Formatter('%(message)s')

debug_handler.setFormatter(debug_formatter)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(debug_handler)
logger.addHandler(stream_handler)


def get_filename_from_tag(url, source):
    url_parsed = urlparse(url)
    logger.debug('parsing url')
    netloc = re.sub(r'[\W+_?]', '-', url_parsed.netloc)
    tag_without_scheme = urlparse(source).path
    filename_from_tag = netloc + re.sub(r'[/+?]', '-', tag_without_scheme)
    logger.debug('creating filename from <tag> for downloading')
    return filename_from_tag


def get_filename_from_url(url):
    logger.debug('getting URL for download html')
    url_without_schema = re.search(r'^(https?://)(\S+)', url).group(2)
    last_slash_cutted_url = url_without_schema[:-1] \
        if url_without_schema[-1] == "/"\
        else url_without_schema
    file_name_from_url = re.sub(r'[\W+?]', '-', last_slash_cutted_url)
    logger.debug('creating filename for downloaded html')
    return file_name_from_url


def img_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_img_list = []
    spinner = Spinner('Loading images')
    state = 'go'
    while state != 'FINISHED':
        for link in soup.find_all('img'):
            logger.debug('check for having "src" atribute in tag <img>')
            if link.get('src') and not urlparse(link.get('src')).scheme:

                response = requests.get(
                    urljoin(
                    request.url,
                    link.get('src')
                    )
                )

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

            if not urlparse(link.get('href')).scheme \
                or urlparse(link.get('href')).scheme \
                and urlparse(link.get('href')).netloc \
                    == urlparse(request.url).netloc:

                response = requests.get(
                    urljoin(
                        request.url,
                        link.get("href")
                    )
                )

            if not os.path.splitext(link.get('href'))[1]:
                logger.debug(
                    'may occur error about ext of file'
                    'in case where "href" attribute is None'
                )
                file_name = get_filename_from_tag(
                    request.url,
                    link.get('href')
                ) + '.html'  # TODO refactor
            elif os.path.splitext(link.get('href'))[1]:
                file_name = get_filename_from_tag(
                    request.url,
                    link.get('href')
                )

            if not urlparse(link.get('href')).scheme \
                or urlparse(link.get('href')).scheme \
                and urlparse(link.get('href')).netloc \
                    == urlparse(request.url).netloc:

                new_href_to_link_list.append(file_name)

                if os.path.isfile(os.path.join(download_path, file_name)):
                    raise FileExistsError(f'File {file_name} already exists')

                with open(os.path.join(download_path, file_name), "wb") as r:
                    logger.debug(f'downloading link "{link}"')
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

                if not urlparse(script.get('src')).scheme \
                    or urlparse(script.get('src')).scheme \
                    and urlparse(script.get('src')).netloc \
                        == urlparse(request.url).netloc:

                    response = requests.get(
                        urljoin(
                            request.url,
                            script.get("src")
                        )
                    )

                file_name = get_filename_from_tag(
                    request.url,
                    script.get('src')
                )

                if not urlparse(script.get('src')).scheme \
                    or urlparse(script.get('src')).scheme \
                    and urlparse(script.get('src')).netloc \
                    == urlparse(request.url).netloc:

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


def download(url, download_path):
    if not os.path.exists(download_path):
        raise FileNotFoundError(f'Directory {download_path} is not exist')
    if not os.access(download_path, os.W_OK):
        raise PermissionError(f'Directory {download_path} is unable to write')
    if not os.path.isdir(download_path):
        raise NotADirectoryError(
            f'Path to download {download_path} is not a directory'
        )

    request = requests.get(url)

    if request.status_code != 200:
        raise ConnectionAbortedError(
            f"Status-code of server-response "
            f"from '{request.url}' is '{request.status_code}'"
        )

    file_name = get_filename_from_url(url)
    path = os.path.join(download_path, file_name)
    path_to_file = path + '.html'
    path_to_dir = path + '_files'
    local_source_path = file_name + '_files'

    if os.path.isdir(path_to_dir):
        raise FileExistsError(f'Directory "{path_to_dir}" is not empty')

    os.mkdir(path_to_dir)

    new_src_for_img = img_download(request, path_to_dir)
    logger.info('\nimages downloaded')
    new_href_for_link = link_download(request, path_to_dir)
    logger.info('\nlinks downloaded')
    new_src_for_script = script_download(request, path_to_dir)
    logger.info('\nscripts downloaded')

    soup = BeautifulSoup(request.text, "html.parser")

    old_src_for_img = []
    for tag in soup.find_all("img"):
        if tag.get("src") and not urlparse(tag.get('src')).scheme:
            old_src_for_img.append(tag)

    old_href_for_link = []
    for tag in soup.find_all('link'):
        if not urlparse(tag.get('href')).scheme \
            or urlparse(tag.get('href')).scheme \
            and urlparse(tag.get('href')).netloc \
                == urlparse(request.url).netloc:
            old_href_for_link.append(tag)

    old_src_for_script = [
        script for script in soup.find_all("script")
        if script.get("src")
        and urlparse(script.get("src")).netloc == urlparse(request.url).netloc
        or script.get("src") and not urlparse(script.get("src")).scheme
    ]

    with open(path_to_file, "w") as r:
        logger.info('Downloading html')
        for index, tag in enumerate(old_src_for_img):
            tag['src'] = os.path.join(
                local_source_path,
                new_src_for_img[index]
            )
            logger.debug('substitution source for img to downloaded')

        for index, tag in enumerate(old_href_for_link):
            logger.debug('substitution source for link to downloaded')
            tag['href'] = os.path.join(
                local_source_path,
                new_href_for_link[index]
            )

        for index, tag in enumerate(old_src_for_script):
            logger.debug('substitution source for script to downloaded')
            tag['src'] = os.path.join(
                local_source_path,
                new_src_for_script[index]
            )

        r.write(soup.prettify(formatter="html5"))

    return path_to_file
