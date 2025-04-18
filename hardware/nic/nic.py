import requests
from typing import Optional

class NIC:
    def __init__(self, device_name: str):
        """
        Create a new NIC object

        :param device_name:
        """
        self.device_name = device_name

    def __repr__(self):
        return f"NIC: {self.device_name}"

    def send_get_request(self, url: str, headers: Optional[dict] = None) -> requests.Response:
        """
        Send a GET request to the specified URL with the specified headers

        :param url:
        :param headers:
        :return:
        """
        response = requests.get(url, headers=headers)
        return response

    def send_post_request(self, url: str, headers: Optional[dict] = None, json_body: Optional[dict] = None, data: Optional[dict] = None, files: Optional[dict] = None) -> requests.Response:
        """
        Send a POST request to the specified URL with the specified headers and a JSON body and/or form data and/or files

        :param url:
        :param headers:
        :param json_body:
        :return:
        """
        response = requests.post(url, headers=headers, json=json_body, data=data, files=files)
        return response

    def send_put_request(self, url: str, headers: Optional[dict] = None, json_body: Optional[dict] = None, data: Optional[dict] = None, files: Optional[dict] = None) -> requests.Response:
        """
        Send a PUT request to the specified URL with the specified headers and a JSON body and/or form data and/or files

        :param url:
        :param headers:
        :param json_body:
        :return:
        """
        response = requests.put(url, headers=headers, json=json_body, data=data, files=files)
        return response

    def send_patch_request(self, url: str, headers: Optional[dict] = None, json_body: Optional[dict] = None, data: Optional[dict] = None, files: Optional[dict] = None) -> requests.Response:
        """
        Send a PUT request to the specified URL with the specified headers and a JSON body and/or form data and/or files

        :param url:
        :param headers:
        :param json_body:
        :return:
        """
        response = requests.patch(url, headers=headers, json=json_body, data=data, files=files)
        return response

    def send_delete_request(self, url: str, headers: Optional[dict] = None, json_body: Optional[dict] = None) -> requests.Response:
        """
        Send a DELETE request to the specified URL with the specified headers

        :param url:
        :param headers:
        :return:
        """
        response = requests.delete(url, headers=headers, json=json_body)
        return response

    def send_head_request(self, url: str, headers: Optional[dict] = None) -> requests.Response:
        """
        Send a HEAD request to the specified URL with the specified headers

        :param url:
        :param headers:
        :return:
        """
        response = requests.head(url, headers=headers)
        return response

    def send_options_request(self, url: str, headers: Optional[dict] = None) -> requests.Response:
        """
        Send an OPTIONS request to the specified URL with the specified headers

        :param url:
        :param headers:
        :return:
        """
        response = requests.options(url, headers=headers)
        return response