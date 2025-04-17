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
            error_msg: str = f"Cannot create SSD {device_name} because that space is allocated to another SSD.\n\t\t\t\tTry changing the device name."
            raise ssd_errors.DirectoryAlreadyExistsError(error_msg)

    def __str__(self):
        return f"SSD Device {self.device_name} with storage size {self.max_storage_size}, currently {(self.currently_storing_size / self.max_storage_size) * 100}% full"
    def __repr__(self):
        return self.__str__()
    def __bool__(self):
        return self.currently_storing_size < self.max_storage_size

    def _cleanup(self):
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)

    def delete(self):
        """
        Permanently delete the SSD file system and object
        """
        self._cleanup()
        del self

    def change_max_storage_size(self, new_max_storage_size: int) -> None:
        """
        Change the amount of storage this SSD can have

        :param new_max_storage_size: The new storage bytes amount
        :return:
        """
        if new_max_storage_size < self.currently_storing_size:
            error_msg: str = f"Cannot compress storage from {self.max_storage_size} bytes to {new_max_storage_size} bytes on SSD {self.device_name} because it is currently storing {self.currently_storing_size} bytes."
            raise ssd_errors.StorageFullError(message=error_msg)
        else:
            self.max_storage_size = new_max_storage_size

    def create_directory(self, parent_path: str, dir_name: str) -> None:
        """
        Create a directory inside this SSD's filesystem
        :param parent_path:
        :param dir_name:
        :return:
        """