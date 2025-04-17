import os
import aiofiles
from typing import Optional

import ssd_errors

class SSD:
    def __init__(self, device_name: Optional[str], storage_size: int = 1000000) -> None:
        """
        Create an SSD Object for storing long-term data in a filesystem.

        :param device_name: The name of THIS SSD device, that will be the base directory for the file system
        :param storage_size: How many bytes this SSD will store, default is 1000000 (1MB)
        """
        self.device_name = device_name
        self.storage: os.path = os.path.join("./storage", storage_dir_name)
        self.storage_size: int = storage_size
        self.currently_storing_size: int = 0

    def change_storage_size(self, new_storage_size: int) -> None:
        """
        Change the amount of storage this SSD can have

        :param new_storage_size: The new storage bytes amount
        :return:
        """
        if new_storage_size < self.currently_storing_size:
            raise ssd_errors.StorageFullError(device_name=self.device_name, storage_size=self.currently_storing_size)