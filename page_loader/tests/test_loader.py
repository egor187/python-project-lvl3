import os.path
import os
import tempfile
# import requests
# import requests_mock
# from bs4 import BeautifulSoup
from page_loader import download


def test_file_html_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.abspath(
            os.path.join(
                tmpdir,
                "ru-hexlet-io-courses.html"
            )
        )
        assert download('https://ru.hexlet.io/courses', tmpdir) == path


# def test_correct_link_list(tmp_path):
#    url = "https://ru.hexlet.io/courses"
#    expected_href = [
#            tmp_path / 'ru-hexlet-io-lessons.rss',
#            tmp_path / 'ru-hexlet-io-courses.html'
#            ]
#
#    download(url, tmp_path)
#
#    example = open(tmp_path / "ru-hexlet-io-courses.html", "r").read()
#
#    real_list = []
#    soup = BeautifulSoup(example, "html.parser")
#    for tag in soup.find_all("link"):
#        real_list.append(tag.get("href"))
#
#    assert expected_href == real_list

# def test_file_html_content(tmp_path):
#    url = "https://page-loader.hexlet.repl.co"
#    request = requests.get(url)
#    soup = BeautifulSoup(request.text, "html.parser")
#
#    download(url, tmp_path)
#
#    expected_file_name = tmp_path / "page-loader-hexlet-repl-co.html"
#    real = soup.prettify(formatter = "html5")
#
#    assert open(expected_file_name, "r").read() == real


def test_iscorrect_dir_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = "https://www.test.com/try"
        download(url, tmpdir)
        expect_dir_name = os.path.join(tmpdir, "www-test-com-try_files")
        assert os.path.isdir(expect_dir_name)


def test_iscorrect_img_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = "https://page-loader.hexlet.repl.co/"
        download(url, tmpdir)
        expect_dir_name = os.path.join(
            tmpdir,
            "page-loader-hexlet-repl-co_files"
        )
        expect_img_file_name = os.path.join(
            tmpdir,
            expect_dir_name,
            "page-loader-hexlet-repl-co-assets-professions-nodejs.png"
        )
        assert os.path.isfile(expect_img_file_name)


# def test_iscorrect_img_content(tmp_path):
#    url = "https://ru.hexlet.io/courses"
#    expected_file_name = tmp_path / "test_content.rss"
#    real_file_name = tmp_path / "ru-hexlet-io-lessons.rss"
#
#    with open(expected_file_name, "wb") as w:
#        w.write(requests.get(url).content)
#
#    excpect = open(expected_file_name, "rb").read()
#
#
#    with requests_mock.Mocker() as m:
#        m.get(url, content = excpect)
#        request = requests.get(url)
#
#        link_download(request, tmp_path)
#
#    real = open(real_file_name, "rb").read()
#
#    assert real == excpect
