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


def get_filename_from_url(source):
    request = requests.get(source)
    logger.debug('getting URL for download html')
    url_without_schema = re.search(r'^(https?://)(\S+)', request.url).group(2)
    last_slash_cutted_url = url_without_schema[:-1] \
        if url_without_schema[-1] == "/"\
        else url_without_schema

    file_name_from_url = re.sub(r'[\W+?]', '-', last_slash_cutted_url)
    logger.debug('creating filename for downloaded html')
    return file_name_from_url


def get_content_type(url):
    request = requests.get(url)
    content_type = re.search(
            r'/(\S+);',
            request.headers['Content-Type']
            ).group(1)
    logger.debug('check content-type from server response')
    return content_type


def img_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_img_list = []
    spinner = Spinner('Loading images')
    state = 'go'
    while state != 'FINISHED':
        for link in soup.find_all('img'):
            logger.debug('check for having "src" atribute in tag <img>')
            if link.get('src') and not urlparse(link.get('src')).scheme:
                # response = requests.get(
                #    request.url + urlparse(
                #        link.get('src')
                #        ).path
                #    )
                response = requests.get(urljoin(
                    request.url, urlparse(
                        link.get('src')
                        ).path
                    ))
                filename_from_img_link = os.path.join(
                    download_path,
                    get_filename_from_tag(
                        request.url,
                        link.get('src')
                    )
                )

                new_src_to_img_list.append(filename_from_img_link)
                with open(filename_from_img_link, "wb") as r:
                    logger.debug(f'downloading image "{link}"')
                    logger.debug(
                        'may occur error if dir for download already exist'
                    )
                    r.write(response.content)
                    spinner.next()
        state = "FINISHED"
    return new_src_to_img_list


def link_download(url, download_path):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    new_href_to_link_list = []
    spinner = Spinner('Loading links')
    state = 'go'
    while state != 'FINISHED':
        for link in soup.find_all('link'):

            if urlparse(link.get('href')).scheme:
                response = requests.get(link.get("href"))
            elif not urlparse(link.get("href")).scheme:
                # response = requests.get(
                #    request.url + urlparse(
                #        link.get("href")
                #        ).path
                #    )

                response = requests.get(urljoin(
                    url, urlparse(
                        link.get("href")
                        ).path
                    ))
            if not os.path.splitext(link.get('href'))[1]:
                logger.debug(
                    'may occur error about ext of file'
                    'in case where "href" attribute is None'
                )
                file_name = get_filename_from_tag(
                    url,
                    link.get('href')
                ) + '.html'  # TODO refactor
            elif os.path.splitext(link.get('href'))[1]:
                file_name = get_filename_from_tag(
                    url,
                    link.get('href')
                )

            filename_from_link_link = os.path.join(
                download_path,
                file_name
            )

            if not urlparse(link.get('href')).scheme \
                or urlparse(link.get('href')).scheme \
                and urlparse(link.get('href')).netloc \
                    == urlparse(url).netloc:

                new_href_to_link_list.append(filename_from_link_link)

                with open(filename_from_link_link, "wb") as r:
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

                if urlparse(script.get('src')).scheme:
                    response = requests.get(script.get("src"))
                elif not urlparse(script.get("src")).scheme:
                    # response = requests.get(
                    #    request.url + urlparse(
                    #        script.get("src")
                    #        ).path
                    #    )

                    response = requests.get(urljoin(
                        request.url, urlparse(
                            script.get("src")
                            ).path
                        ))
                file_name = get_filename_from_tag(
                    request.url,
                    script.get('src')
                )

                filename_from_script_link = os.path.join(
                    download_path,
                    file_name
                )

                if not urlparse(script.get('src')).scheme \
                    or urlparse(script.get('src')).scheme \
                    and urlparse(script.get('src')).netloc \
                        == urlparse(request.url).netloc:

                    new_src_to_script_list.append(filename_from_script_link)

                    with open(filename_from_script_link, "w") as r:
                        logger.debug(f'downloading script "{script}"')
                        r.write(response.text)
                        spinner.next()
        state = "FINISHED"
    return new_src_to_script_list


def download(url, download_path):
    request = requests.get(url)

    if not request:
        raise TypeError(f"Not valid url for '{request.url}'")
    if request.status_code != 200:
        raise ConnectionAbortedError(
            f"Status-code of server-response "
            f"from '{request.url}' is '{request.status_code}'"
        )

    file_name = get_filename_from_url(url)
    path = os.path.join(download_path, file_name)
    path_to_file = path + '.html'
    path_to_dir = path + '_files'
    os.mkdir(path_to_dir)

    new_src_for_img = img_download(request, path_to_dir)
    logger.info('\nimages downloaded')
    new_href_for_link = link_download(url, path_to_dir)
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
            tag['src'] = new_src_for_img[index]
            logger.debug('substitution source for img to downloaded')

        for index, tag in enumerate(old_href_for_link):
            logger.debug('substitution source for link to downloaded')
            tag['href'] = new_href_for_link[index]

        for index, tag in enumerate(old_src_for_script):
            logger.debug('substitution source for script to downloaded')
            tag['src'] = new_src_for_script[index]

        r.write(soup.prettify(formatter="html5"))

    return path_to_file
