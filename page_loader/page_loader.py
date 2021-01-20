import os
import os.path
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_filename_from_tag(url, source):
    url_parsed = urlparse(url)
    netloc = re.sub(r'[\W+?]', '-', url_parsed.netloc)
    # source = source[1:] if source[0] == "/" else source
    # Wrong realization: last 'dot' changes too for '-'. Refactor re-pattern
    # filename_from_tag = re.sub(r'[\W+?]', '-', source)
    filename_from_tag = netloc + re.sub(r'[/+?]', '-', source)
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


#def img_download(url, download_path):
#    request = requests.get(url)
#    soup = BeautifulSoup(request.text, 'html.parser')
#    new_src_to_img_list = []
#    for link in soup.find_all('img'):
#        response = requests.get(request.url + str(link.get('src')))
#        filename_from_img_link = os.path.join(
#            download_path,
#            get_filename_from_tag(
#                url,
#                link.get('src')
#             )
#        )
#        new_src_to_img_list.append(filename_from_img_link)
#        new_src_to_img_list.append(filename_from_img_link)
#        with open(filename_from_img_link, "wb") as r:
#            r.write(response.content)
#    return new_src_to_img_list


# Refactor to download img only from tags WITH 'src' and WITHOUT SCHEME
def img_download(request, download_path):
    soup = BeautifulSoup(request.text, 'html.parser')
    new_src_to_img_list = []
    for link in soup.find_all('img'):
        if link.get('src') and not urlparse(link.get('src')).scheme:
            response = requests.get(request.url + str(link.get('src')))
            filename_from_img_link = os.path.join(
                download_path,
                get_filename_from_tag(
                    request.url,
                    link.get('src')
                )
            )
        new_src_to_img_list.append(filename_from_img_link)
        new_src_to_img_list.append(filename_from_img_link)
        with open(filename_from_img_link, "wb") as r:
            r.write(response.content)
    return new_src_to_img_list


def download(url, download_path):
    request = requests.get(url)
    file_name = get_filename_from_url(url)
    path = os.path.join(download_path, file_name)
    path_to_file = path + '.html'
    path_to_dir = path + '_files'
    os.mkdir(path_to_dir)

    #new_src_for_img = img_download(url, path_to_dir)
    new_src_for_img = img_download(request, path_to_dir)

    with open(path_to_file, "w") as r:
        soup = BeautifulSoup(request.text, "html.parser")
        #!!!
        for index, tag in enumerate(soup.find_all('img')):
            tag['src'] = new_src_for_img[index]
        r.write(soup.prettify(formatter="html5"))

    return path_to_file
