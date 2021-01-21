import os
import os.path
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_filename_from_tag(url, source):
    url_parsed = urlparse(url)
    netloc = re.sub(r'[\W+?]', '-', url_parsed.netloc)
    tag_without_scheme = urlparse(source).path
    filename_from_tag = netloc + re.sub(r'[/+?]', '-', tag_without_scheme)
    return filename_from_tag


def get_filename_from_url(source):
    request = requests.get(source)
    url_without_schema = re.search(r'^(https?://)(\S+)', request.url).group(2)
    last_slash_cutted_url = url_without_schema[:-1] \
        if url_without_schema[-1] == "/"\
        else url_without_schema

    file_name_from_url = re.sub(r'[\W+?]', '-', last_slash_cutted_url)
    return file_name_from_url


def get_content_type(url):
    request = requests.get(url)
    content_type = re.search(
            r'/(\S+);',
            request.headers['Content-Type']
            ).group(1)
    return content_type


def img_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_img_list = []
    for link in soup.find_all('img'):
        if link.get('src') and not urlparse(link.get('src')).scheme:
            response = requests.get(
                request.url + urlparse(
                    link.get('src')
                    ).path
                )
            filename_from_img_link = os.path.join(
                download_path,
                get_filename_from_tag(
                    request.url,
                    link.get('src')
                )
            )
        new_src_to_img_list.append(filename_from_img_link)
        with open(filename_from_img_link, "wb") as r:
            r.write(response.content)
    return new_src_to_img_list


def link_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_href_to_link_list = []
    for link in soup.find_all('link'):

        if urlparse(link.get('href')).scheme:
            response = requests.get(link.get("href"))
        elif not urlparse(link.get("href")).scheme:
            response = requests.get(
                request.url + urlparse(
                    link.get("href")
                    ).path
                )

        if not os.path.splitext(link.get('href'))[1]:
            file_name = get_filename_from_tag(
                request.url,
                link.get('href')
            ) + '.html'  # TODO refactor
        elif os.path.splitext(link.get('href'))[1]:
            file_name = get_filename_from_tag(request.url, link.get('href'))

        filename_from_link_link = os.path.join(
            download_path,
            file_name
        )

        if not urlparse(link.get('href')).scheme \
            or urlparse(link.get('href')).scheme \
            and urlparse(link.get('href')).netloc \
                == urlparse(request.url).netloc:

            new_href_to_link_list.append(filename_from_link_link)

            with open(filename_from_link_link, "wb") as r:
                r.write(response.content)
    return new_href_to_link_list


def script_download():
    pass


def download(url, download_path):
    request = requests.get(url)
    file_name = get_filename_from_url(url)
    path = os.path.join(download_path, file_name)
    path_to_file = path + '.html'
    path_to_dir = path + '_files'
    os.mkdir(path_to_dir)

    new_src_for_img = img_download(request, path_to_dir)
    new_href_for_link = link_download(request, path_to_dir)

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

    with open(path_to_file, "w") as r:
        for index, tag in enumerate(old_src_for_img):
            tag['src'] = new_src_for_img[index]

        for index, tag in enumerate(old_href_for_link):
            tag['href'] = new_href_for_link[index]

        r.write(soup.prettify(formatter="html5"))

    return path_to_file
