from pathlib import Path
import zipfile
import re
class Archive:

    def __init__(self, path: Path | str):
        self._path = path
        self._zipfile = zipfile.ZipFile(path, "r")

        for file_path in self._zipfile.namelist():
            print(file_path)
            print(Path(file_path).parent)
    @property
    def path(self):
        return self._path


    def get_file(self, pattern: str, folder:str | None):
        files_paths = self._get_folder_filelist(folder)
        if len(files_paths) == 0:
            raise Exception(f'Folder dont have any file')
        matches = 0
        for file_path in files_paths:
            if re.fullmatch(pattern, Path(file_path).name) is not None:
                matches += 1
                fullpath = file_path
        if matches == 0:
            raise FileNotFoundError(f'Cant find file using pattern "{pattern}"')
        if matches > 1:
            raise Exception(f'Found more than one file using pattern "{pattern}"')
        return self._zipfile.open(fullpath)


    def _get_folder_filelist(self, folder:str | None = None):
        folder_path = Path('') if folder is None else Path(folder)
        files_list = []
        for file_path in self._zipfile.namelist():
            if Path(file_path).parent == folder_path:
                files_list.append(file_path)
        return files_list
