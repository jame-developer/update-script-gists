import sys
import requests
import os
import re


def get_current_used_go_version():
    token = os.getenv('GITHUB_TOKEN')
    gist_id = os.getenv('INSTALL_GOLANG_GIST_ID')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    gist_url = f"https://api.github.com/gists/{gist_id}"
    response = requests.get(gist_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get gist: {response.text}")
        return False
    print(response.json()['files']['install_golang.sh']['content'])
    current_version = extract_go_version(response.json()['files']['install_golang.sh']['content'])
    with open('current_go_version.txt', 'w') as file:
        file.write(current_version)
    return True

def get_latest_go_version():
    response = requests.get('https://golang.org/VERSION?m=text')
    if response.status_code != 200:
        print(f"Failed to get latest Go version: {response.text}")
        return False
    
    latest_go_version = response.text.split()[0]
    with open('latest_go_version.txt', 'w') as file:
        file.write(latest_go_version)
    return True


def update_gist():
    token = os.getenv('GITHUB_TOKEN')
    gist_id = os.getenv('INSTALL_GOLANG_GIST_ID')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }    
        
    with open('current_go_version.txt', 'r') as file:
        current_go_version = file.read().strip()
    with open('latest_go_version.txt', 'r') as file:
        latest_go_version = file.read().strip()
    
    gist_url = f"https://api.github.com/gists/{gist_id}"
    new_content = response.json()['files']['install_golang.sh']['content'].replace(current_go_version,
                                                                                       latest_go_version)
    data = {
        "files": {
            "install_golang.sh": {
                "content": new_content
            }
        }
    }
    response = requests.patch(gist_url, headers=headers, json=data)
    if response.status_code == 200:
        print("Gist updated successfully")
        return True
    else:    
        print(f"Failed to update gist: {response.text} ")
        return False
    


def extract_go_version(input_string):
    # Use a regular expression to find a line starting with 'GO_VERSION='
    match = re.search(r'^GO_VERSION=(.*)', input_string, re.MULTILINE)
    if match:
        return match.group(1)  # Return the captured group after '='
    return None


if __name__ == "__main__":
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GIST_ID = os.getenv('INSTALL_GOLANG_GIST_ID')
    success = False
    if sys.argv[1] == 'get_current_version':
        success = get_current_used_go_version()
    elif sys.argv[1] == 'get_latest_version':
        success = get_latest_go_version()
    elif sys.argv[1] == 'update_gist':
       success = update_gist()        
    if not success:
        exit(1)