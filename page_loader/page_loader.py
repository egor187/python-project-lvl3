import os
import os.path
import re
import requests


def get_filename_from_url(source):
    request = requests.get(source)
    url_without_schema = re.search(r'[^https?://]\S+', request.url).group(0)
    last_slash_cutted_url = url_without_schema[:-1] \
            if url_without_schema[-1] == "/"\
            else url_without_schema
    
    file_name_from_url = re.sub(r'[\W+?]', '-', last_slash_cutted_url)
    return file_name_from_url


def get_content_type(url):
    request = requests.get(url)
    content_type = re.search(r'/(\S+);', request.headers['Content-Type']).group(1)
    return content_type


def download(url, download_path):
    request = requests.get(url)
    file_name = get_filename_from_url(url)

    #file_name_from_ie_resource = re.search(r'[^https?://]\S+', request.url).group(0)
    #if file_name_from_ie_resource[-1] == "/":
    #    file_name_from_ie_resource = file_name_from_ie_resource[:-1]
    #file_name_from_ie_resource = re.sub(r'[\W+?]', '-', file_name_from_ie_resource)
    #mod_file_name = file_name_from_ie_resource.replace('.', '-')
    #mod_file_name = mod_file_name.replace('/', '-')
    
    content_type = get_content_type(url)
    path = os.path.join(download_path, file_name) + '.' + content_type

    with open(path, "w") as r:
        r.write(request.text)
    return path
