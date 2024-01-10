import os
import requests

def download_hosts_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to download hosts file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading hosts file: {e}")

def replace_hosts_file(contents):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    try:
        with open(hosts_path, 'w') as hosts_file:
            hosts_file.write(contents)
        print("Hosts file replaced successfully.")
    except Exception as e:
        print(f"Error replacing hosts file: {e}")

if __name__ == "__main__":
    github_hosts_url = "https://raw.githubusercontent.com/someuser/somerepo/main/hosts_file.txt"
    
    # Download hosts file from GitHub
    hosts_content = download_hosts_file(github_hosts_url)
    
    if hosts_content:
        # Replace the local hosts file
        replace_hosts_file(hosts_content)
    else:
        print("Failed to download hosts file. Exiting.")
