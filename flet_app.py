import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core import control, event, ControlEvent
import os
import requests
from kill import kill_process_by_pid, get_pid_by_service
from pyuac import main_requires_admin

# Constants
full_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social-only/hosts"
Unified_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts"
credentials = {"admin": "admin", "user2": "pass456", "user3": "pass789"}
counter = 0
import shutil

hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
hosts_back = r"C:\Windows\System32\drivers\etc\hosts.bak"
hosts_temp = r"C:\Windows\System32\drivers\etc\hosts.tmp"


# Decorator to require admin privileges
@main_requires_admin
def main(page: ft.page) -> None:
    # Page settings
    page.title = 'Login'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 750
    page.window_height = 600

    # Function to open a dialog
    def open_dlg(e):
        dlg = ft.AlertDialog(title=ft.Text(f"{e}"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Function to back up the hosts file
    def backup():
        toastmessage("Backup existing file")
        os.system('copy "C:\Windows\System32\drivers\etc\hosts" "C:\Windows\system32\drivers\etc\hosts.bak"')
        open_dlg()

    def killin():
        try:
            toastmessage("kill process..")
            toastmessage(f"trying kill process {get_pid_by_service('dnscache')}")
            kill_process_by_pid(get_pid_by_service("dnscache"))
        except Exception as e:
            toastmessage(e)

    # Function to reset the hosts file
    def hardrest(hosts_path=hosts_temp):
        try:
            killin()
            with open(hosts_path, 'w') as writehosts:
                writehosts.write("")
            shutil.copy(hosts_temp, hosts_file)
            open_dlg("File has been reset")
        except Exception as e:
            open_dlg(e)

    # Function to download hosts file
    def download_hosts_file(url=full_hosts):
        global hosts_temp
        try:
            toastmessage("Starting Download ...")
            response = requests.get(url)
            if response.status_code == 200:
                print(response.status_code)
                try:
                    toastmessage("Loading...")
                    with open(hosts_temp, 'w') as write_hosts:
                        write_hosts.write(response.text)
                    killin()
                    shutil.copy(hosts_temp, hosts_file)
                    open_dlg("Setting has been applied")
                    print("Hosts file replaced successfully.")
                except Exception as e:
                    print(f"Error while setup settings [61]: {e}")
                    open_dlg(e)
                    return e
                return response.text
            else:
                open_dlg(response.status_code)
                print(f"Failed to download hosts file. Status code: {response.status_code}")
        except Exception as e:
            open_dlg(e)
            print(f"Error downloading hosts file: {e}")

    # Buttons
    activate_button: ElevatedButton = ElevatedButton(text="Activate", width=200,
                                                     on_click=lambda e: download_hosts_file())
    light_filter: ElevatedButton = ElevatedButton(text="Light Filter", width=200,
                                                  on_click=lambda e: download_hosts_file(Unified_hosts))
    backup_button: ElevatedButton = ElevatedButton(text="Backup", width=200, on_click=lambda e: backup())
    hardrest_button: ElevatedButton = ElevatedButton(text="Hard Reset", width=200, on_click=lambda e: hardrest())

    kill_button: ElevatedButton = ElevatedButton(text="Kill Process", width=200, on_click=lambda e: killin())

    # Function to display toast messages
    def toastmessage(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    # Function to handle login button click
    def on_click(e):
        global counter
        if text_username.value in credentials and credentials[text_username.value] == text_password.value:
            toastmessage("Successful Login")
            page.clean()
            page.add(
                Row(
                    controls=[
                        Column([
                            activate_button,
                            light_filter,
                            backup_button,
                            hardrest_button,
                            kill_button
                        ])
                    ], alignment=ft.MainAxisAlignment.CENTER
                )
            )
            page.update()
        else:
            print(counter)
            counter += 1
            if counter >= 3:
                exit()
            toastmessage("Username or Password not correct!")

    # Page components
    text_label: Text = Text(value="WebFilter", size=30, text_align=ft.TextAlign.CENTER)
    text_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200, height=40)
    text_password: TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, height=40,
                                         password=True)
    button_login: ElevatedButton = ElevatedButton(text="Login", width=200, disabled=True, on_click=on_click)

    # Function to validate login fields
    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value]):
            button_login.disabled = False
        else:
            button_login.disabled = True
        page.update()

    # Page layout
    page.add(
        Row(
            controls=[
                Column([
                    text_label,
                    text_username,
                    text_password,
                    button_login
                ])
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )

    # Event listeners
    text_username.on_change = validate
    text_password.on_change = validate
    page.update()


# Run the app
ft.app(target=main)
