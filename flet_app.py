import flet as ft
from flet import TextField, ElevatedButton, Text, Row, Column, Page
from flet_core import control, event, ControlEvent
import shutil, os, requests

counter = 0
hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
hosts_back = r"C:\Windows\System32\drivers\etc\hosts.bak"
hosts_temp = r"C:\Windows\System32\drivers\etc\hosts.tmp"
hosts_temp2 = r"C:\Windows\System32\drivers\etc\hosts.tmp2"

credentials = {"admin": "admin", "user2": "pass456"}


def downloadfile(url):
    response = requests.get(url)
    if response.status_code == 200:
        if "fakenews" in url:
            print(response.status_code)
            with open(hosts_temp, 'w') as tempfile:
                tempfile.write(response.text)
                print("finis writing")
                return
        else:
            print(response.status_code)
            with open(hosts_temp2, 'w') as tempfile2:
                tempfile2.write(response.text)
                print("finis writing temp2")
            return
    else:
        print("failed download")
        return "Failed"


def clenhost():
    global hosts_file
    try:
        shutil.copy(hosts_file, hosts_back)
        with open(hosts_file, 'w') as writehosts:
            writehosts.write("")
            print("File has been reset")
    except Exception as e:
        return e


clenhost()
# Constants
full_hosts = downloadfile(
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social-only/hosts")
unified_hosts = downloadfile("https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts")


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

    def restore():
        toastmessage("restore file")
        shutil.copy(hosts_back, hosts_file)
        print("restore file")

    def hardrest():
        global hosts_file
        try:
            with open(hosts_file, 'w') as writehosts:
                writehosts.write("")
                print("File has been reset")
                open_dlg("File has been reset")
        except Exception as e:
            open_dlg(e)
            return e


    def change_hosts(filtertype="F"):
        global hosts_temp, full_hosts, unified_hosts
        try:
            if filtertype == "F":
                shutil.copy(hosts_temp, hosts_file)
            else:
                shutil.copy(hosts_temp2, hosts_file)
            # os.system('ipconfig /flushdns')
            open_dlg("Setting has been applied")
            print("Hosts file replaced successfully.")
            return 0
        except Exception as e:
            open_dlg(f"Error change setting")
            print(f"Error change setting")

    # Buttons
    activate_button = ElevatedButton(text="Activate", width=200, on_click=lambda e: change_hosts())
    light_filter = ElevatedButton(text="Light Filter", width=200, on_click=lambda e: change_hosts("U"))
    restore_button = ElevatedButton(text="Restore", width=200, on_click=lambda e: restore())
    hardrest_button = ElevatedButton(text="Hard Reset", width=200, on_click=lambda e: hardrest())

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
                            restore_button,
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
# try:
ft.app(target=main)
# finally:
#     os.remove("C:\Windows\System32\drivers\etc\hosts.tmp")
#     os.remove("C:\Windows\System32\drivers\etc\hosts.tmp2")
