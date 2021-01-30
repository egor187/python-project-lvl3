import re
import os.path
from urllib.parse import urlparse
from page_loader.logging import logger


def get_filename_from_tag(url, source):
    url_parsed = urlparse(url)
    logger.debug('parsing url')
    netloc = re.sub(r'[\W+_?]', '-', url_parsed.netloc)
    tag_without_scheme = urlparse(source).path
    # Cutting filename to 60-symbol len
    filename_from_tag = netloc + re.sub(r'[/+?]', '-', tag_without_scheme)[:60]
    logger.debug('creating filename from <tag> for downloading')
    return filename_from_tag


def get_filename_for_downloaded_html(url):
    logger.debug('getting URL for download html')
    url_without_schema = re.search(r'^(https?://)(\S+)', url).group(2)
    last_slash_cutted_url = url_without_schema[:-1] \
        if url_without_schema[-1] == "/"\
        else url_without_schema
    file_name_from_url = re.sub(r'[\W+?]', '-', last_slash_cutted_url)
    logger.debug('creating filename for downloaded html')
    return file_name_from_url


def get_filename_for_link(link, request):
    if not os.path.splitext(link.get('href'))[1]:
        logger.debug(
            'may occur error about ext of file'
            ' in case where "href" attribute is None'
        )
        try:
            file_name = get_filename_from_tag(
                request.url,
                link.get('href')
            ) + '.html'  # TODO refactor
        except FileExistsError:
            print('File already exist. Creating new file with [0]')
            file_name = get_filename_from_tag(
                request.url,
                link.get('href')
            ) + '0' + '.html'
    elif os.path.splitext(link.get('href'))[1]:
        file_name = get_filename_from_tag(
            request.url,
            link.get('href')
        )
    return file_name
