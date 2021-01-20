import os.path
import os
import tempfile
from page_loader import download, img_download


def test_file_html_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.abspath(
            os.path.join(
                tmpdir,
                "ru-hexlet-io-courses.html"
            )
        )
        assert download('https://ru.hexlet.io/courses', tmpdir) == path


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
        expect_dir_name = os.path.join(tmpdir, "page-loader-hexlet-repl-co_files")
        expect_img_file_name = os.path.join(tmpdir, expect_dir_name,  "page-loader-hexlet-repl-co-assets-professions-nodejs.png")
        assert os.path.isfile(expect_img_file_name)

