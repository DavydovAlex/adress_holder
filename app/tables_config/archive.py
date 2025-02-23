from pathlib import Path
import zipfile
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
        for file_path in self._zipfile.namelist():

    def _get_folder_filelist(self, folder:str | None = None):
        files_list = []
        for file_path in self._zipfile.namelist():
            if folder is None:
                if Path(file_path).parent == Path(''):
                    files_list.append((file_path, file_path,))
            else:
                if Path(file_path).parent == Path(str(folder)):
                    files_list.append((file_path, str(Path(file_path).name),))
        return files_list


    def _get_folder_filelist(self, folder: str | None):
        files_list = []
        for file_path in self._zipfile.namelist():
            if folder is None:
                if Path(file_path).parent == Path(''):
                    files_list.append((file_path, file_path,))
            else:
                if Path(file_path).parent == Path(str(folder)):
                    files_list.append((file_path, str(Path(file_path).name),))
        return files_list



    def __find_file(self, filelist: list[tuple], mask) -> tuple:
        matches = 0
        for path, name in filelist:
            if re.fullmatch(mask, name) is not None:
                matches += 1
                filename = name
                fullpath = path
        if matches == 0:
            raise FileNotFoundError(' Не удалось найти файл по заданной маске "{}"'.
                                    format(mask))
        if matches > 1:
            raise Exception('Найдено больше одного файла по заданной маске "{}"'.
                            format(mask))
        return fullpath, filename


    def get_archive_filelist(self, archive_path, folder=None):
        with zipfile.ZipFile(archive_path, "r") as zf:
            files_list = []
            for file_path in zf.namelist():
                if folder is None:
                    if Path(file_path).parent == Path(''):
                        files_list.append((file_path, file_path,))
                else:
                    if Path(file_path).parent == Path(str(folder)):
                        files_list.append((file_path, str(Path(file_path).name),))
            return files_list
