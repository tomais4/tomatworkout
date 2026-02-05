import flet as ft
import datetime
import os

# --- CONFIGURAÇÕES VISUAIS ---
COR_FUNDO = "#121212"
COR_CARD = "#1E1E1E"
COR_PRIMARIA = "#536DFE"
COR_SECUNDARIA = "#333333"
COR_TEXTO = "#E0E0E0"
COR_TEXTO_DIM = "#9E9E9E"

TIPOS_SERIE = {
    "Normal": "blue", "TOP": "red", "BACK-OFF": "purple", 
    "ATÉ A FALHA": "orange", "FALHA + PARCIAL": "yellow", 
    "SEGURAR 2 SEG": "cyan", "FALHA + DROP": "pink"
}

# --- DADOS PADRÃO ---
TREINOS_PADRAO = {
    "A: EMPURRAR": [
        {"nome": "Supino Inclinado Halter", "series": [{"tipo": "TOP", "min": "6", "max": "9"}, {"tipo": "BACK-OFF", "min": "6", "max": "9"}]},
        {"nome": "Supino Máquina", "series": [{"tipo": "ATÉ A FALHA", "min": "8", "max": "12"}, {"tipo": "ATÉ A FALHA", "min": "8", "max": "12"}]},
        {"nome": "Elevação Lateral", "series": [{"tipo": "Normal", "min": "12", "max": "15"}, {"tipo": "Normal", "min": "12", "max": "15"}, {"tipo": "Normal", "min": "12", "max": "15"}]},
        {"nome": "Tríceps Testa", "series": [{"tipo": "ATÉ A FALHA", "min": "10", "max": "12"}, {"tipo": "ATÉ A FALHA", "min": "10", "max": "12"}]},
        {"nome": "Tríceps Francês", "series": [{"tipo": "Normal", "min": "8", "max": "10"}, {"tipo": "Normal", "min": "8", "max": "10"}]},
        {"nome": "Desenvolvimento Máq.", "series": [{"tipo": "Normal", "min": "8", "max": "10"}]}
    ],
    "B: PUXAR": [
        {"nome": "Puxada Alta Neutra", "series": [{"tipo": "TOP", "min": "8", "max": "10"}, {"tipo": "BACK-OFF", "min": "8", "max": "10"}]},
        {"nome": "Remada Apoiada", "series": [{"tipo": "ATÉ A FALHA", "min": "8", "max": "12"}, {"tipo": "ATÉ A FALHA", "min": "8", "max": "12"}]},
        {"nome": "Crucifixo Inverso", "series": [{"tipo": "Normal", "min": "12", "max": "15"}, {"tipo": "Normal", "min": "12", "max": "15"}, {"tipo": "Normal", "min": "12", "max": "15"}]},
        {"nome": "Rosca Scott", "series": [{"tipo": "FALHA + PARCIAL", "min": "8", "max": "12"}, {"tipo": "FALHA + PARCIAL", "min": "8", "max": "12"}]},
        {"nome": "Rosca Martelo", "series": [{"tipo": "ATÉ A FALHA", "min": "8", "max": "10"}, {"tipo": "ATÉ A FALHA", "min": "8", "max": "10"}]},
        {"nome": "Encolhimento", "series": [{"tipo": "SEGURAR 2 SEG", "min": "10", "max": "12"}, {"tipo": "SEGURAR 2 SEG", "min": "10", "max": "12"}]}
    ],
    "C: PERNAS": [
        {"nome": "Hack Squat / Leg 45", "series": [{"tipo": "TOP", "min": "5", "max": "8"}, {"tipo": "BACK-OFF", "min": "5", "max": "8"}]},
        {"nome": "Cadeira Extensora", "series": [{"tipo": "FALHA + DROP", "min": "10", "max": "15"}, {"tipo": "FALHA + DROP", "min": "10", "max": "15"}]},
        {"nome": "Mesa Flexora", "series": [{"tipo": "ATÉ A FALHA", "min": "8", "max": "10"}, {"tipo": "ATÉ A FALHA", "min": "8", "max": "10"}]},
        {"nome": "Cadeira Flexora", "series": [{"tipo": "FALHA + PARCIAL", "min": "10", "max": "12"}, {"tipo": "FALHA + PARCIAL", "min": "10", "max": "12"}]},
        {"nome": "Panturrilha Leg", "series": [{"tipo": "ATÉ A FALHA", "min": "10", "max": "15"}, {"tipo": "ATÉ A FALHA", "min": "10", "max": "15"}, {"tipo": "ATÉ A FALHA", "min": "10", "max": "15"}]},
        {"nome": "Cadeira Adutora", "series": [{"tipo": "ATÉ A FALHA", "min": "12", "max": "15"}, {"tipo": "ATÉ A FALHA", "min": "12", "max": "15"}]}
    ]
}

