import flet as ft
import flet.canvas as cv
import math

# Importar los controles reutilizables
from Models import Controls  


def main_triangulo(page: ft.Page) -> ft.View:
    page.title = "Resolución de Triángulo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 1000
    page.window.height = 700

    # --- UI controls ---
    lado_a = ft.TextField(label="Lado a", width=230, on_change=Controls.cambio_Textfield)
    lado_b = ft.TextField(label="Lado b", width=230, on_change=Controls.cambio_Textfield)
    lado_c = ft.TextField(label="Lado c", width=230, on_change=Controls.cambio_Textfield)
    angulo_A = ft.TextField(label="Ángulo A (°)", width=230, on_change=Controls.cambio_Textfield)
    angulo_B = ft.TextField(label="Ángulo B (°)", width=230, on_change=Controls.cambio_Textfield)
    angulo_C = ft.TextField(label="Ángulo C (°)", width=230, on_change=Controls.cambio_Textfield)

    area = ft.TextField(label="Área", disabled=True, width=160)
    perimetro = ft.TextField(label="Perímetro", disabled=True, width=160)
    semiperimetro = ft.TextField(label="Semiperímetro", disabled=True, width=160)
    altura_ha = ft.TextField(label="Altura ha", disabled=True, width=160)
    altura_hb = ft.TextField(label="Altura hb", disabled=True, width=160)
    altura_hc = ft.TextField(label="Altura hc", disabled=True, width=160)
    inradio = ft.TextField(label="Inradio", disabled=True, width=160)
    circunradio = ft.TextField(label="Circunradio", disabled=True, width=160)
    Mediana_ma = ft.TextField(label="Mediana ma", disabled=True, width=160)
    Mediana_mb = ft.TextField(label="Mediana mb", disabled=True, width=160)
    Mediana_mc = ft.TextField(label="Mediana mc", disabled=True, width=160)

    # Canvas
    canvas = cv.Canvas(width=520, height=520, shapes=[])
    canvas_container = ft.Container(
        content=canvas,
        width=520, height=520,
        border=ft.border.all(1, ft.Colors.BLUE_200),
        border_radius=8,
        bgcolor=ft.Colors.BLACK12
    )

    # Utilidades internas
    def clamp(x): return max(-1.0, min(1.0, x))

    def show_snack(msg):
        sb = ft.SnackBar(ft.Text(msg))
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def limpiar_todo(e=None):
        for fld in [lado_a, lado_b, lado_c, angulo_A, angulo_B, angulo_C,
                    area, perimetro, semiperimetro, altura_ha, altura_hb, altura_hc,
                    inradio, circunradio, Mediana_ma, Mediana_mb, Mediana_mc]:
            fld.value = ""
        canvas.shapes.clear()
        canvas.update()
        page.update()

    def dibujar_triangulo(a, b, c, A_deg, B_deg, C_deg):
        if a <= 0 or b <= 0 or c <= 0:
            return
        canvas.shapes.clear()
        max_lado = max(a, b, c)
        escala = 380 / max_lado
        ax, ay = 60, 480
        bx, by = ax + c * escala, ay
        A_rad = math.radians(A_deg)
        cx = ax + b * escala * math.cos(A_rad)
        cy = ay - b * escala * math.sin(A_rad)

        # Dibujar lados
        for (x1, y1, x2, y2) in [(ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay)]:
            canvas.shapes.append(cv.Line(
                x1, y1, x2, y2,
                paint=ft.Paint(stroke_width=3, color=ft.Colors.BLUE_700, style=ft.PaintingStyle.STROKE)
            ))

        # Vértices
        for px, py in [(ax, ay), (bx, by), (cx, cy)]:
            canvas.shapes.append(cv.Circle(
                px, py, 4,
                paint=ft.Paint(color=ft.Colors.RED_700, style=ft.PaintingStyle.FILL)
            ))
        canvas.update()

    # --- Cálculo principal ---
    def calcular_click(e):
        def parse(f):
            try:
                return float(f.value) if f.value not in ("", None) else 0.0
            except:
                return 0.0

        ctx = {
            "a": parse(lado_a),
            "b": parse(lado_b),
            "c": parse(lado_c),
            "A": parse(angulo_A),
            "B": parse(angulo_B),
            "C": parse(angulo_C),
        }

        # Counters
        lados_known = sum(1 for k in ("a","b","c") if ctx[k] > 0)
        ang_known = sum(1 for k in ("A","B","C") if ctx[k] > 0)

        # basic validation
        if lados_known + ang_known < 3:
            show_snack("Ingresar al menos 3 datos (combinación válida: SSS, SAS, ASA, AAS, SSA).")
            return

        # --- Helper solvers ---
        def law_of_cos_for_angle(opposite, side1, side2):
            denom = 2 * side1 * side2
            if denom == 0:
                return 0.0
            val = (side1*side1 + side2*side2 - opposite*opposite) / denom
            val = clamp(val)
            return math.degrees(math.acos(val))

        def law_of_cos_for_side(side1, side2, included_angle_deg):
            return math.sqrt(side1*side1 + side2*side2 - 2*side1*side2*math.cos(math.radians(included_angle_deg)))

        def law_of_sines_find_angle(known_side, known_angle_deg, target_side):
            denom = known_side
            if denom == 0:
                return 0.0
            ratio = (target_side * math.sin(math.radians(known_angle_deg))) / denom
            ratio = clamp(ratio)
            try:
                ang = math.degrees(math.asin(ratio))
                return ang
            except Exception:
                return 0.0

        # Attempt to solve progressively using standard cases
        changed = True
        iter_count = 0
        ambiguous_alert = False
        while changed and iter_count < 15:
            changed = False
            iter_count += 1

            # If three sides known -> compute all angles (SSS)
            if sum(1 for k in ("a","b","c") if ctx[k] > 0) == 3:
                if ctx["A"] == 0:
                    ctx["A"] = law_of_cos_for_angle(ctx["a"], ctx["b"], ctx["c"])
                    changed = True
                if ctx["B"] == 0:
                    ctx["B"] = law_of_cos_for_angle(ctx["b"], ctx["a"], ctx["c"])
                    changed = True
                if ctx["C"] == 0:
                    ctx["C"] = 180.0 - ctx["A"] - ctx["B"]
                    changed = True

            # SAS: two sides and included angle -> compute opposite side
            if ctx["A"] > 0 and ctx["b"] > 0 and ctx["c"] > 0 and ctx["a"] == 0:
                ctx["a"] = law_of_cos_for_side(ctx["b"], ctx["c"], ctx["A"]); changed = True
            if ctx["B"] > 0 and ctx["a"] > 0 and ctx["c"] > 0 and ctx["b"] == 0:
                ctx["b"] = law_of_cos_for_side(ctx["a"], ctx["c"], ctx["B"]); changed = True
            if ctx["C"] > 0 and ctx["a"] > 0 and ctx["b"] > 0 and ctx["c"] == 0:
                ctx["c"] = law_of_cos_for_side(ctx["a"], ctx["b"], ctx["C"]); changed = True

            # ASA/AAS: two angles known -> third angle and law of sines for sides
                if sum(1 for k in ("A","B","C") if ctx[k] > 0) >= 2:
                    if ctx["A"] == 0:
                        ctx["A"] = 180.0 - (ctx.get("B",0)+ctx.get("C",0)); changed = True
                    if ctx["B"] == 0:
                        ctx["B"] = 180.0 - (ctx.get("A",0)+ctx.get("C",0)); changed = True
                    if ctx["C"] == 0:
                        ctx["C"] = 180.0 - (ctx.get("A",0)+ctx.get("B",0)); changed = True
                    # now use law of sines to get sides if at least one side known
                    if ctx["a"] > 0 and ctx["A"] > 0:
                        if ctx["b"] == 0 and ctx["B"] > 0:
                            ctx["b"] = (ctx["a"] * math.sin(math.radians(ctx["B"]))) / math.sin(math.radians(ctx["A"])); changed = True
                        if ctx["c"] == 0 and ctx["C"] > 0:
                            ctx["c"] = (ctx["a"] * math.sin(math.radians(ctx["C"]))) / math.sin(math.radians(ctx["A"])); changed = True
                    if ctx["b"] > 0 and ctx["B"] > 0:
                        if ctx["a"] == 0 and ctx["A"] > 0:
                            ctx["a"] = (ctx["b"] * math.sin(math.radians(ctx["A"]))) / math.sin(math.radians(ctx["B"])); changed = True
                        if ctx["c"] == 0 and ctx["C"] > 0:
                            ctx["c"] = (ctx["b"] * math.sin(math.radians(ctx["C"]))) / math.sin(math.radians(ctx["B"])); changed = True
                    if ctx["c"] > 0 and ctx["C"] > 0:
                        if ctx["a"] == 0 and ctx["A"] > 0:
                            ctx["a"] = (ctx["c"] * math.sin(math.radians(ctx["A"]))) / math.sin(math.radians(ctx["C"])); changed = True
                        if ctx["b"] == 0 and ctx["B"] > 0:
                            ctx["b"] = (ctx["c"] * math.sin(math.radians(ctx["B"]))) / math.sin(math.radians(ctx["C"])); changed = True
    
                # SSA (ambiguous) - try to resolve using law of sines
                # Example: given a and A, find B from b: sin(B) = b*sin(A)/a
                # We'll check possible supplements
                # Solve for each unknown angle via known pair
                for known_side, known_angle, target_side, target_key in [
                    ("a","A","b","B"),
                    ("a","A","c","C"),
                    ("b","B","a","A"),
                    ("b","B","c","C"),
                    ("c","C","a","A"),
                    ("c","C","b","B"),
                ]:
                    ks = ctx.get(known_side,0); ka = ctx.get(known_angle,0); ts = ctx.get(target_side,0)
                    if ks > 0 and ka > 0 and ts > 0 and ctx.get(target_key,0) == 0:
                        denom = ks
                        ratio = (ts * math.sin(math.radians(ka))) / denom
                        if ratio < -1 or ratio > 1:
                            # impossible for this relation; skip
                            continue
                        # principal solution
                        ang_candidate = math.degrees(math.asin(clamp(ratio)))
                        # check ambiguous supplement (180 - ang_candidate) if it fits the triangle
                        other = 180.0 - ang_candidate
                        # pick one that makes sense with sum < 180 with the third angle (if available)
                        third_angle = 180.0 - (ka + ang_candidate)
                        third_angle_other = 180.0 - (ka + other)
                        # prefer principal, but detect ambiguity
                        ctx[target_key] = ang_candidate
                        changed = True
                        # if both possible (both positive third angles), mark ambiguous
                        if third_angle > 0 and third_angle_other > 0 and abs(third_angle - third_angle_other) > 1e-6:
                            ambiguous_alert = True
    
                # Recompute sum-of-angles if any two available
                if sum(1 for k in ("A","B","C") if ctx[k] > 0) >= 2:
                    if ctx["A"] == 0:
                        ctx["A"] = 180.0 - ctx.get("B",0) - ctx.get("C",0); changed = True
                    if ctx["B"] == 0:
                        ctx["B"] = 180.0 - ctx.get("A",0) - ctx.get("C",0); changed = True
                    if ctx["C"] == 0:
                        ctx["C"] = 180.0 - ctx.get("A",0) - ctx.get("B",0); changed = True
    
            # end while
    
            if ambiguous_alert:
                show_snack("Caso SSA ambiguo detectado: podría haber dos soluciones. Se eligió la solución principal.")
    
            # Basic final validation: triangle inequality for sides
            if ctx["a"] <= 0 or ctx["b"] <= 0 or ctx["c"] <= 0:
                show_snack("No se pudieron obtener los 3 lados. Verifica los datos ingresados.")
                # still update what we have
            else:
                # triangle inequality
                if not (ctx["a"] + ctx["b"] > ctx["c"] and ctx["a"] + ctx["c"] > ctx["b"] and ctx["b"] + ctx["c"] > ctx["a"]):
                    show_snack("La desigualdad triangular no se cumple con los lados calculados. Datos inválidos.")
    
            # Compute semiperimeter, perimeter, area (Heron), inradius, circumradius, heights, medians
            try:
                per = 0.0
                if ctx["a"]>0 and ctx["b"]>0 and ctx["c"]>0:
                    per = ctx["a"] + ctx["b"] + ctx["c"]
                    s = per/2.0
                    semiper = s
                    semiperimetro.value = f"{round(semiper,2)}"
                    perimetro.value = f"{round(per,2)}"
                    # Heron
                    val = s*(s-ctx["a"])*(s-ctx["b"])*(s-ctx["c"])
                    if val >= 0:
                        ar = math.sqrt(val)
                        ctx["area"] = ar
                        area.value = f"{round(ar,2)}"
                    else:
                        ctx["area"] = 0.0
                        area.value = ""
                else:
                    semiperimetro.value = ""
                    perimetro.value = ""
                    area.value = ""
            except Exception:
                area.value = ""
                perimetro.value = ""
                semiperimetro.value = ""
    
            # heights from area
            try:
                ar = ctx.get("area",0.0)
                if ar > 0:
                    ha = (2*ar)/ctx["a"] if ctx["a"]>0 else 0.0
                    hb = (2*ar)/ctx["b"] if ctx["b"]>0 else 0.0
                    hc = (2*ar)/ctx["c"] if ctx["c"]>0 else 0.0
                    altura_ha.value = f"{round(ha,2)}" if ha>0 else ""
                    altura_hb.value = f"{round(hb,2)}" if hb>0 else ""
                    altura_hc.value = f"{round(hc,2)}" if hc>0 else ""
                else:
                    altura_ha.value = altura_hb.value = altura_hc.value = ""
            except Exception:
                altura_ha.value = altura_hb.value = altura_hc.value = ""
    
            # inradius and circumradius
            try:
                if ctx.get("area",0) > 0 and semiperimetro.value != "":
                    s = float(semiperimetro.value)
                    ir = ctx["area"]/s if s>0 else 0.0
                    inradio.value = f"{round(ir,2)}" if ir>0 else ""
                else:
                    inradio.value = ""
                if ctx.get("area",0) > 0 and ctx["a"]>0 and ctx["b"]>0 and ctx["c"]>0:
                    cr = (ctx["a"]*ctx["b"]*ctx["c"]) / (4*ctx["area"])
                    circunradio.value = f"{round(cr,2)}" if cr>0 else ""
                else:
                    circunradio.value = ""
            except Exception:
                inradio.value = ""
                circunradio.value = ""
    
            # medians
            def med(l1,l2,op):
                try:
                    return 0.5*math.sqrt(2*l1*l1 + 2*l2*l2 - op*op)
                except Exception:
                    return 0.0
            ma = med(ctx["b"], ctx["c"], ctx["a"]) if ctx["b"]>0 and ctx["c"]>0 else 0.0
            mb = med(ctx["a"], ctx["c"], ctx["b"]) if ctx["a"]>0 and ctx["c"]>0 else 0.0
            mc = med(ctx["a"], ctx["b"], ctx["c"]) if ctx["a"]>0 and ctx["b"]>0 else 0.0
            Mediana_ma.value = f"{round(ma,2)}" if ma>0 else ""
            Mediana_mb.value = f"{round(mb,2)}" if mb>0 else ""
            Mediana_mc.value = f"{round(mc,2)}" if mc>0 else ""
    
            # Update angle fields nicely
            if ctx.get("A",0)>0: angulo_A.value = f"{round(ctx['A'],2)}"
            if ctx.get("B",0)>0: angulo_B.value = f"{round(ctx['B'],2)}"
            if ctx.get("C",0)>0: angulo_C.value = f"{round(ctx['C'],2)}"
            # Update side fields nicely
            if ctx.get("a",0)>0: lado_a.value = f"{round(ctx['a'],2)}"
            if ctx.get("b",0)>0: lado_b.value = f"{round(ctx['b'],2)}"
            if ctx.get("c",0)>0: lado_c.value = f"{round(ctx['c'],2)}"
    
            # draw triangle if enough info
            if ctx.get("a",0)>0 and ctx.get("b",0)>0 and ctx.get("c",0)>0 and ctx.get("A",0)>0:
                dibujar_triangulo(ctx["a"], ctx["b"], ctx["c"], ctx["A"], ctx["B"], ctx["C"])
    
            page.update()

    # Interfaz
    header = Controls.header_page(page)

    left_col = ft.Column(
        controls=[
            ft.Row(controls=[lado_a, angulo_A]),
            ft.Row(controls=[lado_b, angulo_B]),
            ft.Row(controls=[lado_c, angulo_C]),
            Controls.Buttons(None, calcular_click, limpiar_todo),
            ft.Row(controls=[area, perimetro, semiperimetro]),
            ft.Row(controls=[altura_ha, altura_hb, altura_hc]),
            ft.Row(controls=[Mediana_ma, Mediana_mb, Mediana_mc]),
            ft.Row(controls=[inradio, circunradio]),
        ],
        spacing=10,
        width=430,
        scroll=ft.ScrollMode.AUTO
    )

    body = ft.Row(
        controls=[left_col, canvas_container],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    content = ft.Column(
        controls=[header, body],
        expand=True
    )

    return ft.View("/Triangulo", [content], padding=0)


def main(page: ft.Page):
    view = main_triangulo(page)
    page.views.append(view)
    page.update()


if __name__ == "__main__":
    try:
        ft.app(main)
    except Exception as ex:
        print("Error al iniciar la app:", ex)