import pytest
import json
import os
from pathlib import Path
from typing import List

from delivery.archiver.archiver import Archive, ArchiveE

@pytest.fixture()
def generate_files(tmpdir):
    file_list = ["first/test11", "first/test12", 
                "second/test21", "second/test22",
                "first/first_lvl2/test111"]
    base_dir = Path(tmpdir).joinpath(Path("base"))           
    file_list = [base_dir.joinpath(Path(_file)) for _file in file_list]
    for file in file_list:
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w") as file_pointer:
            file_pointer.write(str(os.urandom(1024)))
    yield base_dir


class Test_archive:
    def test_add_folder(self, generate_files, tmpdir):
        archive_path = Path(tmpdir).joinpath(Path("test.zip"))
        archive = Archive(file_name=archive_path)
        dir_path = generate_files
        archive.compress(dir_path=dir_path)
        assert archive_path.exists()

    def test_add_folder_raises_no_dir(self, generate_files, tmpdir):
        archive_path = Path(tmpdir).joinpath(Path("example.zip"))
        faulty_dir_path = Path(tmpdir).joinpath(Path("not_an_existing_directory"))
        archive = Archive(file_name=archive_path)
        with pytest.raises(ArchiveE):
            archive.compress(dir_path=faulty_dir_path)