class BancoDeDados:
    def __init__(self, page: ft.Page):
        self.page = page
        self.carregar_dados()

    def carregar_dados(self):
        try:
            if self.page.client_storage.contains_key("gym_data"):
                self.dados = self.page.client_storage.get("gym_data")
            else:
                self.inicializar_padrao()
        except Exception as e:
            print(f"Erro ao ler memória: {e}")
            self.inicializar_padrao()

    def inicializar_padrao(self):
        self.dados = {"treinos_criados": TREINOS_PADRAO, "historico_log": []}
        self.salvar_dados()

    def salvar_dados(self):
        try:
            self.page.client_storage.set("gym_data", self.dados)
        except Exception as e:
            print(f"Erro ao salvar: {e}")

    def obter_ultimo(self, nome_ex, idx):
        try:
            historico = self.dados.get("historico_log", [])
            if not historico: return None
            for s in reversed(historico):
                if "exercicios" in s:
                    for e in s["exercicios"]:
                        if e["nome"] == nome_ex:
                            return e["series_realizadas"][idx]
        except: return None
        return None

def main(page: ft.Page):
    # --- CORREÇÃO DE CRASH ANDROID (LIFECYCLE) ---
    def handle_lifecycle(e):
        if e.data == "detach":
            os._exit(1)
    
    page.on_app_lifecycle_state_change = handle_lifecycle
    # ---------------------------------------------

    page.title = "Gym Ciencia Tomate"
    page.bgcolor = COR_FUNDO
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0
    
    db = BancoDeDados(page)

    def mudar_tela(destino, dados_extra=None):
        page.clean()
        if destino == "menu": menu()
        elif destino == "treinar": selecao()
        elif destino == "executar": executar(dados_extra)
        page.update()

    def menu():
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=40),
                    ft.Text("GYM CIENCIA TOMATE", size=26, weight="bold", color=COR_TEXTO, text_align="center"),
                    ft.Text("V25 - ANDROID FIX", color="green", weight="bold", size=14),
                    ft.Divider(color=COR_SECUNDARIA),
                    ft.Container(height=40),
                    ft.ElevatedButton(
                        "TREINAR AGORA", 
                        icon="play_arrow", 
                        color="white", 
                        bgcolor=COR_PRIMARIA, 
                        width=280, 
                        height=60, 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=lambda e: mudar_tela("treinar")
                    ),
                ], horizontal_alignment="center", alignment=ft.Alignment(0,0)),
                padding=20, expand=True, alignment=ft.Alignment(0,0)
            )
        )

    def selecao():
        treinos = db.dados.get("treinos_criados", {})
        col_treinos = ft.Column(horizontal_alignment="center", spacing=15)
        for t in treinos:
            btn = ft.Container(
                content=ft.Row([
                    ft.Text(t.split(":")[0], size=24, weight="bold", color=COR_PRIMARIA),
                    ft.Column([
                        ft.Text(t.split(":")[1].strip(), size=14, weight="bold", color="white"),
                        ft.Text("Toque para iniciar", size=10, color="grey")
                    ], spacing=2)
                ]),
                bgcolor=COR_CARD, padding=20, border_radius=15, width=320,
                on_click=lambda e, n=t: mudar_tela("executar", n), ink=True
            )
            col_treinos.controls.append(btn)

        page.add(
            ft.Column([
                ft.Container(height=20),
                ft.Text("ESCOLHER TREINO", size=20, color=COR_TEXTO, weight="bold"),
                ft.Divider(color=COR_SECUNDARIA),
                ft.Container(content=col_treinos, expand=True, padding=20),
                ft.TextButton("Voltar", on_click=lambda e: mudar_tela("menu"))
            ], horizontal_alignment="center", scroll="auto", expand=True)
        )

    def executar(nome):
        inputs = []
        lista_exercicios = ft.Column(scroll="auto", expand=True)
        
        for ex in db.dados["treinos_criados"][nome]:
            ex_container = ft.Column()
            ex_container.controls.append(ft.Text(ex['nome'], weight="bold", size=16, color=COR_TEXTO, max_lines=2, overflow="ellipsis"))
            
            series_in = []
            for idx, s in enumerate(ex['series']):
                h = db.obter_ultimo(ex['nome'], idx)
                c_val = str(h['carga']) if h else ""
                r_val = str(h['reps']) if h else ""
                
                tipo_serie = s.get('tipo', 'Normal')
                min_t = int(s.get('min', 6))
                max_t = int(s.get('max', 10))
                
                ic = ft.TextField(label="Kg", width=70, value=c_val, text_align="center", height=45, content_padding=5, text_size=14, border_color=COR_SECUNDARIA, keyboard_type="number")
                ir = ft.TextField(label="Reps", width=70, value=r_val, text_align="center", height=45, content_padding=5, text_size=14, border_color=COR_SECUNDARIA, keyboard_type="number")
                feedback = ft.Text("", size=11, weight="bold")

                def make_check(mn, mx, fb):
                    def check(e):
                        try:
                            val = int(e.control.value)
                            if val > mx: fb.value, fb.color = "⬆ CARGA", "green"
                            elif val < mn: fb.value, fb.color = "⬇ CARGA", "red"
                            else: fb.value, fb.color = "OK", "blue"
                            page.update()
                        except: pass
                    return check

                ir.on_change = make_check(min_t, max_t, feedback)
                series_in.append({"c": ic, "r": ir, "t": tipo_serie})
                
                cor = TIPOS_SERIE.get(tipo_serie, "white")
                linha = ft.Row([
                    ft.Container(width=10, height=10, bgcolor=cor, border_radius=5),
                    ft.Column([
                        ft.Text(f"{tipo_serie}", size=10, color=COR_TEXTO, no_wrap=True),
                        ft.Text(f"Meta: {min_t}-{max_t}", size=9, color=COR_TEXTO_DIM)
                    ], spacing=0, width=80),
                    ic, ir, feedback
                ], alignment="start", vertical_alignment="center")
                
                ex_container.controls.append(linha)
                ex_container.controls.append(ft.Container(height=8))
            
            inputs.append({"n": ex['nome'], "s": series_in})
            card = ft.Container(content=ex_container, bgcolor=COR_CARD, padding=15, border_radius=12, margin=ft.margin.only(bottom=10))
            lista_exercicios.controls.append(card)

        def finalizar(e):
            sessao = {"data": str(datetime.date.today()), "treino_nome": nome, "exercicios": [], "volume_total": 0}
            vol = 0
            for i in inputs:
                ex_data = {"nome": i["n"], "series_realizadas": []}
                for s in i["s"]:
                    try:
                        c, r = float(s["c"].value or 0), float(s["r"].value or 0)
                        vol += c * r
                        ex_data["series_realizadas"].append({"tipo": s["t"], "carga": c, "reps": r})
                    except: ex_data["series_realizadas"].append({"tipo": s["t"], "carga": 0, "reps": 0})
                sessao["exercicios"].append(ex_data)
            sessao["volume_total"] = vol
            
            db.dados["historico_log"].append(sessao)
            db.salvar_dados()
            
            # --- FIX COMPATIBILIDADE ---
            page.snack_bar = ft.SnackBar(ft.Text("Treino Salvo!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            # ---------------------------
            mudar_tela("menu")

        page.add(
            ft.Column([
                ft.Container(content=ft.Text(f"TREINANDO: {nome.split(':')[0]}", color=COR_PRIMARIA, weight="bold", size=18), padding=ft.padding.only(top=10, bottom=10), alignment=ft.Alignment(0,0)),
                lista_exercicios,
                ft.Container(content=ft.ElevatedButton("FINALIZAR TREINO", bgcolor=COR_PRIMARIA, color="white", width=300, height=50, on_click=finalizar), padding=20, alignment=ft.Alignment(0,0))
            ], expand=True)
        )

    menu()

ft.app(target=main)