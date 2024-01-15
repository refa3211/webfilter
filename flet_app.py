from concurrent.futures import ThreadPoolExecutor
import flet as ft
from flet import TextField, ElevatedButton, Text, Row, Column, Page
from flet_core import control, event, ControlEvent
import shutil, os, requests, subprocess
from kill import get_pid_by_service, kill_process_by_pid

counter = 0
hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
hosts_back = r"C:\Windows\System32\drivers\etc\hosts.bak"
hosts_temp = r"C:\Windows\System32\drivers\etc\hosts.tmp"
hosts_temp2 = r"C:\Windows\System32\drivers\etc\hosts.tmp2"

credentials = {"admin": "admin", "user2": "pass456"}


##########################################################


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
        print("file is download")


urls = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social-only/hosts",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts"
]
filenames = [hosts_temp, hosts_temp2]

# with ThreadPoolExecutor(max_workers=2) as executor:
#     # Download files concurrently
#     executor.map(download_file, urls, filenames)
#
# print("Download complete.")


#################################################################


def is_file_locked(file_path):
    try:
        with open(file_path, 'r'):
            pass
        print("The file is not locked")
        return False  # The file is not locked
    except IOError as e:
        # Check if the IOError is due to a file being locked
        if "[Errno 13] Permission denied" in str(e):
            print("file is locked")
            return True  # The file is locked
        else:
            print(f"error file lock:  {e}")
            raise  # Propagate other IOErrors

def clenhost():
    global hosts_file
    try:
        shutil.copy(hosts_file, hosts_back)
        with open(hosts_file, 'w') as writehosts:
            writehosts.write("")
            print("File has been reset")
    except Exception as e:
        return e


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

    def dnskill():
        # pidi_num = get_pid_by_service('dnscache')
        toastmessage(f"kill service {get_pid_by_service('dnscache')}")
        kill_process_by_pid(get_pid_by_service('dnscache'))


    def backup():
        toastmessage("Backup file")
        shutil.copy(hosts_file, hosts_back)
        print("Backup file")

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
    def ring():
        pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
        open_dlg(page.add(pr))



    def change_hosts(filtertype="F"):
        global hosts_temp
        try:
            if filtertype == "F":
                shutil.copy(hosts_temp, hosts_file)
            else:
                shutil.copy(hosts_temp2, hosts_file)
            subprocess.run(['ipconfig', '/flushdns'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           creationflags=subprocess.CREATE_NO_WINDOW,
                           text=True)

            open_dlg("Setting has been applied")
            print("Hosts file replaced successfully.")
            return 0
        except Exception as e:
            open_dlg(f"Error change setting {e}")
            print(f"Error change setting {e}")

    # Buttons
    activate_button = ElevatedButton(text="Activate", width=200, on_click=lambda e: change_hosts())
    light_filter = ElevatedButton(text="Light Filter", width=200, on_click=lambda e: change_hosts("U"))
    ring_btn = ElevatedButton(text="ring", width=200, on_click=lambda e: ring())
    kill_btn = ElevatedButton(text="kill_btn", width=200, on_click=lambda e: dnskill())
    backup_button = ElevatedButton(text="Backup", width=200, on_click=lambda e: backup())
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
                            ring_btn,
                            kill_btn,
                            backup_button,
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
try:
    ft.app(target=main)
finally:
    os.remove(r"C:\Windows\System32\drivers\etc\hosts.tmp")
    os.remove(r"C:\Windows\System32\drivers\etc\hosts.tmp2")
