import flet as ft
from flet import TextField, ElevatedButton, Text, Row, Column
from flet_core import control, event, ControlEvent
import shutil, os, requests
from kill import kill_process_by_pid, get_pid_by_service
from pyuac import main_requires_admin

# Constants
full_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social-only/hosts"
Unified_hosts = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts"
credentials = {"admin": "admin", "user2": "pass456"}
counter = 0

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
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2)

    # Function to open a dialog
    def open_dlg(e):
        dlg = ft.AlertDialog(title=ft.Text(f"{e}"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Function to back up the hosts file
    def backup():
        toastmessage("Backup existing file")
        shutil.copy(hosts_file, hosts_back)
        # open_dlg()

    def ring():
        pri = ft.ProgressRing(width=16, height=16, stroke_width=2)

        page.add(
            ft.Row([pri]),
            ft.Column(
                [ft.ProgressRing()],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
            ),
        )

    def killin():
        try:
            toastmessage(f"trying kill process {get_pid_by_service('dnscache')}")
            kill_process_by_pid(get_pid_by_service("dnscache"))
        except Exception as e:
            toastmessage(e)

    # Function to reset the hosts file
    def hardrest():
        global hosts_temp, hosts_file
        try:
            killin()
            with open(hosts_temp, 'w') as writehosts:
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
            ring()
            response = requests.get(url)
            if response.status_code == 200:
                print(response.status_code)
                try:

                    toastmessage("Loading...")
                    with open(hosts_temp, 'w') as write_hosts:
                        write_hosts.write(response.text)

                    os.system('ipconfig /flushdns')
                    killin()
                    shutil.copy(hosts_temp, hosts_file)
                    open_dlg("Setting has been applied")
                    print("Hosts file replaced successfully.")
                except Exception as e:
                    print(f"Error while setup settings [80]: {e}")
                    open_dlg(e)
                    return e

            else:
                open_dlg(f"Failed to download hosts file. Status code: {response.status_code}")
                print(f"Failed to download hosts file. Status code: {response.status_code}")
        except Exception as e:
            open_dlg(f"Error downloading hosts file: {e}")
            print(f"Error downloading hosts file: {e}")

    # Buttons
    activate_button = ElevatedButton(text="Activate", width=200, on_click=lambda e: download_hosts_file())
    light_filter = ElevatedButton(text="Light Filter", width=200, on_click=lambda e: download_hosts_file(Unified_hosts))
    backup_button = ElevatedButton(text="Backup", width=200, on_click=lambda e: backup())
    hardrest_button = ElevatedButton(text="Hard Reset", width=200, on_click=lambda e: hardrest())
    kill_button = ElevatedButton(text="Kill Process", width=200, on_click=lambda e: killin())

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
    text_label = Text(value="WebFilter", size=30, text_align=ft.TextAlign.CENTER)
    text_username = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200, height=40)
    text_password = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, height=40, password=True)
    button_login = ElevatedButton(text="Login", width=200, disabled=True, on_click=on_click)

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
