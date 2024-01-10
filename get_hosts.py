import os

import requests


github_hosts_url = ("https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn"
                    "-social-only/hosts")
clean_hosts = "https://raw.githubusercontent.com/refa3211/webfilter/main/hosts"



def download_hosts_file(url=github_hosts_url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            try:
                # print(response.text)
                with open(hosts_path, 'w') as hosts_file:
                    hosts_file.write(response.text)
                print("Hosts file replaced successfully.")
            except Exception as e:
                print(f"Error replacing hosts file: {e}")
            
            return response.text
        else:
            print(f"Failed to download hosts file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading hosts file: {e}")

