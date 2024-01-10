import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core import control, event, ControlEvent
# from get_hosts import clean_hosts, download_hosts_file, github_hosts_url
from pyuac import main_requires_admin
import os
import requests

full_hosts = (
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts")
Unified_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-porn/hosts"

credentials = {"admin": "admin", "user2": "pass456", "user3": "pass789"}


# @main_requires_admin
def main(page: ft.page) -> None:
    page.title = 'Login'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 750
    page.window_height = 600

    # dlg = ft.AlertDialog(title=ft.Text(f"{e}"))

    def open_dlg(e):
        dlg = ft.AlertDialog(title=ft.Text(f"{e}"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def download_hosts_file(url=full_hosts):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
                try:
                    os.system("ipconfig /flushdns")
                    # print(response.text)
                    with open(hosts_path, 'w') as hosts_file:
                        hosts_file.write(response.text)
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

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )
    activatebutton: ElevatedButton = ElevatedButton(text="Activate", width=200,
                                                    on_click=lambda e: download_hosts_file())
    disablebutton: ElevatedButton = ElevatedButton(text="Disable", width=200,
                                                   on_click=lambda e: download_hosts_file(Unified_hosts))

    def on_click(e):
        if text_username.value in credentials and credentials[text_username.value] == text_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Successful Login"))
            page.snack_bar.open = True
            page.update()
            page.clean()
            page.add(
                Row(
                    controls=[
                        Column([
                            activatebutton,
                            disablebutton
                        ]
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER
                )
            )

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Username or Password not correct!"))
            page.snack_bar.open = True
            page.update()

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
