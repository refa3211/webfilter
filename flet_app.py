import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core import control, event, ControlEvent
# from get_hosts import clean_hosts, download_hosts_file, github_hosts_url
from pyuac import main_requires_admin
import os
import requests

full_hosts = (
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social-only/hosts")
Unified_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts"
# Unified_hosts = r"C:\Windows\System32\drivers\etc\hosts.txt"
credentials = {"admin": "admin", "user2": "pass456", "user3": "pass789"}

counter = 0


@main_requires_admin
def main(page: ft.page) -> None:
    page.title = 'Login'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 750
    page.window_height = 600

    def open_dlg(e):
        dlg = ft.AlertDialog(title=ft.Text(f"{e}"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def backup():
        os.system('copy "C:\Windows\System32\drivers\etc\hosts" "C:\Windows\system32\drivers\etc\hosts.txt"')
        # os.system('$p=Tasklist /svc /fi "SERVICES eq windefend" /fo csv | convertfrom-csv')
        # pid = os.system("taskkill /pid $p.PID /f")

    def hardrest(hosts_path="C:\Windows\System32\drivers\etc\hosts"):
        with open(hosts_path, 'w') as hosts_file:
            hosts_file.write("127.0.0.1 localhost")
            toastmessage("file has reset")

    def download_hosts_file(url=full_hosts):
        try:
            print("try download")
            toastmessage("Starting Download")
            page.update()
            response = requests.get(url)
            if response.status_code == 200:
                print(response.status_code)
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
                try:
                    # os.system("ipconfig /flushdns")
                    os.system(
                        'copy "C:\Windows\System32\drivers\etc\hosts" "C:\Windows\system32\drivers\etc\hosts.txt"')
                    with open(hosts_path, 'w') as hosts_file:
                        hosts_file.write(response.text)
                    toastmessage("Hosts file replaced successfully.")
                    print("Hosts file replaced successfully.")
                except Exception as e:
                    print(f"Error replacing hosts file: {e}")
                    open_dlg(e)
                    page.update()
                    return e

                return response.text
            else:
                open_dlg(response.status_code)
                page.update()
                print(f"Failed to download hosts file. Status code: {response.status_code}")
        except Exception as e:
            open_dlg(e)
            page.update()
            print(f"Error downloading hosts file: {e}")

    activatebutton: ElevatedButton = ElevatedButton(text="Activate", width=200,
                                                    on_click=lambda e: download_hosts_file())
    disablebutton: ElevatedButton = ElevatedButton(text="Disable", width=200,
                                                   on_click=lambda e: download_hosts_file(Unified_hosts))
    backup_button: ElevatedButton = ElevatedButton(text="Backup", width=200,
                                                   on_click=lambda e: backup())

    hardrest_button: ElevatedButton = ElevatedButton(text="hardrest_button", width=200,
                                                     on_click=lambda e: hardrest())

    def toastmessage(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def on_click(e):
        global counter
        if text_username.value in credentials and credentials[text_username.value] == text_password.value:
            toastmessage("Successful Login")
            page.clean()
            page.add(
                Row(
                    controls=[
                        Column([
                            activatebutton,
                            disablebutton,
                            backup_button,
                            hardrest_button
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

    text_label: Text = Text(value="WebFilter", size=30, text_align=ft.TextAlign.CENTER)
    text_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200, height=40)
    text_password: TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, height=40,
                                         password=True)
    button_login: ElevatedButton = ElevatedButton(text="Login", width=200, disabled=True, on_click=on_click)

    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value]):
            button_login.disabled = False
        else:
            button_login.disabled = True
        page.update()

    page.update()

    page.add(
        Row(
            controls=[
                Column([
                    text_label,
                    text_username,
                    text_password,
                    button_login
                ]
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )

    text_username.on_change = validate
    text_password.on_change = validate
    page.update()

    page.update()


ft.app(target=main)
