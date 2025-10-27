import flet as ft
import random
from math import pi
import threading
from typing import Callable


class Controls:
    """Clase con controles y utilidades reutilizables para la aplicación"""
    
    @staticmethod
    def header_page(page: ft.Page) -> ft.Container:
        app_bar = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/")),
                    ft.Text("KINNEMA"),
                    ft.IconButton(ft.Icons.CODE_ROUNDED, url='https://github.com/Nosebone96/KINNEMA'),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            height=150,
            padding=ft.padding.symmetric(horizontal=35),
        )
        return app_bar
    
    @staticmethod
    def Buttons(e: ft.ControlEvent, Calcular: Callable, Limpiar: Callable) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.OutlinedButton(
                        'calcular',
                        on_click=Calcular,                
                        icon=ft.Icons.CALCULATE,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)),
                        icon_color='green',
                        height=50,
                        width=150,
                    ),
                    ft.OutlinedButton(
                        'limpiar',
                        on_click=Limpiar,
                        icon=ft.Icons.CLEANING_SERVICES,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)),
                        height=50,
                        width=150,
                        icon_color="red",
                    ),
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment=ft.CrossAxisAlignment.START, 
                height=50
            )
        )
    
    @staticmethod
    def cambio_Textfield(e: ft.ControlEvent) -> None:
        """Valida y cambia el color del borde del TextField según el valor ingresado"""
        Textfields = e.control
        if not isinstance(Textfields, ft.TextField):
            return
            
        try:
            if Textfields.value:
                float(Textfields.value)
                Textfields.border_color = None  # Restaurar color por defecto
            else:
                Textfields.border_color = None  # Restaurar color por defecto
        except ValueError:
            Textfields.border_color = ft.Colors.RED
        
        Textfields.update()
    
    @staticmethod
    def background(e: ft.ControlEvent) -> ft.Container:
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_right,
                end=ft.alignment.bottom_left,
                colors=["#0F3548", "#000000", "#000000"]
            ),
            expand=True, 
            margin=0, 
            padding=0
        )
    
    @staticmethod
    def example(page: ft.Page) -> ft.Container:
        """Crea una animación del logo KINNEMA"""
        size = 10
        gap = 3
        duration = 1500
        
        c1 = ft.Colors.PINK_500
        c2 = ft.Colors.AMBER_500
        c3 = ft.Colors.LIGHT_GREEN_500
        c4 = ft.Colors.DEEP_PURPLE_500
        c5 = ft.Colors.LIGHT_BLUE_500
        c6 = ft.Colors.RED_600
        
        all_colors = [
            ft.Colors.AMBER_400,
            ft.Colors.AMBER_ACCENT_400,
            ft.Colors.BLUE_400,
            ft.Colors.BROWN_400,
            ft.Colors.CYAN_700,
            ft.Colors.DEEP_ORANGE_500,
            ft.Colors.CYAN_500,
            ft.Colors.INDIGO_600,
            ft.Colors.ORANGE_ACCENT_100,
            ft.Colors.PINK,
            ft.Colors.RED_600,
            ft.Colors.GREEN_400,
            ft.Colors.GREEN_ACCENT_200,
            ft.Colors.TEAL_ACCENT_200,
            ft.Colors.LIGHT_BLUE_500,
        ]

        parts = [
            # K
            (0, 0, c1), (0, 1, c1), (0, 2, c1), (0, 3, c1), (0, 4, c1),
            (3, 0, c1), (2, 1, c1), (1, 2, c1), (1, 3, c1), (2, 3, c1), (3, 4, c1),
            # I
            (5, 0, c2), (5, 4, c2), (7, 0, c2), (7, 4, c2),
            (6, 0, c2), (6, 1, c2), (6, 2, c2), (6, 3, c2), (6, 4, c2),
            # N
            (9, 0, c3), (9, 1, c3), (9, 2, c3), (9, 3, c3), (9, 4, c3),
            (10, 0, c3), (10, 1, c3), (11, 2, c3), (12, 3, c3), (12, 4, c3),
            (13, 0, c3), (13, 1, c3), (13, 2, c3), (13, 3, c3), (13, 4, c3),
            # N
            (15, 0, c3), (15, 1, c3), (15, 2, c3), (15, 3, c3), (15, 4, c3),
            (16, 0, c3), (16, 1, c3), (17, 2, c3), (18, 3, c3), (18, 4, c3),
            (19, 0, c3), (19, 1, c3), (19, 2, c3), (19, 3, c3), (19, 4, c3),
            # E
            (21, 0, c4), (21, 1, c4), (21, 2, c4), (21, 3, c4), (21, 4, c4),
            (22, 0, c4), (22, 2, c4), (22, 4, c4),
            (23, 0, c4), (23, 2, c4), (23, 4, c4),
            # M
            (25, 0, c5), (25, 1, c5), (25, 2, c5), (25, 3, c5), (25, 4, c5),
            (26, 0, c5), (26, 1, c5), (27, 1, c5), (27, 2, c5),
            (28, 1, c5), (28, 0, c5), (29, 0, c5), (29, 1, c5),
            (29, 2, c5), (29, 3, c5), (29, 4, c5),
            # A
            (31, 0, c6), (31, 1, c6), (31, 2, c6), (31, 3, c6), (31, 4, c6),
            (32, 0, c6), (32, 2, c6), (33, 0, c6), (33, 2, c6),
            (34, 0, c6), (34, 1, c6), (34, 2, c6), (34, 3, c6), (34, 4, c6),
        ]

        width = 100 * (size + gap)
        height = 30 * (size + gap)

        canvas = ft.Stack(
            width=width,
            height=height,
            animate_scale=duration,
            animate_opacity=duration,
        )

        # Spread parts randomly
        for i in range(len(parts)):
            canvas.controls.append(
                ft.Container(
                    animate=duration,
                    animate_position=duration,
                    animate_rotation=duration,
                )
            )

        def randomize(e: ft.ControlEvent) -> None:
            random.seed()
            for i in range(len(parts)):
                c = canvas.controls[i]
                part_size = random.randrange(int(size / 2), int(size * 3))
                c.left = random.randrange(0, width)
                c.top = random.randrange(0, height)
                c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
                c.width = part_size
                c.height = part_size
                c.border_radius = random.randrange(0, int(size / 2))
                c.rotate = random.randrange(0, 90) * 2 * pi / 360
            canvas.scale = 5
            canvas.opacity = 0.3
            go_button.visible = True
            page.update()

        def assemble(e: ft.ControlEvent | None) -> None:
            i = 0
            for left, top, bgcolor in parts:
                c = canvas.controls[i]
                c.left = left * (size + gap)
                c.top = top * (size + gap)
                c.bgcolor = bgcolor
                c.width = size
                c.height = size
                c.border_radius = 5
                c.rotate = 0
                i += 1
            canvas.scale = 1
            canvas.opacity = 1
            go_button.visible = False
            page.update()

        go_button = ft.ElevatedButton("Go!", on_click=assemble, visible=True)
                
        def delayed_assemble() -> None:
            assemble(None)
        
        timer = threading.Timer(1, delayed_assemble)
        timer.start()
        
        return ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Container(height=25, width=1),
                    canvas,
                ],
            ),
        )

    @staticmethod
    def containers(page: ft.Page) -> ft.Container:
        """Genera contenedores aleatorios decorativos en el fondo"""
        size = 30
        gap = 3
        
        page_width = 15 * (size + gap)
        page_height = 10 * (size + gap)
        
        num_containers = 15
        thinks = ft.Stack(
            width=page_width,
            height=page_height,
        )
        
        # Generar contenedores aleatorios
        for _ in range(num_containers):
            x_pos = random.randrange(30, page_width)
            y_pos = random.randrange(30, page_height)
            part_size = random.randrange(int(size / 2), int(size * 3))
            color = ft.Colors.Random_Color()

            container = ft.Container(
                width=part_size,
                height=part_size,
                bgcolor=color,
                border_radius=10,
                left=x_pos,
                top=y_pos,
                opacity=0.05
            )

            thinks.controls.append(container)
        
        thinks.scale = 4
            
        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.TRANSPARENT,
            padding=10,
            content=ft.Column(
                tight=True,
                controls=[thinks],
            ),
        )