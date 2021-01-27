import os.path
import os
import tempfile
import requests
import requests_mock
import pytest
from page_loader import download, link_download


def test_file_html_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.abspath(
            os.path.join(
                tmpdir,
                "ru-hexlet-io-courses.html"
            )
        )
        assert download('https://ru.hexlet.io/courses', tmpdir) == path


def test_correct_link_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = "https://ru.hexlet.io/courses"
        expected_href = [
            'ru-hexlet-io-lessons.rss',
            'ru-hexlet-io-courses.html',
        ]
        real_href = link_download(requests.get(url), tmpdir)

        assert expected_href == real_href


def test_isexceptions_handled(tmp_path):
    with requests_mock.Mocker() as m:
        url = "https://ru.hexlet.io/courses"
        m.get(url, status_code=100)
        with pytest.raises(ConnectionAbortedError):
            download(url, tmp_path)


def test_iscorrect_dir_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = "https://www.test.com/try"
        download(url, tmpdir)
        expect_dir_name = os.path.join(tmpdir, "www-test-com-try_files")
        assert os.path.isdir(expect_dir_name)


def test_iscorrect_img_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = "https://page-loader.hexlet.repl.co"
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

def test_hexlet_check():
    def main():
        return 2 + 3

    assert main() == 4
