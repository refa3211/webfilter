import flet as ft
from flet import ProgressRing
from time import sleep


def main(page: ft.Page):
    # pr = ft.ProgressRing(width=50, height=50, stroke_width=3, value=0.1)
    #
    # page.add(
    #     ft.Text("Circular progress indicator", style="headlineSmall"),
    #     ft.Row([pr], alignment=ft.MainAxisAlignment.CENTER),
    #     ft.Row(
    #         [ft.ProgressRing(width=50, height=50, stroke_width=10, color='green')],
    #         alignment=ft.MainAxisAlignment.CENTER
    #     ))
    #
    # for i in range(0, 101):
    #     pr.value = i * 0.05
    #     sleep(0.1)
    #     page.update()

    ################################################
    page.title = "AlertDialog examples"

    dlg = ft.AlertDialog(
        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    # dlg2 = ft.AlertDialog(
    #     content=
    # )

    page.dialog = (ft.AlertDialog(ProgressRing(width=2)))

    def open_dlg(e):
        # page.dialog = dlg
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_dlg2(e):
        # page.dialog = dlg
        page.dialog = ProgressRing()
        dlg.open = True
        page.update()

    page.add(
        ft.ElevatedButton("Open dialog", on_click=open_dlg),
        ft.ElevatedButton("Open dialog2", on_click=open_dlg2),
    )


ft.app(target=main)
