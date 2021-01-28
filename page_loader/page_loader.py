import os
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.logging import logger
from page_loader.exceptions import exc
from page_loader.download import img_download, link_download, script_download
from page_loader.naming import get_filename_for_downloaded_html


def download(url, download_path):
    request = requests.get(url)
    file_name = get_filename_for_downloaded_html(url)
    path = os.path.join(download_path, file_name)
    path_to_file = path + '.html'
    path_to_dir = path + '_files'
    local_source_path = file_name + '_files'

    exc(request, download_path, path_to_dir)

    os.mkdir(path_to_dir)

#    new_src_for_img = img_download(request, path_to_dir)[1]
#    logger.info('\nimages downloaded')

    new_href_for_link = link_download(request, path_to_dir)
    logger.info('\nlinks downloaded')

    new_src_for_script = script_download(request, path_to_dir)
    logger.info('\nscripts downloaded')

    soup = BeautifulSoup(request.text, "html.parser")

    old_src_for_img, new_src_for_img = img_download(request, path_to_dir)
    logger.info('\nimages downloaded')

#    old_src_for_img = []
#    for tag in soup.find_all("img"):
#        if tag.get("src") and not urlparse(tag.get('src')).scheme:
#            old_src_for_img.append(tag)

    old_href_for_link = []
    for tag in soup.find_all('link'):
        if not urlparse(tag.get('href')).scheme \
            or urlparse(tag.get('href')).scheme \
            and urlparse(tag.get('href')).netloc \
                == urlparse(request.url).netloc:
            old_href_for_link.append(tag)

    old_src_for_script = [
        script for script in soup.find_all("script")
        if script.get("src") and urlparse(
            script.get("src")
        ).netloc == urlparse(
            request.url
        ).netloc or script.get("src") and not urlparse(
            script.get("src")
        ).scheme
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
