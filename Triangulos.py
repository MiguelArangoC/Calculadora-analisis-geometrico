import flet as ft
import math as Math

# try import controls; if not present, provide minimal fallbacks
try:
    import controls
except Exception:
    class _ControlsFallback:
        @staticmethod
        def header_page(page):
            return ft.Container()

        @staticmethod
        def background(container):
            return ft.Container()

        @staticmethod
        def containers(page):
            return ft.Container()
    controls = _ControlsFallback()

def main_triangulo(page: ft.Page) -> ft.View:
    page.title = "Resolución de Triangulo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # TextFields
    lado_a = ft.TextField(label="Lado A", width=230)
    lado_b = ft.TextField(label="Lado B", width=230)
    lado_c = ft.TextField(label="Lado C", width=230)
    angulo_a = ft.TextField(label="Angulo A", width=230)
    angulo_b = ft.TextField(label="Angulo B", width=230)
    angulo_c = ft.TextField(label="Angulo C", width=230)

    area = ft.TextField(label="Area", disabled=True, width=150)
    perimetro = ft.TextField(label="Perimetro", disabled=True, width=150)
    semiperimetro = ft.TextField(label="Semiperimetro", disabled=True, width=150)
    altura_ha = ft.TextField(label="Altura ha", disabled=True, width=150)
    altura_hb = ft.TextField(label="Altura hb", disabled=True, width=150)
    altura_hc = ft.TextField(label="Altura hc", disabled=True, width=150)
    inradio = ft.TextField(label="Inradio", disabled=True, width=150)
    circunradio = ft.TextField(label="Circunradio", disabled=True, width=150)
    Mediana_ma = ft.TextField(label="Mediana ma", disabled=True, width=150)
    Mediana_mb = ft.TextField(label="Mediana mb", disabled=True, width=150)
    Mediana_mc = ft.TextField(label="Mediana mc", disabled=True, width=150)

    def clamp(x):
        if x is None:
            return None
        return max(-1.0, min(1.0, x))

    def Limpiar_triangulo(e):
        lado_a.value = ''
        lado_b.value = ''
        lado_c.value = ''
        angulo_a.value = ''
        angulo_b.value = ''
        angulo_c.value = ''
        area.value = ''
        perimetro.value = ''
        semiperimetro.value = ''
        altura_ha.value = ''
        altura_hb.value = ''
        altura_hc.value = ''
        inradio.value = ''
        circunradio.value = ''
        Mediana_ma.value = ''
        Mediana_mb.value = ''
        Mediana_mc.value = ''
        page.update()

    def calcular_click(e):
        # contexto mutable para valores
        ctx = {
            "a": 0.0, "b": 0.0, "c": 0.0,
            "A": 0.0, "B": 0.0, "C": 0.0,
            "angulos_faltantes": 0, "lados_faltantes": 0,
            "area": 0.0, "semiperimetro": 0.0
        }

        # leer campos (si no convertible, contar como faltante)
        try:
            ctx["a"] = float(lado_a.value)
        except Exception:
            ctx["a"] = 0.0
            ctx["lados_faltantes"] += 1
        try:
            ctx["b"] = float(lado_b.value)
        except Exception:
            ctx["b"] = 0.0
            ctx["lados_faltantes"] += 1
        try:
            ctx["c"] = float(lado_c.value)
        except Exception:
            ctx["c"] = 0.0
            ctx["lados_faltantes"] += 1
        try:
            ctx["A"] = float(angulo_a.value)
        except Exception:
            ctx["A"] = 0.0
            ctx["angulos_faltantes"] += 1
        try:
            ctx["B"] = float(angulo_b.value)
        except Exception:
            ctx["B"] = 0.0
            ctx["angulos_faltantes"] += 1
        try:
            ctx["C"] = float(angulo_c.value)
        except Exception:
            ctx["C"] = 0.0
            ctx["angulos_faltantes"] += 1

        # helper funciones que mutan ctx
        def ley_seno_ALL():
            try:
                if ctx["A"] != 0 and ctx["a"] != 0:
                    if ctx["b"] != 0 and ctx["B"] == 0:
                        ratio = (ctx["b"] * Math.sin(Math.radians(ctx["A"]))) / ctx["a"]
                        ratio = clamp(ratio)
                        ctx["B"] = Math.degrees(Math.asin(ratio))
                        angulo_b.value = f'{round(ctx["B"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                    elif ctx["c"] != 0 and ctx["C"] == 0:
                        ratio = (ctx["c"] * Math.sin(Math.radians(ctx["A"]))) / ctx["a"]
                        ratio = clamp(ratio)
                        ctx["C"] = Math.degrees(Math.asin(ratio))
                        angulo_c.value = f'{round(ctx["C"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                elif ctx["B"] != 0 and ctx["b"] != 0:
                    if ctx["a"] != 0 and ctx["A"] == 0:
                        ratio = (ctx["a"] * Math.sin(Math.radians(ctx["B"]))) / ctx["b"]
                        ratio = clamp(ratio)
                        ctx["A"] = Math.degrees(Math.asin(ratio))
                        angulo_a.value = f'{round(ctx["A"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                    elif ctx["c"] != 0 and ctx["C"] == 0:
                        ratio = (ctx["c"] * Math.sin(Math.radians(ctx["B"]))) / ctx["b"]
                        ratio = clamp(ratio)
                        ctx["C"] = Math.degrees(Math.asin(ratio))
                        angulo_c.value = f'{round(ctx["C"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                elif ctx["C"] != 0 and ctx["c"] != 0:
                    if ctx["a"] != 0 and ctx["A"] == 0:
                        ratio = (ctx["a"] * Math.sin(Math.radians(ctx["C"]))) / ctx["c"]
                        ratio = clamp(ratio)
                        ctx["A"] = Math.degrees(Math.asin(ratio))
                        angulo_a.value = f'{round(ctx["A"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                    elif ctx["b"] != 0 and ctx["B"] == 0:
                        ratio = (ctx["b"] * Math.sin(Math.radians(ctx["C"]))) / ctx["c"]
                        ratio = clamp(ratio)
                        ctx["B"] = Math.degrees(Math.asin(ratio))
                        angulo_b.value = f'{round(ctx["B"], 2)}'
                        ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
            except Exception:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Verifica que los datos digitados sean correctos"))
                page.snack_bar.open = True

        def ley_coseno_LLL():
            try:
                if ctx["A"] == 0 and ctx["b"] != 0 and ctx["c"] != 0:
                    val = (Math.pow(ctx["b"], 2) + Math.pow(ctx["c"], 2) - Math.pow(ctx["a"], 2)) / (2.0 * ctx["b"] * ctx["c"])
                    val = clamp(val)
                    ctx["A"] = Math.degrees(Math.acos(val))
                    angulo_a.value = f'{round(ctx["A"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                if ctx["B"] == 0 and ctx["a"] != 0 and ctx["c"] != 0:
                    val = (Math.pow(ctx["a"], 2) + Math.pow(ctx["c"], 2) - Math.pow(ctx["b"], 2)) / (2.0 * ctx["a"] * ctx["c"])
                    val = clamp(val)
                    ctx["B"] = Math.degrees(Math.acos(val))
                    angulo_b.value = f'{round(ctx["B"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                if ctx["C"] == 0 and ctx["a"] != 0 and ctx["b"] != 0:
                    val = (Math.pow(ctx["a"], 2) + Math.pow(ctx["b"], 2) - Math.pow(ctx["c"], 2)) / (2.0 * ctx["a"] * ctx["b"])
                    val = clamp(val)
                    ctx["C"] = Math.degrees(Math.acos(val))
                    angulo_c.value = f'{round(ctx["C"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
            except Exception:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Verifica que los datos digitados sean correctos"))
                page.snack_bar.open = True

        def ley_seno_ALA():
            try:
                # tercer ángulo si faltante
                if ctx["A"] != 0 and ctx["B"] != 0 and ctx["C"] == 0:
                    ctx["C"] = 180 - (ctx["A"] + ctx["B"])
                    angulo_c.value = f'{round(ctx["C"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                elif ctx["B"] != 0 and ctx["C"] != 0 and ctx["A"] == 0:
                    ctx["A"] = 180 - (ctx["B"] + ctx["C"])
                    angulo_a.value = f'{round(ctx["A"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)
                elif ctx["C"] != 0 and ctx["A"] != 0 and ctx["B"] == 0:
                    ctx["B"] = 180 - (ctx["C"] + ctx["A"])
                    angulo_b.value = f'{round(ctx["B"], 2)}'
                    ctx["angulos_faltantes"] = max(0, ctx["angulos_faltantes"] - 1)

                # aplicar ley del seno para lados
                if ctx["a"] != 0 and ctx["A"] != 0:
                    if ctx["b"] == 0 and ctx["B"] != 0:
                        denom = Math.sin(Math.radians(ctx["A"]))
                        if denom != 0:
                            ctx["b"] = (ctx["a"] * Math.sin(Math.radians(ctx["B"]))) / denom
                            lado_b.value = f'{round(ctx["b"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
                    if ctx["c"] == 0 and ctx["C"] != 0:
                        denom = Math.sin(Math.radians(ctx["A"]))
                        if denom != 0:
                            ctx["c"] = (ctx["a"] * Math.sin(Math.radians(ctx["C"]))) / denom
                            lado_c.value = f'{round(ctx["c"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)

                elif ctx["b"] != 0 and ctx["B"] != 0:
                    if ctx["a"] == 0 and ctx["A"] != 0:
                        denom = Math.sin(Math.radians(ctx["B"]))
                        if denom != 0:
                            ctx["a"] = (ctx["b"] * Math.sin(Math.radians(ctx["A"]))) / denom
                            lado_a.value = f'{round(ctx["a"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
                    if ctx["c"] == 0 and ctx["C"] != 0:
                        denom = Math.sin(Math.radians(ctx["B"]))
                        if denom != 0:
                            ctx["c"] = (ctx["b"] * Math.sin(Math.radians(ctx["C"]))) / denom
                            lado_c.value = f'{round(ctx["c"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)

                elif ctx["c"] != 0 and ctx["C"] != 0:
                    if ctx["a"] == 0 and ctx["A"] != 0:
                        denom = Math.sin(Math.radians(ctx["C"]))
                        if denom != 0:
                            ctx["a"] = (ctx["c"] * Math.sin(Math.radians(ctx["A"]))) / denom
                            lado_a.value = f'{round(ctx["a"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
                    if ctx["b"] == 0 and ctx["B"] != 0:
                        denom = Math.sin(Math.radians(ctx["C"]))
                        if denom != 0:
                            ctx["b"] = (ctx["c"] * Math.sin(Math.radians(ctx["B"]))) / denom
                            lado_b.value = f'{round(ctx["b"], 2)}'
                            ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
            except Exception:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Verifica que los datos digitados sean correctos"))
                page.snack_bar.open = True

        def ley_coseno_LAL():
            try:
                if ctx["a"] == 0 and ctx["b"] != 0 and ctx["c"] != 0 and ctx["A"] != 0:
                    ctx["a"] = Math.sqrt(Math.pow(ctx["b"], 2) + Math.pow(ctx["c"], 2) - 2 * ctx["b"] * ctx["c"] * Math.cos(Math.radians(ctx["A"])))
                    lado_a.value = f'{round(ctx["a"], 2)}'
                    ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
                if ctx["b"] == 0 and ctx["a"] != 0 and ctx["c"] != 0 and ctx["B"] != 0:
                    ctx["b"] = Math.sqrt(Math.pow(ctx["a"], 2) + Math.pow(ctx["c"], 2) - 2 * ctx["a"] * ctx["c"] * Math.cos(Math.radians(ctx["B"])))
                    lado_b.value = f'{round(ctx["b"], 2)}'
                    ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
                if ctx["c"] == 0 and ctx["a"] != 0 and ctx["b"] != 0 and ctx["C"] != 0:
                    ctx["c"] = Math.sqrt(Math.pow(ctx["a"], 2) + Math.pow(ctx["b"], 2) - 2 * ctx["a"] * ctx["b"] * Math.cos(Math.radians(ctx["C"])))
                    lado_c.value = f'{round(ctx["c"], 2)}'
                    ctx["lados_faltantes"] = max(0, ctx["lados_faltantes"] - 1)
            except Exception:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Verifica que los datos digitados sean correctos"))
                page.snack_bar.open = True

        # iterar para intentar resolver incógnitas
        i = 0
        while (ctx["angulos_faltantes"] > 0 or ctx["lados_faltantes"] > 0) and i < 4:
            if ctx["a"] == 0 or ctx["b"] == 0 or ctx["c"] == 0:
                if ctx["angulos_faltantes"] <= 2 and ctx["lados_faltantes"] <= 1:
                    ley_coseno_LAL()
                if ctx["angulos_faltantes"] <= 2 and ctx["lados_faltantes"] <= 1:
                    ley_seno_ALL()
                if ctx["angulos_faltantes"] <= 1 and ctx["lados_faltantes"] <= 2:
                    ley_seno_ALA()
            else:
                ley_coseno_LLL()
            i += 1

        # semiperimetro
        try:
            s = (ctx["a"] + ctx["b"] + ctx["c"]) / 2
            ctx["semiperimetro"] = s
            semiperimetro.value = f'{round(s, 2)}'
        except Exception:
            semiperimetro.value = ''

        # area (Heron) guardando dominio
        try:
            s = ctx["semiperimetro"]
            if s > 0 and (s - ctx["a"]) >= 0 and (s - ctx["b"]) >= 0 and (s - ctx["c"]) >= 0:
                ar = Math.sqrt(s * (s - ctx["a"]) * (s - ctx["b"]) * (s - ctx["c"]))
            else:
                ar = 0.0
            ctx["area"] = ar
            area.value = f'{round(ar, 2)}' if ar != 0 else ''
        except Exception:
            area.value = ''

        # alturas
        def hl_triangulo(area_val, p):
            try:
                if p == 0:
                    return 0.0
                return (2 * area_val) / p
            except Exception:
                return 0.0

        ha = hl_triangulo(ctx["area"], ctx["a"])
        hb = hl_triangulo(ctx["area"], ctx["b"])
        hc = hl_triangulo(ctx["area"], ctx["c"])
        altura_ha.value = f'{round(ha, 2)}' if ha != 0 else ''
        altura_hb.value = f'{round(hb, 2)}' if hb != 0 else ''
        altura_hc.value = f'{round(hc, 2)}' if hc != 0 else ''

        # inradio
        try:
            if ctx["semiperimetro"] != 0:
                ir = ctx["area"] / ctx["semiperimetro"]
            else:
                ir = 0.0
            inradio.value = f'{round(ir, 2)}' if ir != 0 else ''
        except Exception:
            inradio.value = ''

        # circunradio
        try:
            if ctx["area"] != 0:
                cr = (ctx["a"] * ctx["b"] * ctx["c"]) / (4 * ctx["area"])
            else:
                cr = 0.0
            circunradio.value = f'{round(cr, 2)}' if cr != 0 else ''
        except Exception:
            circunradio.value = ''

        # medianas
        def mediana(p1, p2, p3):
            try:
                return 0.5 * Math.sqrt(2 * Math.pow(p1, 2) + 2 * Math.pow(p2, 2) - Math.pow(p3, 2))
            except Exception:
                return 0.0

        ma = mediana(ctx["b"], ctx["c"], ctx["a"]) if (ctx["b"] and ctx["c"]) else 0.0
        mb = mediana(ctx["a"], ctx["c"], ctx["b"]) if (ctx["a"] and ctx["c"]) else 0.0
        mc = mediana(ctx["a"], ctx["b"], ctx["c"]) if (ctx["a"] and ctx["b"]) else 0.0
        Mediana_ma.value = f'{round(ma, 2)}' if ma != 0 else ''
        Mediana_mb.value = f'{round(mb, 2)}' if mb != 0 else ''
        Mediana_mc.value = f'{round(mc, 2)}' if mc != 0 else ''

        # perimetro
        try:
            per = (ctx["a"] + ctx["b"] + ctx["c"])
            perimetro.value = f'{round(per, 2)}' if per != 0 else ''
        except Exception:
            perimetro.value = ''

        # actualizar angulos y lados si se calcularon
        if ctx["A"] != 0:
            angulo_a.value = f'{round(ctx["A"], 2)}'
        if ctx["B"] != 0:
            angulo_b.value = f'{round(ctx["B"], 2)}'
        if ctx["C"] != 0:
            angulo_c.value = f'{round(ctx["C"], 2)}'
        if ctx["a"] != 0:
            lado_a.value = f'{round(ctx["a"], 2)}'
        if ctx["b"] != 0:
            lado_b.value = f'{round(ctx["b"], 2)}'
        if ctx["c"] != 0:
            lado_c.value = f'{round(ctx["c"], 2)}'

        page.update()

    lados_angulos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=[lado_a, angulo_a], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[lado_b, angulo_b], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[lado_c, angulo_c], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[
                    ft.ElevatedButton("Calcular", on_click=calcular_click),
                    ft.ElevatedButton("Limpiar", on_click=Limpiar_triangulo),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]
        )
    )

    datos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=[area, perimetro, semiperimetro], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[altura_ha, altura_hb, altura_hc], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[Mediana_ma, Mediana_mb, Mediana_mc], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(controls=[inradio, circunradio], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
            ]
        )
    )

    column = ft.Column(
        controls=[
            controls.header_page(page),
            lados_angulos,
            datos,
        ],
        scroll=ft.ScrollMode.AUTO,
        width=page.width,
        height=page.height
    )

    content = ft.Row(
        controls=[column],
        scroll=ft.ScrollMode.ALWAYS,
        width=page.width
    )

    stack = ft.Stack(
        [
            controls.background(ft.Container),
            controls.containers(page),
            content,
        ], expand=True
    )

    def resized(e):
        column.width = page.width
        column.height = page.height
        content.width = page.width
        page.update()

    page.on_resized = resized

    return ft.View(
        "/Triangulo",
        [stack],
        padding=0,
    )

