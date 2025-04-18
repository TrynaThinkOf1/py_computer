import os
import shutil
import pathlib
import aiofiles
from typing import Optional

import ssd_errors

class SSD:
    def __init__(self, device_name: Optional[str], max_storage_size: int = 1000000) -> None:
        """
        Create an SSD Object for storing long-term data in a filesystem.

        :param device_name: The name of THIS SSD device, that will be the base directory for the file system
        :param max_storage_size: How many bytes this SSD will store, default is 1000000 (1MB)
        """
        self.device_name: str = device_name
        self.storage_path: pathlib.Path = os.path.join("./storage", device_name)
        self.max_storage_size: int = max_storage_size
        self.currently_storing_size: int = 0

        if not os.path.exists(self.storage_path):
            os.mkdir(self.storage_path)
        else:
            error_msg: str = f"Cannot create SSD {device_name} because that space is allocated to another SSD.\n\t\t\t\tTry changing the device name"
            raise ssd_errors.DirectoryAlreadyExistsError(error_msg)

    def __str__(self):
        return f"SSD Device {self.device_name} with storage size {self.max_storage_size}, currently {(self.currently_storing_size / self.max_storage_size) * 100}% full"
    def __repr__(self):
        return self.__str__()
    def __bool__(self):
        return self.currently_storing_size < self.max_storage_size

    async def _cleanup(self):
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)

    async def delete(self):
        """
        Permanently delete the SSD filesystem and object
        """
        await self._cleanup()
        del self

    async def create_directory(self, parent_path: str, dir_name: str) -> None:
        """
        Create a directory inside this SSD's filesystem

        :param parent_path: the root-directory where the new directory will be created
        :param dir_name: the name of the new directory
        :return:
        """
        path = os.path.join(self.storage_path, parent_path, dir_name)
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            error_msg = f"Cannot create directory {dir_name} because the path {os.path.join(parent_path, dir_name)} already exists"
            raise ssd_errors.DirectoryAlreadyExistsError(error_msg)

    async def delete_directory(self, dir_path: str) -> None:
        """
        Delete a directory inside this SSD's filesystem

        :param dir_path: where the directory to be deleted is located
        :return:
        """
        path = os.path.join(self.storage_path, dir_path)
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            error_msg = f"Cannot delete directory {dir_path} because the path {dir_path} does not exist"
            raise ssd_errors.DirectoryDoesNotExistError(error_msg)

    async def create_file(self, parent_directory_path: str, file_name: str) -> None:
        """
        Create a file inside this SSD's filesystem

        :param directory_path: where the file will be located
        :param file_name: what the file will be called
        :return:
        """
        path = os.path.join(self.storage_path, parent_directory_path, file_name)
        if not os.path.exists(path):
            async with aiofiles.open(path, "w") as f:
                await f.write("")
        else:
            error_msg = f"Cannot create file {file_name} because the path {os.path.join(parent_directory_path, file_name)} already exists"
            raise ssd_errors.FileAlreadyExistsError(error_msg)

    async def delete_file(self, file_path: str) -> None:
        """
        Delete a file inside this SSD's filesystem

        :param file_path: where the file is located
        :return:
        """
        path = os.path.join(self.storage_path, file_path)
        if os.path.exists(path):
            os.remove(path)
        else:
            error_msg = f"Cannot delete file {file_path.split('/')[-1]} because the path {file_path} does not exist"
            raise ssd_errors.FileNotFoundError(error_msg)

    async def read_file(self, file_path: str, read_binary: bool = False) -> str | bytes:
        """
        Read from a file inside this SSD's filesystem

        :param file_path: where the file is located
        :param read_binary: whether or not to write the contens as binary content
        :return: either the text content or the bytes content
        """
        path = os.path.join(self.storage_path, file_path)
        if not os.path.exists(path):
            error_msg = f"Cannot read file {file_path} because the path {file_path} does not exist"
            raise ssd_errors.File(error_msg)

        if read_binary:
            async with aiofiles.open(path, "rb") as f:
                return await f.read()
        else:
            async with aiofiles.open(path, "r") as f:
                return await f.read()

    async def write_to_file(self, file_path: str, new_content: str | bytes, write_binary: bool = False) -> None:
        """
        Write new content to a file, completely erases old file contents
        **READ & SAVE OLD FILE CONTENTS FIRST**

        :param file_path: where the file is located
        :param new_content: what is the content to be written to the file
        :param write_binary:
        :return:
        """
        path = os.path.join(self.storage_path, file_path)
        if not os.path.exists(path):
            error_msg = f"Cannot write to file {file_path.split('/')[-1]} because the path {file_path} does not exist"
            raise ssd_errors.FileNotFoundError(error_msg)

        if write_binary:
            async with aiofiles.open(path, "wb") as f:
                await f.write(new_content)
        else:
            async with aiofiles.open(path, "w") as f:
                await f.write(new_content)