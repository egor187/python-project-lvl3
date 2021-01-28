import os
import os.path


def exc(request, download_path, path_to_dir):
    if not os.path.exists(download_path):
        raise FileNotFoundError(f'Directory {download_path} is not exist')
    if not os.access(download_path, os.W_OK):
        raise PermissionError(f'Directory {download_path} is unable to write')
    if not os.path.isdir(download_path):
        raise NotADirectoryError(
            f'Path to download {download_path} is not a directory'
        )
    if request.status_code != 200:
        raise ConnectionAbortedError(
            f"Status-code of server-response "
            f"from '{request.url}' is '{request.status_code}'"
        )
    if os.path.isdir(path_to_dir):
        raise FileExistsError(f'Directory "{path_to_dir}" is not empty')
