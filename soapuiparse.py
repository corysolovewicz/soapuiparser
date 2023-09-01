import os
import xml.etree.ElementTree as ET
import requests

def extract_requests_from_soapui_project(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    requests_list = []
    for request_tag in root.findall('.//request'):
        # Extracting method. Default to GET if attribute doesn't exist
        method = request_tag.attrib.get('method', 'GET').upper()

        # Extracting the request URL or payload
        request_data = request_tag.text

        requests_list.append((method, request_data))

    return requests_list

def send_requests_to_proxy(requests_list):
    proxy = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    for method, req in requests_list:
        try:
            if method == 'POST':
                response = requests.post(req, proxies=proxy)
            elif method == 'GET':
                response = requests.get(req, proxies=proxy)
            # Add more elif checks for other methods like PUT, DELETE, etc. if needed.
            else:
                print(f"Unsupported method {method} for request {req}. Skipping.")
                continue

            print(f"Sent {method} request to {req}, received status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send {method} request to {req}. Error: {e}")

def main():
    directory_path = './path_to_directory'  # Change this to your SOAPUI projects' directory

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.xml'):  # Assuming the SOAPUI project files have .xml extension
            file_path = os.path.join(directory_path, file_name)
            requests_list = extract_requests_from_soapui_project(file_path)
            send_requests_to_proxy(requests_list)

if __name__ == "__main__":
    main()
