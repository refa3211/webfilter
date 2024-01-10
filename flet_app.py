import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core import control, event, ControlEvent


def main(page: ft.page) -> None:
    page.title = 'Login'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 300
    page.window_height = 450

    text_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200, height=40)
    text_password: TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, height=40)
    button_loggin: ElevatedButton = ElevatedButton(text="Login", width=200, disabled=True)

    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value]):
            button_loggin.disabled = True
        else:
            button_loggin.disabled = False

    text_username.on_change = validate
    text_password.on_change = validate
    page.update()

    page.add(
        Row(
            controls=[
                Column([
                    text_username,
                    text_password,
                    button_loggin
                    ]
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()

    # page.add(
    #     Row(
    #         controls=[Column(
    #             text_username,
    #             text_password,
    #             button_loggin
    #         )
    #     ]
    #     )  
    # )


ft.app(target=main)
