import tkinter as tk
from tkinter import messagebox
from get_hosts import clean_hosts, download_hosts_file, github_hosts_url
from pyuac import main_requires_admin



class LoginApp:
    @main_requires_admin
    def __init__(self, root):
        self.root = root
        self.root.title("Login App")
        self.root.minsize(500, 350)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack(pady=15)

        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=15)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(pady=15)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=15)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # In-memory storage for usernames and passwords (replace with a secure database)
        self.credentials = {"admin": "admin", "user2": "pass456", "user3": "pass789"}

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.credentials and self.credentials[username] == password:
            # messagebox.showinfo(f"Login Successful", "Welcome, {}".format(username))
            self.show_success_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_success_page(self):
        # Destroy login widgets
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()

        # Create success page widgets
        success_label = tk.Label(self.root, text="Login Successful!")
        success_label.pack(pady=10)

        # filter_button = tk.Button(self.root, text="filter", command=download_hosts_file(url=github_hosts_url))
        # filter_button.pack(pady=15)
        filter_button = tk.Button(root, text="Filter", command=lambda: download_hosts_file(url=github_hosts_url))
        filter_button.pack(pady=15)

        unfilter_button = tk.Button(self.root, text="Unfilter", command=lambda: download_hosts_file(url=clean_hosts))
        unfilter_button.pack(pady=15)

        logout_button = tk.Button(self.root, text="Logout", command=self.root.destroy)
        logout_button.pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
