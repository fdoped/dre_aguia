import streamlit as st
import pandas as pd
import os

# ✅ set_page_config PRIMEIRO, antes de qualquer outro st.*
st.set_page_config(
    page_title="DRE Gerencial",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)




st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ── Oculta elementos nativos do Streamlit ─── */
#MainMenu {visibility: hidden !important;}
header[data-testid="stHeader"] {visibility: hidden !important; height: 0 !important;}
footer {visibility: hidden !important;}

.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

iframe {
    width: 100% !important;
    min-width: 100% !important;
    background: var(--c-bg-3,#060D1A) !important;
    border-radius: 10px !important;
}

/* ── Midnight Pro — fundo escuro global ─── */
.stApp, .stApp > header, .main, .main > div {
    background-color: var(--c-bg-3,#060D1A) !important;
}

/* ── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: var(--c-bg-2,#0A1628) !important;
    border-right: 1px solid var(--c-border-1,#1A2E4A) !important;
}
[data-testid="stSidebar"] * { color: var(--c-text-2b,#8FAEC8) !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] h1 { 
    color: var(--c-text-1,#E2E8F0) !important; font-family:system-ui, -apple-system, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif !important;
    font-size: 1.1rem !important; font-weight: 700 !important; letter-spacing: 0.05em !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--c-text-1,#C8D9E9) !important; font-family:system-ui, -apple-system, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: var(--c-text-2b,#8FAEC8) !important; font-size: 0.8rem !important; font-weight: 500 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--c-text-2,#A0B8CC) !important; font-weight: 600 !important; font-size: 0.78rem !important; }

/* Sidebar widgets */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: var(--c-bg-5,#0F1F35) !important;
    border-color: var(--c-border-1,#1E3550) !important;
    color: var(--c-text-1b,#CBD5E1) !important;
    border-radius: 7px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="input"] input { color: var(--c-text-1b,#CBD5E1) !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: var(--c-border-2,#1A3A5C) !important;
    border-radius: 5px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: var(--c-accent-bright,#7DD3FC) !important; font-size: 0.72rem !important; }

/* Toggle */
[data-testid="stToggle"] label { color: var(--c-text-2b,#8FAEC8) !important; }
[data-testid="stToggle"] [data-checked="true"] { background: var(--c-accent,#2563EB) !important; }

/* Botão */
[data-testid="stSidebar"] button {
    background: var(--c-bg-4,#0F2540) !important;
    border: 1px solid var(--c-border-2,#1E3A5A) !important;
    color: var(--c-accent-bright,#7DD3FC) !important;
    border-radius: 7px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] button:hover {
    background: var(--c-bg-4,#163354) !important;
    border-color: var(--c-accent,#3B82F6) !important;
    color: var(--c-accent-bright,#BAE6FD) !important;
}

/* Divider */
[data-testid="stSidebar"] hr { border-color: var(--c-border-1,#1A2E4A) !important; margin: 10px 0 !important; }

/* Metric na sidebar */
[data-testid="stSidebar"] [data-testid="metric-container"] {
    background: var(--c-bg-5,#0F1F35) !important;
    border: 1px solid var(--c-border-2,#1A3050) !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
}
[data-testid="stSidebar"] [data-testid="metric-container"] [data-testid="stMetricLabel"] p { color: var(--c-text-3,#7B9BBB) !important; font-size: 0.72rem !important; }
[data-testid="stSidebar"] [data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--c-text-1,#E2E8F0) !important; font-size: 1rem !important; font-family: 'Inter', sans-serif !important; }

/* Main content text */
.stMarkdown p, .stText, h1, h2, h3 { color: var(--c-text-1,#E2E8F0) !important; }

/* Cabeçalho principal */
h2[style*="0A2342"], h2[style*="Inter"] { font-family:system-ui, -apple-system, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif !important; }

/* Warning/error boxes */
[data-testid="stAlert"] {
    background: var(--c-bg-5,#0F1F35) !important;
    border-left: 3px solid var(--c-warning,#F59E0B) !important;
    color: var(--c-warning,#FCD34D) !important;
    border-radius: 6px !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--c-accent,#3B82F6) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ESTRUTURA DO DRE
# ─────────────────────────────────────────────────────────────────────────────
ESTRUTURA_DRE = [
    ("VENDA BRUTA",                                "Venda Bruta",                   +1),
    ("(-) Comissão sobre Vendas",                  "(-) Comissões sobre Vendas",    -1),
    ("(-) Custo das Vendas",                       "(-) Custo das Vendas",          -1),
    ("(+) Reembolso de Custos",                    "(+) Reembolso de Custos",       +1),
    ("Impostos Incidentes s/ Receita Tributável",  "(-) Impostos s/ Receita",       -1),
    ("Despesas Administrativa, Comercial e Mkt",   "(-) Despesas Operacionais",     -1),
    ("(+) Receitas Financeiras",                   "(+) Receitas Financeiras",      +1),
    ("(-) Despesas Financeiras",                   "(-) Despesas Financeiras",      -1),
    ("INVESTIMENTOS",                              "(-) Investimentos",             -1),
]

SUBTOTAIS = {
    "(-) Comissão sobre Vendas":                 ("Venda Líquida",                      False),
    "(+) Reembolso de Custos":                   ("Margem de Contribuição / Lucro Bruto",False),
    "Impostos Incidentes s/ Receita Tributável": ("Receita Líquida",                    True),
    "Despesas Administrativa, Comercial e Mkt":  ("Resultado Operacional (EBITDA)",     False),
    "(-) Despesas Financeiras":                  ("Resultado Antes de Investimentos",   False),
    "INVESTIMENTOS":                             ("Resultado Líquido do Exercício",     False),
}

# Separador de seção antes de cada categoria
SECOES = {
    "VENDA BRUTA":                               "RECEITAS OPERACIONAIS",
    "(-) Custo das Vendas":                      "CUSTOS",
    "Impostos Incidentes s/ Receita Tributável": "IMPOSTOS",
    "Despesas Administrativa, Comercial e Mkt":  "DESPESAS OPERACIONAIS",
    "(+) Receitas Financeiras":                  "RESULTADO FINANCEIRO",
}

FORA_DRE = "Movimentações de Caixa"

MESES_PT    = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",
               7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
MESES_CURTO = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
               7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# ─────────────────────────────────────────────────────────────────────────────
# MAPEAMENTO
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_mapping(path: str, _mtime: float = 0) -> dict:
    if not os.path.exists(path):
        return {}
    mp = pd.read_excel(path, sheet_name="Mapeamento")
    mp["tipo_documento"] = mp["tipo_documento"].astype(str).str.strip()
    mp["cp_ms"]          = mp["cp_ms"].astype(str).str.strip()
    mp["categoria_dre"]  = mp["categoria_dre"].astype(str).str.strip()
    mp["sinal"]          = pd.to_numeric(mp["sinal"], errors="coerce").fillna(-1).astype(int)
    return {(r.tipo_documento, r.cp_ms): (r.categoria_dre, int(r.sinal))
            for _, r in mp.iterrows()}


def aplicar_mapping(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    if not mapping:
        df = df.copy(); df["sinal"] = -1; return df
    SEP = "|||"
    map_dre_exact, map_sig_exact, map_dre_star, map_sig_star = {}, {}, {}, {}
    for (td, cpm), (cat, sig) in mapping.items():
        if cpm == "*":
            map_dre_star[td] = cat; map_sig_star[td] = sig
        else:
            k = td + SEP + cpm
            map_dre_exact[k] = cat; map_sig_exact[k] = sig

    # Garante dtype object puro — parquet pandas2+ usa StringDtype/ArrowDtype
    # que nao aceita NaN float nas operacoes de atribuicao por mascara booleana
    td_col  = df["Tipo_Documento"].astype(object).astype(str)
    cpm_col = df["cp_ms"].astype(object).astype(str)
    dre_col = df["dre"].astype(object).astype(str)

    key_col   = td_col + SEP + cpm_col
    new_dre   = key_col.map(map_dre_exact).astype(object)
    new_sinal = key_col.map(map_sig_exact).astype(object)

    no_match = new_dre.isna()
    if no_match.any():
        new_dre[no_match]   = td_col[no_match].map(map_dre_star)
        new_sinal[no_match] = td_col[no_match].map(map_sig_star)

    null2 = new_dre.isna()
    if null2.any():
        new_dre[null2]   = dre_col[null2]
        new_sinal[null2] = -1

    df = df.copy()
    df["dre"]   = new_dre.values
    df["sinal"] = pd.to_numeric(new_sinal, errors="coerce").fillna(-1).astype(int).values
    return df

# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DADOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(xlsx_path: str, parquet_path: str) -> pd.DataFrame:
    # Detecta aba automaticamente (DRE, Planilha1, Sheet1 ou a primeira disponível)
    def _get_sheet(path):
        sheets = pd.ExcelFile(path).sheet_names
        return next((s for s in sheets if s in ("DRE","Planilha1","Sheet1","Base")), sheets[0])

    # Valida parquet existente: verifica colunas e presença do orçamento
    _parquet_ok = False
    if os.path.exists(parquet_path) and os.path.getmtime(parquet_path) >= os.path.getmtime(xlsx_path):
        try:
            df = pd.read_parquet(parquet_path)
            colunas_ok = {"cp_ms","dre","valor_real_quitado","valor_real_aberto"}.issubset(df.columns)
            tem_orc_parquet = df["cp_ms"].astype(str).str.strip().eq("Orcamento").any()
            df_ck = pd.read_excel(xlsx_path, sheet_name=_get_sheet(xlsx_path),
                                  usecols=["cp_ms"], nrows=1000)
            tem_orc_excel = df_ck["cp_ms"].astype(str).str.strip().eq("Orcamento").any()
            _parquet_ok = colunas_ok and (tem_orc_parquet or not tem_orc_excel)
        except Exception:
            _parquet_ok = False

    if not _parquet_ok:
        if os.path.exists(parquet_path):
            os.remove(parquet_path)
        df = pd.read_excel(xlsx_path, sheet_name=_get_sheet(xlsx_path))
        # Converte colunas não-numéricas/não-datetime para str antes do parquet
        for col in df.columns:
            if df[col].dtype.kind not in ("i", "u", "f", "M"):
                try:
                    df[col] = df[col].astype(str)
                except Exception:
                    df[col] = df[col].apply(lambda x: "" if x is None else str(x))
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)
        df.to_parquet(parquet_path, index=False, engine="pyarrow")

    for col in ["dre","Grupo","SubGrupo","Tipo_Documento","Empresa","cp_ms"]:
        if col in df.columns:
            # Converte StringDtype/ArrowDtype para object puro — pandas 2+ salva parquet
            # com StringDtype que nao aceita NaN float nas operacoes de .map() do aplicar_mapping
            df[col] = df[col].astype(object).astype(str).str.strip().replace("nan","Sem Classificacao")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["Ano"]  = df["data"].dt.year.astype("Int64")
    df["Mes"]  = df["data"].dt.month.astype("Int64")
    for col in ("valor_real_quitado","valor_real_aberto"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["valor_total"] = df["valor_real_quitado"] + df["valor_real_aberto"]
    return df


# ─────────────────────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────────────────────
diretorio    = os.path.dirname(os.path.abspath(__file__))
xlsx_path    = os.path.join(diretorio, "Base_1805 CSC Abril (Orc).xlsx")
parquet_path = xlsx_path.replace(".xlsx", ".parquet")
mapping_path = os.path.join(diretorio, "mapeamento_td.xlsx")

# ─────────────────────────────────────────────────────────────────────────────
# TEMAS — paletas claras e escuras intercambiáveis
# Cada tema define os mesmos 28 tokens. O CSS principal usa var(--token, fallback);
# a função abaixo gera o bloco :root { } com os valores do tema escolhido.
# ─────────────────────────────────────────────────────────────────────────────
TEMAS = {
    "Command Center (atual)": {
        "kind": "dark",
        "c-bg-1": "#080F1C", "c-bg-2": "#0A1628", "c-bg-3": "#060D1A",
        "c-bg-4": "#0F1E30", "c-bg-5": "#0C1828",
        "c-border-1": "#1A2E4A", "c-border-2": "#1A3050",
        "c-text-1": "#E2E8F0", "c-text-1b": "#CBD5E1",
        "c-text-2": "#94A3B8", "c-text-2b": "#8FAEC8",
        "c-text-3": "#607A90", "c-text-3b": "#3D6080", "c-text-3c": "#4A7090",
        "c-text-3d": "#4A6680", "c-text-3e": "#475569", "c-text-3f": "#64748B",
        "c-text-4": "#2A5080", "c-text-4b": "#2A4560",
        "c-text-4c": "#2A4060", "c-text-4d": "#3D5A78",
        "c-accent": "#3B82F6", "c-accent-bright": "#7DD3FC",
        "c-success": "#22C55E", "c-warning": "#F59E0B", "c-danger": "#EF4444",
        "font-mono": "'JetBrains Mono', 'Fira Code', Menlo, ui-monospace, monospace",
        "font-sans": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    },
    "Carbon Terminal": {
        "kind": "dark",
        "c-bg-1": "#0F0F0F", "c-bg-2": "#161616", "c-bg-3": "#0A0A0A",
        "c-bg-4": "#1F1F1F", "c-bg-5": "#161616",
        "c-border-1": "#262626", "c-border-2": "#393939",
        "c-text-1": "#F4F4F4", "c-text-1b": "#E0E0E0",
        "c-text-2": "#C6C6C6", "c-text-2b": "#A8A8A8",
        "c-text-3": "#8D8D8D", "c-text-3b": "#8D8D8D", "c-text-3c": "#A8A8A8",
        "c-text-3d": "#8D8D8D", "c-text-3e": "#6F6F6F", "c-text-3f": "#A8A8A8",
        "c-text-4": "#6F6F6F", "c-text-4b": "#525252",
        "c-text-4c": "#393939", "c-text-4d": "#6F6F6F",
        "c-accent": "#4589FF", "c-accent-bright": "#78A9FF",
        "c-success": "#42BE65", "c-warning": "#F1C21B", "c-danger": "#FA4D56",
        "font-mono": "'IBM Plex Mono', 'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "'IBM Plex Sans', 'Inter', -apple-system, sans-serif",
    },
    "Aurora": {
        "kind": "dark",
        "c-bg-1": "#0A0A0F", "c-bg-2": "#131320", "c-bg-3": "#070710",
        "c-bg-4": "#1A1A2E", "c-bg-5": "#0E0E18",
        "c-border-1": "#1F1F2E", "c-border-2": "#2A2A45",
        "c-text-1": "#F4F4F8", "c-text-1b": "#E2E2EE",
        "c-text-2": "#A8A8C8", "c-text-2b": "#9090B5",
        "c-text-3": "#8B8BA8", "c-text-3b": "#7878A0", "c-text-3c": "#9090B5",
        "c-text-3d": "#7878A0", "c-text-3e": "#666688", "c-text-3f": "#8B8BA8",
        "c-text-4": "#5A5A78", "c-text-4b": "#454560",
        "c-text-4c": "#353550", "c-text-4d": "#5A5A78",
        "c-accent": "#A78BFA", "c-accent-bright": "#5EEAD4",
        "c-success": "#5EEAD4", "c-warning": "#FBBF24", "c-danger": "#F472B6",
        "font-mono": "'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    },
    "Monochrome Zinc": {
        "kind": "dark",
        "c-bg-1": "#18181B", "c-bg-2": "#1F1F22", "c-bg-3": "#101013",
        "c-bg-4": "#27272A", "c-bg-5": "#1F1F22",
        "c-border-1": "#27272A", "c-border-2": "#3F3F46",
        "c-text-1": "#FAFAFA", "c-text-1b": "#E4E4E7",
        "c-text-2": "#D4D4D8", "c-text-2b": "#A1A1AA",
        "c-text-3": "#A1A1AA", "c-text-3b": "#71717A", "c-text-3c": "#A1A1AA",
        "c-text-3d": "#71717A", "c-text-3e": "#52525B", "c-text-3f": "#A1A1AA",
        "c-text-4": "#52525B", "c-text-4b": "#3F3F46",
        "c-text-4c": "#27272A", "c-text-4d": "#52525B",
        "c-accent": "#E4E4E7", "c-accent-bright": "#FAFAFA",
        "c-success": "#A1A1AA", "c-warning": "#D4D4D8", "c-danger": "#71717A",
        "font-mono": "'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    },
    "Midnight Glass": {
        "kind": "dark",
        "c-bg-1": "#0F0F1E", "c-bg-2": "#1A1A35", "c-bg-3": "#050511",
        "c-bg-4": "#1E1B4B", "c-bg-5": "#15152A",
        "c-border-1": "rgba(255,255,255,.08)", "c-border-2": "rgba(255,255,255,.14)",
        "c-text-1": "#FFFFFF", "c-text-1b": "#EDEDFF",
        "c-text-2": "#C4C4E8", "c-text-2b": "#A8A8D0",
        "c-text-3": "#8B8BC8", "c-text-3b": "#7878B5", "c-text-3c": "#9090C0",
        "c-text-3d": "#7878B5", "c-text-3e": "#5A5A88", "c-text-3f": "#8B8BC8",
        "c-text-4": "#6B6B9E", "c-text-4b": "#525275",
        "c-text-4c": "#3A3A55", "c-text-4d": "#6B6B9E",
        "c-accent": "#67E8F9", "c-accent-bright": "#C4F1F9",
        "c-success": "#67E8F9", "c-warning": "#FCD34D", "c-danger": "#FB7185",
        "font-mono": "'SF Mono', 'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "-apple-system, 'SF Pro Display', 'Inter', sans-serif",
    },
    "Forest (GitHub dark)": {
        "kind": "dark",
        "c-bg-1": "#0D1117", "c-bg-2": "#161B22", "c-bg-3": "#010409",
        "c-bg-4": "#21262D", "c-bg-5": "#161B22",
        "c-border-1": "#21262D", "c-border-2": "#30363D",
        "c-text-1": "#E6EDF3", "c-text-1b": "#C9D1D9",
        "c-text-2": "#C9D1D9", "c-text-2b": "#8B949E",
        "c-text-3": "#7D8590", "c-text-3b": "#6E7681", "c-text-3c": "#8B949E",
        "c-text-3d": "#6E7681", "c-text-3e": "#484F58", "c-text-3f": "#7D8590",
        "c-text-4": "#484F58", "c-text-4b": "#30363D",
        "c-text-4c": "#21262D", "c-text-4d": "#484F58",
        "c-accent": "#58A6FF", "c-accent-bright": "#79C0FF",
        "c-success": "#3FB950", "c-warning": "#D29922", "c-danger": "#F85149",
        "font-mono": "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, monospace",
        "font-sans": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "Blood Moon": {
        "kind": "dark",
        "c-bg-1": "#0C0606", "c-bg-2": "#160A0A", "c-bg-3": "#080404",
        "c-bg-4": "#1A0808", "c-bg-5": "#120606",
        "c-border-1": "#2D0F0F", "c-border-2": "#4A1818",
        "c-text-1": "#FFD9D9", "c-text-1b": "#FFB8B8",
        "c-text-2": "#D4A4A4", "c-text-2b": "#B58585",
        "c-text-3": "#8B5959", "c-text-3b": "#704545", "c-text-3c": "#8B5959",
        "c-text-3d": "#704545", "c-text-3e": "#5C3838", "c-text-3f": "#8B5959",
        "c-text-4": "#6B2929", "c-text-4b": "#4A1818",
        "c-text-4c": "#2D0F0F", "c-text-4d": "#6B2929",
        "c-accent": "#FF8E8E", "c-accent-bright": "#FFB8B8",
        "c-success": "#5EEAA0", "c-warning": "#FBBF24", "c-danger": "#E04545",
        "font-mono": "'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    },
    "Executive Premium (light)": {
        "kind": "light",
        "c-bg-1": "#FBF8F0", "c-bg-2": "#FFFFFF", "c-bg-3": "#F3EFE3",
        "c-bg-4": "#F9F6EC", "c-bg-5": "#FAF6E8",
        "c-border-1": "#E5DCC0", "c-border-2": "#C8B98E",
        "c-text-1": "#1E3A5F", "c-text-1b": "#2D4A6F",
        "c-text-2": "#2D2D2D", "c-text-2b": "#3D3D3D",
        "c-text-3": "#5A5A5A", "c-text-3b": "#6A6A6A", "c-text-3c": "#5A5A5A",
        "c-text-3d": "#6A6A6A", "c-text-3e": "#7A7A7A", "c-text-3f": "#5A5A5A",
        "c-text-4": "#8A8A8A", "c-text-4b": "#A0A0A0",
        "c-text-4c": "#B8B8B8", "c-text-4d": "#8A8A8A",
        "c-accent": "#1E3A5F", "c-accent-bright": "#B8860B",
        "c-success": "#1E7548", "c-warning": "#B8860B", "c-danger": "#8B1A1A",
        "font-mono": "'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "Georgia, 'Times New Roman', serif",
    },
    "Modern SaaS (light)": {
        "kind": "light",
        "c-bg-1": "#F8FAFC", "c-bg-2": "#FFFFFF", "c-bg-3": "#F1F5F9",
        "c-bg-4": "#FFFFFF", "c-bg-5": "#F8FAFC",
        "c-border-1": "#E2E8F0", "c-border-2": "#CBD5E1",
        "c-text-1": "#0F172A", "c-text-1b": "#1E293B",
        "c-text-2": "#334155", "c-text-2b": "#475569",
        "c-text-3": "#64748B", "c-text-3b": "#64748B", "c-text-3c": "#64748B",
        "c-text-3d": "#64748B", "c-text-3e": "#94A3B8", "c-text-3f": "#64748B",
        "c-text-4": "#94A3B8", "c-text-4b": "#94A3B8",
        "c-text-4c": "#CBD5E1", "c-text-4d": "#94A3B8",
        "c-accent": "#3B82F6", "c-accent-bright": "#2563EB",
        "c-success": "#10B981", "c-warning": "#F59E0B", "c-danger": "#EF4444",
        "font-mono": "'JetBrains Mono', ui-monospace, monospace",
        "font-sans": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    },
    "Newspaper (light)": {
        "kind": "light",
        "c-bg-1": "#FFFFFF", "c-bg-2": "#FFFFFF", "c-bg-3": "#F5F5F0",
        "c-bg-4": "#FAFAF5", "c-bg-5": "#FFFFFF",
        "c-border-1": "#000000", "c-border-2": "#000000",
        "c-text-1": "#000000", "c-text-1b": "#1A1A1A",
        "c-text-2": "#2A2A2A", "c-text-2b": "#3A3A3A",
        "c-text-3": "#4A4A4A", "c-text-3b": "#5A5A5A", "c-text-3c": "#4A4A4A",
        "c-text-3d": "#5A5A5A", "c-text-3e": "#6A6A6A", "c-text-3f": "#4A4A4A",
        "c-text-4": "#7A7A7A", "c-text-4b": "#8A8A8A",
        "c-text-4c": "#9A9A9A", "c-text-4d": "#7A7A7A",
        "c-accent": "#000000", "c-accent-bright": "#1A1A1A",
        "c-success": "#1A5F1A", "c-warning": "#8B6914", "c-danger": "#8B0000",
        "font-mono": "'Courier New', 'JetBrains Mono', monospace",
        "font-sans": "'Times New Roman', Times, serif",
    },
}

def _build_theme_css(theme_name: str) -> str:
    """Gera o bloco <style>:root { --tokens... }</style> a partir do tema escolhido.
    Inclui ajustes finos para temas light (sombras, hovers etc)."""
    tema = TEMAS.get(theme_name, TEMAS["Command Center (atual)"])
    rules = "\n".join(f"  --{k}: {v};" for k, v in tema.items() if k != "kind")
    # Para temas light, neutraliza efeitos típicos de dark (rgba claros invertidos)
    extras = ""
    if tema.get("kind") == "light":
        # Ajustes: hover rows, alert backgrounds em tons claros
        extras = """
/* Ajustes para tema light */
.tr-cat:hover, .tr-grp:hover, .tr-subg:hover, .tr-leaf:hover { background: rgba(0,0,0,.03) !important; }
.row-alert-vermelho .td-label { background: rgba(239, 68, 68, .06) !important; }
.row-alert-verde .td-label { background: rgba(34, 197, 94, .05) !important; }
.tr-total-final { background: rgba(0,0,0,.04) !important; }
"""
    return f"<style>\n:root {{\n{rules}\n}}\n{extras}\n</style>"


# ─────────────────────────────────────────────────────────────────────────────
# EXECUTIVE BRIEF — narrativa automática para o CEO
# Compõe um bloco no topo do dashboard com: status semáforo, parágrafo
# narrativo e duas colunas (boas notícias / atenções).
# Toda a lógica é determinística (sem IA): templates + regras sobre números.
# ─────────────────────────────────────────────────────────────────────────────

_MESES_NOMES = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


def _brief_fmt(v: float, casas: int = 0) -> str:
    """Formata valor monetário em R$ com sufixo k/M para compactar."""
    abs_v = abs(v)
    if abs_v >= 1_000_000:
        s = f"{v/1_000_000:.2f}".replace('.', ',')
        return f"R$ {s} M"
    elif abs_v >= 1_000:
        s = f"{v/1_000:.0f}"
        return f"R$ {s} k"
    else:
        s = f"{v:.0f}"
        return f"R$ {s}"


def _brief_calc_subtotal(df: pd.DataFrame, estrutura, label_subtotal: str,
                         subtotais: dict) -> float:
    """Soma o valor de todas as categorias até o subtotal `label_subtotal` (inclusivo).
    Retorna 0 se df vazio ou subtotal não encontrado."""
    if df is None or df.empty:
        return 0.0
    total = 0.0
    for nome_dre, _, sinal in estrutura:
        sub = df[df["dre"] == nome_dre]
        if not sub.empty:
            if "sinal" in sub.columns:
                total += float((sub["valor_total"] * sub["sinal"]).sum())
            else:
                total += float(sinal * sub["valor_total"].sum())
        # Se este nome_dre fecha o subtotal procurado, encerra
        if nome_dre in subtotais and subtotais[nome_dre][0] == label_subtotal:
            return total
    return total


def _brief_calc_cat(df: pd.DataFrame, nome_dre: str, sinal: int) -> float:
    """Soma o valor de uma categoria específica no df."""
    if df is None or df.empty:
        return 0.0
    sub = df[df["dre"] == nome_dre]
    if sub.empty:
        return 0.0
    if "sinal" in sub.columns:
        return float((sub["valor_total"] * sub["sinal"]).sum())
    return float(sinal * sub["valor_total"].sum())


def _brief_var_pct(real: float, base: float) -> float | None:
    """Variação % de real vs base. None se base for zero."""
    if base == 0:
        return None
    return (real - base) / abs(base) * 100


def _brief_describe_var(var_pct: float | None, threshold: float) -> tuple:
    """Retorna (cor_hex, qualificador_texto) para uma variação %.
       cor_hex: var() do tema. qualificador: 'superou em X%' etc."""
    if var_pct is None:
        return ('var(--c-text-2,#94A3B8)', 'sem comparação')
    abs_v = abs(var_pct)
    if var_pct >= threshold * 2:
        return ('var(--c-success,#22C55E)', f'muito acima do orçado (+{abs_v:.0f}%)')
    if var_pct >= threshold:
        return ('var(--c-success,#22C55E)', f'acima do orçado (+{abs_v:.0f}%)')
    if var_pct >= 0:
        return ('var(--c-text-1,#E2E8F0)', f'em linha com o orçado (+{abs_v:.1f}%)')
    if var_pct > -threshold:
        return ('var(--c-text-1,#E2E8F0)', f'levemente abaixo (-{abs_v:.1f}%)')
    if var_pct > -threshold * 2:
        return ('var(--c-warning,#F59E0B)', f'abaixo do orçado (-{abs_v:.0f}%)')
    return ('var(--c-danger,#EF4444)', f'muito abaixo do orçado (-{abs_v:.0f}%)')


def _brief_periodo_label(meses_ativos: list, ano: int) -> str:
    """Constrói label do período: 'Jan – Abr 2026' ou 'Abr 2026' se 1 mês."""
    if not meses_ativos:
        return f"{ano}"
    mins, maxs = min(meses_ativos), max(meses_ativos)
    if mins == maxs:
        return f"{_MESES_NOMES[mins]} {ano}"
    return f"{_MESES_NOMES[mins]} – {_MESES_NOMES[maxs]} {ano}"


def _build_executive_brief(df_f, df_orc, df_orc_ano, df_yoy,
                           estrutura, subtotais,
                           empresas_sel, meses_ativos, ano_sel,
                           var_threshold) -> str:
    """Gera o HTML do Executive Brief.

    Lógica:
    1) Calcula Receita Líquida e EBITDA do período (Real, Orçado, Ano Anterior)
    2) Determina status semáforo baseado em EBITDA vs orçado
    3) Compõe narrativa: receita, EBITDA, margem, top contribuidor, pressões
    4) Lista 3 boas notícias e 3 atenções (categorias com maiores variações)
    5) Adiciona projeção de fim de ano (run-rate)
    """
    import datetime as _dt
    if df_f is None or df_f.empty:
        return ""

    # ─── 1. Métricas-chave ───────────────────────────────────────
    rec_real = _brief_calc_subtotal(df_f,    estrutura, 'Receita Líquida', subtotais)
    rec_orc  = _brief_calc_subtotal(df_orc,  estrutura, 'Receita Líquida', subtotais)
    rec_yoy  = _brief_calc_subtotal(df_yoy,  estrutura, 'Receita Líquida', subtotais)

    ebit_real = _brief_calc_subtotal(df_f,   estrutura, 'Resultado Operacional (EBITDA)', subtotais)
    ebit_orc  = _brief_calc_subtotal(df_orc, estrutura, 'Resultado Operacional (EBITDA)', subtotais)
    ebit_yoy  = _brief_calc_subtotal(df_yoy, estrutura, 'Resultado Operacional (EBITDA)', subtotais)

    margem    = (ebit_real / rec_real * 100) if rec_real else 0
    margem_orc = (ebit_orc / rec_orc * 100) if rec_orc else 0

    var_rec_orc   = _brief_var_pct(rec_real, rec_orc)
    var_rec_yoy   = _brief_var_pct(rec_real, rec_yoy)
    var_ebit_orc  = _brief_var_pct(ebit_real, ebit_orc)
    var_ebit_yoy  = _brief_var_pct(ebit_real, ebit_yoy)

    # ─── 2. Status semáforo (baseado em EBITDA vs orçado) ─────────
    if var_ebit_orc is None:
        status, status_label, status_cor, status_bg = 'cinza', 'SEM ORÇADO', 'var(--c-text-3,#607A90)', 'rgba(96,122,144,.18)'
    elif var_ebit_orc >= var_threshold:
        status, status_label, status_cor, status_bg = 'verde', 'NO ALVO', 'var(--c-success,#22C55E)', 'rgba(34,197,94,.18)'
    elif var_ebit_orc <= -var_threshold:
        status, status_label, status_cor, status_bg = 'vermelho', 'FORA DO ALVO', 'var(--c-danger,#EF4444)', 'rgba(239,68,68,.18)'
    else:
        status, status_label, status_cor, status_bg = 'amarelo', 'ATENÇÃO', 'var(--c-warning,#F59E0B)', 'rgba(245,158,11,.18)'

    # ─── 3. Top empresa contribuidora ─────────────────────────────
    top_emp_str = ""
    if empresas_sel and len(empresas_sel) > 1 and ebit_real != 0:
        ebit_por_emp = {}
        for emp in empresas_sel:
            df_emp = df_f[df_f['Empresa'] == emp]
            v = _brief_calc_subtotal(df_emp, estrutura, 'Resultado Operacional (EBITDA)', subtotais)
            if v != 0:
                ebit_por_emp[emp] = v
        if ebit_por_emp:
            top_emp = max(ebit_por_emp, key=ebit_por_emp.get)
            # Limpa nome (remove CNPJ/sufixos)
            top_emp_clean = top_emp.split(' - ')[0] if ' - ' in top_emp else top_emp
            top_emp_clean = top_emp_clean[:40]
            pct_contrib = (ebit_por_emp[top_emp] / ebit_real * 100) if ebit_real else 0
            top_emp_str = f", liderado por <span style='color:var(--c-text-1,#E2E8F0);font-weight:600;'>{top_emp_clean}</span>"

    # ─── 4. Top pressões (categorias com variação desfavorável) ──
    pressoes = []
    positivos = []
    for nome_dre, label, sinal in estrutura:
        val_real = _brief_calc_cat(df_f, nome_dre, sinal)
        val_orc  = _brief_calc_cat(df_orc, nome_dre, sinal)
        if val_orc == 0 or val_real == 0:
            continue
        var = _brief_var_pct(val_real, val_orc)
        if var is None:
            continue
        diff_abs = abs(val_real - val_orc)
        item = {'label': label, 'nome': nome_dre, 'var_pct': var,
                'diff_abs': diff_abs, 'val_real': val_real, 'val_orc': val_orc}
        if var <= -var_threshold:
            pressoes.append(item)
        elif var >= var_threshold:
            positivos.append(item)

    pressoes.sort(key=lambda x: -x['diff_abs'])
    positivos.sort(key=lambda x: -x['diff_abs'])
    top_pressoes = pressoes[:3]
    top_positivos = positivos[:3]

    # ─── 5. Projeção fim de ano (run-rate) ────────────────────────
    meta_ebit_ano = _brief_calc_subtotal(df_orc_ano, estrutura,
                                          'Resultado Operacional (EBITDA)', subtotais)
    proj_str = ""
    if meses_ativos and len(meses_ativos) >= 1 and meta_ebit_ano != 0:
        meses_restantes = 12 - len(meses_ativos)
        run_rate = ebit_real / len(meses_ativos)
        projecao = ebit_real + run_rate * meses_restantes
        var_proj = _brief_var_pct(projecao, meta_ebit_ano)
        if var_proj is not None:
            cor_proj, qual_proj = _brief_describe_var(var_proj, var_threshold)
            proj_str = (f" Em ritmo atual, projeção de <span style='color:var(--c-text-1,#E2E8F0);font-weight:600;'>"
                       f"{_brief_fmt(projecao)}</span> de EBITDA no ano "
                       f"(<span style='color:{cor_proj};'>{qual_proj.replace('do orçado','da meta anual').replace('com o orçado','com a meta anual')}</span> de "
                       f"{_brief_fmt(meta_ebit_ano)}).")

    # ─── 6. Compõe narrativa ──────────────────────────────────────
    cor_rec_orc, qual_rec_orc = _brief_describe_var(var_rec_orc, var_threshold)
    cor_ebit_orc, qual_ebit_orc = _brief_describe_var(var_ebit_orc, var_threshold)

    rec_yoy_str = ""
    if var_rec_yoy is not None:
        seta_yoy = "↑" if var_rec_yoy >= 0 else "↓"
        cor_yoy = "var(--c-success,#22C55E)" if var_rec_yoy >= 0 else "var(--c-danger,#EF4444)"
        rec_yoy_str = f", <span style='color:{cor_yoy};'>{seta_yoy} {abs(var_rec_yoy):.0f}% YoY</span>"

    ebit_yoy_str = ""
    if var_ebit_yoy is not None:
        seta_yoy = "↑" if var_ebit_yoy >= 0 else "↓"
        cor_yoy = "var(--c-success,#22C55E)" if var_ebit_yoy >= 0 else "var(--c-danger,#EF4444)"
        ebit_yoy_str = f", <span style='color:{cor_yoy};'>{seta_yoy} {abs(var_ebit_yoy):.0f}% YoY</span>"

    # Detecta padrão "tesoura": receita acima, EBITDA abaixo
    tesoura_str = ""
    if (var_rec_orc is not None and var_ebit_orc is not None
        and var_rec_orc >= var_threshold and var_ebit_orc <= -var_threshold/2):
        tesoura_str = (" <span style='color:var(--c-warning,#F59E0B);'>Apesar da receita acima do esperado, "
                      "o EBITDA ficou pressionado</span> pelo aumento de custos/despesas.")

    # Lista de pressões para narrativa
    pressao_narr = ""
    if top_pressoes:
        nomes = [p['label'] for p in top_pressoes[:2]]
        if len(nomes) == 1:
            pressao_narr = f" Principal pressão veio de <span style='color:var(--c-text-1,#E2E8F0);'>{nomes[0]}</span>."
        else:
            pressao_narr = (f" Principais pressões vieram de <span style='color:var(--c-text-1,#E2E8F0);'>"
                           f"{nomes[0]}</span> e <span style='color:var(--c-text-1,#E2E8F0);'>{nomes[1]}</span>.")

    # Margem comparada
    margem_diff_str = ""
    if margem_orc != 0:
        diff_pp = margem - margem_orc
        if abs(diff_pp) >= 0.5:
            cor_mg = "var(--c-success,#22C55E)" if diff_pp >= 0 else "var(--c-warning,#F59E0B)"
            seta_mg = "↑" if diff_pp >= 0 else "↓"
            margem_diff_str = f" (<span style='color:{cor_mg};'>{seta_mg} {abs(diff_pp):.1f}pp vs orçada de {margem_orc:.1f}%</span>)"

    narrativa = (
        f"Receita líquida acumulada de <span style='color:var(--c-text-1,#E2E8F0);font-weight:600;'>{_brief_fmt(rec_real)}</span> "
        f"<span style='color:{cor_rec_orc};'>{qual_rec_orc}</span>{rec_yoy_str}{top_emp_str}. "
        f"EBITDA fechou em <span style='color:var(--c-text-1,#E2E8F0);font-weight:600;'>{_brief_fmt(ebit_real)}</span> "
        f"(margem <span style='color:var(--c-text-1,#E2E8F0);'>{margem:.1f}%</span>{margem_diff_str}), "
        f"<span style='color:{cor_ebit_orc};'>{qual_ebit_orc}</span>{ebit_yoy_str}.{tesoura_str}{pressao_narr}{proj_str}"
    )

    # ─── 7. Boas notícias e atenções ──────────────────────────────
    boas_notas = []
    for p in top_positivos:
        diff_str = _brief_fmt(p['diff_abs'])
        boas_notas.append(f"<div>• <b>{p['label']}</b> superou orçado em {abs(p['var_pct']):.0f}% ({diff_str})</div>")
    # Se receita YoY positiva, adiciona
    if var_rec_yoy is not None and var_rec_yoy >= var_threshold and len(boas_notas) < 3:
        boas_notas.append(f"<div>• Receita Líquida ↑ {var_rec_yoy:.0f}% vs mesmo período de {ano_sel-1}</div>")
    if not boas_notas:
        boas_notas.append("<div style='color:var(--c-text-3,#607A90);'>Sem destaques positivos significativos</div>")

    atencoes = []
    for p in top_pressoes:
        diff_str = _brief_fmt(p['diff_abs'])
        atencoes.append(f"<div>• <b>{p['label']}</b> estourou em {abs(p['var_pct']):.0f}% ({diff_str})</div>")
    if var_ebit_yoy is not None and var_ebit_yoy <= -var_threshold and len(atencoes) < 3:
        atencoes.append(f"<div>• EBITDA ↓ {abs(var_ebit_yoy):.0f}% vs mesmo período de {ano_sel-1}</div>")
    if not atencoes:
        atencoes.append("<div style='color:var(--c-text-3,#607A90);'>Nenhuma pressão significativa identificada</div>")

    # ─── 8. Renderiza o HTML ──────────────────────────────────────
    periodo_label = _brief_periodo_label(meses_ativos, ano_sel)
    timestamp = _dt.datetime.now().strftime("%d/%m %Hh%M")

    boas_html = "\n".join(boas_notas[:3])
    atencoes_html = "\n".join(atencoes[:3])

    return f"""
<!-- EXECUTIVE BRIEF -->
<div style="background: var(--c-bg-2,#0A1628); border: 1px solid var(--c-border-2,#1A3050); border-radius: 10px; padding: 14px 18px; margin: 12px 12px 14px 12px; font-family: 'Inter', -apple-system, sans-serif;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
    <span style="display: inline-block; padding: 3px 10px; border-radius: 12px; background: {status_bg}; border: 1px solid {status_cor}; color: {status_cor}; font-size: 10px; font-weight: 700; letter-spacing: .05em;">{status_label}</span>
    <span style="color: var(--c-text-2,#94A3B8); font-size: 11px;">Resumo Executivo · {periodo_label} · atualizado em {timestamp}</span>
  </div>
  <div style="color: var(--c-text-1b,#CBD5E1); font-size: 13.5px; line-height: 1.65; margin-bottom: 12px;">
    {narrativa}
  </div>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
    <div style="background: rgba(34,197,94,.06); border-left: 3px solid var(--c-success,#22C55E); padding: 8px 12px; border-radius: 0 6px 6px 0;">
      <div style="color: var(--c-success,#22C55E); font-size: 9.5px; font-weight: 700; letter-spacing: .06em; margin-bottom: 4px;">BOAS NOTÍCIAS</div>
      <div style="color: var(--c-text-1b,#CBD5E1); font-size: 11.5px; line-height: 1.7;">{boas_html}</div>
    </div>
    <div style="background: rgba(239,68,68,.06); border-left: 3px solid var(--c-danger,#EF4444); padding: 8px 12px; border-radius: 0 6px 6px 0;">
      <div style="color: var(--c-danger,#EF4444); font-size: 9.5px; font-weight: 700; letter-spacing: .06em; margin-bottom: 4px;">ATENÇÕES</div>
      <div style="color: var(--c-text-1b,#CBD5E1); font-size: 11.5px; line-height: 1.7;">{atencoes_html}</div>
    </div>
  </div>
</div>
<!-- END EXECUTIVE BRIEF -->
"""



with st.sidebar:
    if st.button("🔄 Recarregar dados do Excel"):
        if os.path.exists(parquet_path): os.remove(parquet_path)
        st.cache_data.clear(); st.rerun()

with st.spinner("Carregando…"):
    try:
        _map_mtime = os.path.getmtime(mapping_path) if os.path.exists(mapping_path) else 0
        mapping = load_mapping(mapping_path, _mtime=_map_mtime)
        if not mapping:
            st.warning("⚠️ mapeamento_td.xlsx não encontrado — usando classificação original.")
        df_raw = load_data(xlsx_path, parquet_path)
        df     = aplicar_mapping(df_raw, mapping)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xlsx_path}"); st.stop()
    except Exception as exc:
        # Se o parquet estiver corrompido/incompatível, remove e tenta de novo
        if os.path.exists(parquet_path):
            os.remove(parquet_path)
            st.cache_data.clear()
            try:
                df_raw = load_data(xlsx_path, parquet_path)
                df     = aplicar_mapping(df_raw, mapping)
            except Exception as exc2:
                st.error(f"Erro ao carregar: {exc2}")
                st.stop()
        else:
            st.error(f"Erro ao carregar: {exc}")
            st.stop()
# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTROS (Cascata Completa)
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔎 Filtros")
    
    # 1. Empresa e Cenário
    empresas_all = sorted(df["Empresa"].unique())
    empresa_fmt  = lambda x: x.split(" - ", 1)[-1] if " - " in x else x

    comparar_empresas = st.toggle("🔀 Comparar múltiplas empresas", value=False, key="comparar_empresas")

    if comparar_empresas:
        empresas_sel = st.multiselect(
            "🏢 Empresas",
            empresas_all,
            default=empresas_all,
            format_func=empresa_fmt,
            key="empresas_multi"
        )
        if not empresas_sel:
            empresas_sel = empresas_all
        empresa_unica = empresas_sel[0]  # referência para filtros dependentes
    else:
        empresa_unica = st.selectbox(
            "🏢 Empresa",
            empresas_all,
            format_func=empresa_fmt,
            index=0,
            key="empresa_unica"
        )
        empresas_sel = [empresa_unica]

    cenarios_all = sorted(df[df["Empresa"].isin(empresas_sel)]["cp_ms"].unique())

    todos_cenarios = st.toggle("📋 Todos os cenários", value=True, key="todos_cenarios")
    if todos_cenarios:
        cenarios_sel = cenarios_all
    else:
        cenarios_sel = st.multiselect(
            "Selecionar cenários",
            cenarios_all,
            default=cenarios_all,
            key="cenarios_manual"
        )
        if not cenarios_sel:
            cenarios_sel = cenarios_all
    
    # 2. Datas (MOVIDAS PARA CIMA)
    anos    = sorted(df["Ano"].dropna().unique().astype(int), reverse=True)
    idx_ano = anos.index(2026) if 2026 in anos else 0
    ano_sel = st.selectbox("📅 Ano", anos, index=idx_ano)
    
    meses_do_ano = sorted(df[df["Ano"]==ano_sel]["Mes"].dropna().unique().astype(int))
    st.markdown("**📆 Período**")
    c1, c2 = st.columns(2)
    with c1:
        mes_de = st.selectbox("De", meses_do_ano, format_func=lambda m: MESES_CURTO[m],
                              index=0, key="mes_de")
    with c2:
        opcoes_ate = [m for m in meses_do_ano if m >= mes_de]
        mes_ate = st.selectbox("Até", opcoes_ate, format_func=lambda m: MESES_CURTO[m],
                               index=len(opcoes_ate)-1, key="mes_ate")
    meses_sel = list(range(mes_de, mes_ate + 1))
    
    # 3. CRD Dinâmico (AGORA FILTRA POR EMPRESA, CENÁRIO E DATA)
    df_opcoes_crd = df[
        df["Empresa"].isin(empresas_sel) & 
        df["cp_ms"].isin(cenarios_sel) &
        (df["Ano"] == ano_sel) & 
        df["Mes"].isin(meses_sel)
    ]
    crd_all = sorted(df_opcoes_crd["CRD"].unique())
    crd_sel = st.multiselect(
        "🎯 Centro de Resultado (CRD)",
        crd_all,
        default=crd_all,
        format_func=lambda x: x.split(" - ", 1)[-1] if " - " in x else x
    )

    st.divider()
    mostrar_orfaos = st.toggle("⚠️ Mostrar contas não mapeadas", value=True)

    st.markdown("**🎨 Tema visual**")
    tema_escolhido = st.selectbox(
        "Selecione o tema",
        options=list(TEMAS.keys()),
        index=0,
        key="tema_visual",
        help="Troca paleta de cores e tipografia. A estrutura da DRE, alertas e gráficos permanecem idênticos."
    )

    st.markdown("**🚨 Alertas de desvio (Real vs Orçado)**")
    var_threshold = st.slider(
        "Banda de tolerância (±%)",
        min_value=5, max_value=50, value=5, step=5,
        help=("Define a banda ±T% em torno do orçado. Acima de +T%: verde (favorável). "
              "Dentro da banda: amarelo (tolerância). Abaixo de -T%: vermelho (desfavorável)."),
        key="var_threshold"
    )

# ─────────────────────────────────────────────────────────────────────────────
# FILTRO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
# cenarios_sel pode incluir "Orcamento" — removemos do realizado
CPMS_ORCAMENTO = "Orcamento"
cenarios_real = [c for c in cenarios_sel if c != CPMS_ORCAMENTO]

df_f = df[
    df["Empresa"].isin(empresas_sel) &
    df["cp_ms"].isin(cenarios_real) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel) &
    df["Mes"].isin(meses_sel)
].copy()

# DataFrame do orçamento (mesmo empresa/CRD/período, cp_ms == Orcamento)
tem_orcamento = CPMS_ORCAMENTO in df["cp_ms"].unique()
df_orc = df[
    df["Empresa"].isin(empresas_sel) &
    (df["cp_ms"] == CPMS_ORCAMENTO) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel) &
    df["Mes"].isin(meses_sel)
].copy() if tem_orcamento else pd.DataFrame(columns=df.columns)

# Orçamento do ANO INTEIRO (todos os meses) — denominador fixo para Real/Orc Ano%
df_orc_ano = df[
    df["Empresa"].isin(empresas_sel) &
    (df["cp_ms"] == CPMS_ORCAMENTO) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel)
].copy() if tem_orcamento else pd.DataFrame(columns=df.columns)

# Realizado dos meses SUBSEQUENTES ao período filtrado — coluna "Prov."
_meses_prov = [m for m in range(1, 13) if m not in meses_sel]
df_prov = df[
    df["Empresa"].isin(empresas_sel) &
    df["cp_ms"].isin(cenarios_real) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel) &
    df["Mes"].isin(_meses_prov)
].copy() if _meses_prov else pd.DataFrame(columns=df.columns)

# Realizado do ANO INTEIRO — usado para gráficos de evolução mensal por linha
df_ano = df[
    df["Empresa"].isin(empresas_sel) &
    df["cp_ms"].isin(cenarios_real) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel)
].copy()

# Realizado do MESMO PERÍODO DO ANO ANTERIOR — usado para comparação YoY no Executive Brief
df_yoy = df[
    df["Empresa"].isin(empresas_sel) &
    df["cp_ms"].isin(cenarios_real) &
    df["CRD"].isin(crd_sel) &
    (df["Ano"] == ano_sel - 1) &
    df["Mes"].isin(meses_sel)
].copy()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _soma(frame: pd.DataFrame, sp: int) -> float:
    if "sinal" in frame.columns:
        return float((frame["valor_total"] * frame["sinal"]).sum())
    return float(sp * frame["valor_total"].sum())

def _fmt(v: float, casas: int = 0) -> str:
    """Formata número no padrão brasileiro: 1.234.567,89"""
    if casas == 0:
        s = f"{abs(v):,.0f}"
    else:
        s = f"{abs(v):,.2f}"
    # Converte separadores para padrão BR
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"({s})" if v < 0 else s

def _cor(v: float) -> str:
    return "var(--c-danger,#EF4444)" if v < 0 else "var(--c-success,#22C55E)"

# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUÇÃO DA TABELA HTML
# A DRE inteira é uma única tabela HTML com linhas colapsáveis via JS puro.
# Hierarquia: Seção → Categoria → Grupo → SubGrupo → TD
# ─────────────────────────────────────────────────────────────────────────────
def build_dre_html(df_f: pd.DataFrame, df_orc: pd.DataFrame, df_orc_ano: pd.DataFrame,
                   df_prov: pd.DataFrame, df_ano: pd.DataFrame,
                   estrutura, subtotais, secoes,
                   fora_dre: str, mostrar_orfaos: bool, meses_ativos: list = None,
                   var_threshold: float = 10.0, tema: str = "Command Center (atual)",
                   df_yoy: pd.DataFrame = None, empresas_sel: list = None,
                   ano_sel: int = None) -> str:

    dres_no_arquivo = set(df_f["dre"].unique())
    dres_mapeadas   = set()
    acumulador      = 0.0
    acumulador_orc  = 0.0  # acumulador paralelo para o orçado
    acumulador_orc_ano = 0.0  # acumulador orçado ano inteiro
    acumulador_prov = 0.0  # acumulador realizado meses subsequentes
    resumo          = {}   # para a sidebar
    resumo_meses    = {}   # subtotais mês a mês — calculado após o loop principal
    detalhe_data    = {}   # chave → lista de dicts de linhas para o modal
    chart_data      = {}   # chave → {label, real:{m:v}, orc:{m:v}} para mini-gráficos

    # Meses disponíveis nos dados filtrados (para colunas mensais)
    meses_disponiveis = sorted([int(m) for m in df_f["Mes"].dropna().unique()])
    if meses_ativos is None:
        meses_ativos = meses_disponiveis

    def _soma_mes(frame, sp, mes):
        sub = frame[frame["Mes"] == mes]
        if sub.empty: return 0.0
        if "sinal" in sub.columns: return float((sub["valor_total"] * sub["sinal"]).sum())
        return float(sp * sub["valor_total"].sum())

    linhas_html = []   # cada item = string HTML de uma <tr>

    # Pré-indexa orçamento por (dre, Grupo, SubGrupo, Tipo_Documento) para lookups rápidos
    _orc_cache: dict = {}
    def _soma_orc(frame_real: pd.DataFrame, sp: int,
                  nivel: str = "cat", nome_dre: str = "",
                  grupo: str = "", subg: str = "", td: str = "") -> float:
        """Soma o valor orçado correspondente ao frame realizado passado."""
        if df_orc.empty:
            return 0.0
        mask = df_orc["dre"] == nome_dre
        if nivel in ("grp", "subg", "td") and grupo:
            mask &= df_orc["Grupo"] == grupo
        if nivel in ("subg", "td") and subg:
            mask &= df_orc["SubGrupo"] == subg
        if nivel == "td" and td:
            mask &= df_orc["Tipo_Documento"] == td
        sub = df_orc[mask]
        if sub.empty:
            return 0.0
        if "sinal" in sub.columns:
            return float((sub["valor_total"] * sub["sinal"]).sum())
        return float(sp * sub["valor_total"].sum())

    def _soma_orc_ano(sp: int, nome_dre: str = "",
                      grupo: str = "", subg: str = "", td: str = "",
                      nivel: str = "cat") -> float:
        """Soma o orçado do ANO INTEIRO (sem filtro de meses) para a linha."""
        if df_orc_ano.empty:
            return 0.0
        mask = df_orc_ano["dre"] == nome_dre
        if nivel in ("grp", "subg", "td") and grupo:
            mask &= df_orc_ano["Grupo"] == grupo
        if nivel in ("subg", "td") and subg:
            mask &= df_orc_ano["SubGrupo"] == subg
        if nivel == "td" and td:
            mask &= df_orc_ano["Tipo_Documento"] == td
        sub = df_orc_ano[mask]
        if sub.empty:
            return 0.0
        if "sinal" in sub.columns:
            return float((sub["valor_total"] * sub["sinal"]).sum())
        return float(sp * sub["valor_total"].sum())

    def _soma_prov(sp: int, nome_dre: str = "",
                   grupo: str = "", subg: str = "", td: str = "",
                   nivel: str = "cat") -> float:
        """Soma o realizado dos meses SUBSEQUENTES ao período filtrado."""
        if df_prov.empty:
            return 0.0
        mask = df_prov["dre"] == nome_dre
        if nivel in ("grp", "subg", "td") and grupo:
            mask &= df_prov["Grupo"] == grupo
        if nivel in ("subg", "td") and subg:
            mask &= df_prov["SubGrupo"] == subg
        if nivel == "td" and td:
            mask &= df_prov["Tipo_Documento"] == td
        sub = df_prov[mask]
        if sub.empty:
            return 0.0
        if "sinal" in sub.columns:
            return float((sub["valor_total"] * sub["sinal"]).sum())
        return float(sp * sub["valor_total"].sum())

    def _chart_for(sp: int, label: str, nome_dre: str = "",
                   grupo: str = "", subg: str = "", td: str = "",
                   nivel: str = "cat") -> dict:
        """Gera dict {label, real:{1..12}, orc:{1..12}} para o gráfico de evolução mensal."""
        def _sum_mes(src, mes):
            if src.empty:
                return 0.0
            mask = src["dre"] == nome_dre
            if nivel in ("grp", "subg", "td") and grupo:
                mask &= src["Grupo"] == grupo
            if nivel in ("subg", "td") and subg:
                mask &= src["SubGrupo"] == subg
            if nivel == "td" and td:
                mask &= src["Tipo_Documento"] == td
            mask &= src["Mes"] == mes
            sub = src[mask]
            if sub.empty:
                return 0.0
            if "sinal" in sub.columns:
                return float((sub["valor_total"] * sub["sinal"]).sum())
            return float(sp * sub["valor_total"].sum())

        return {
            "label": label,
            "real": {str(m): _sum_mes(df_ano, m) for m in range(1, 13)},
            "orc":  {str(m): _sum_mes(df_orc_ano, m) for m in range(1, 13)},
        }

    def _alert_badge(valor: float, orc: float) -> tuple:
        """Avalia o desempenho Real vs Orçado e retorna (badge_html, level).

        No espaço com sinal já aplicado (receitas positivas, despesas negativas):
            var_pct = (valor - orc) / abs(orc) * 100

        var_pct > 0  → Real foi FAVORÁVEL ao orçado
                       (receita acima do esperado OU despesa abaixo do esperado)
        var_pct < 0  → Real foi DESFAVORÁVEL ao orçado
                       (receita abaixo do esperado OU despesa acima do esperado)

        Threshold T = var_threshold (do slider):
            var_pct ≥ +T  → 'verde'    (desempenho favorável significativo)
            -T < var_pct < +T → 'amarelo'  (dentro da banda de tolerância)
            var_pct ≤ -T  → 'vermelho' (desempenho desfavorável significativo)

        Linhas sem orçamento (orc=0) retornam level='' (sem badge).
        """
        if orc == 0:
            return ("", "")
        var_pct = (valor - orc) / abs(orc) * 100
        abs_pct = abs(var_pct)

        if var_pct >= var_threshold:
            tip = f"Favorável: Real superou orçado em {abs_pct:.1f}% (threshold {var_threshold:.0f}%)"
            badge = (
                f"<span class='alert-badge alert-verde' title='{tip}' "
                f"onclick='event.stopPropagation();' "
                f"style='display:inline-block;margin-left:6px;color:var(--c-success,#22C55E);"
                f"font-size:11px;cursor:help;vertical-align:middle;'>&#9650;</span>"
            )
            return (badge, "verde")

        if var_pct <= -var_threshold:
            tip = f"Desfavorável: Real ficou {abs_pct:.1f}% pior que o orçado (threshold {var_threshold:.0f}%)"
            badge = (
                f"<span class='alert-badge alert-vermelho' title='{tip}' "
                f"onclick='event.stopPropagation();' "
                f"style='display:inline-block;margin-left:6px;color:var(--c-danger,#EF4444);"
                f"font-size:11px;cursor:help;vertical-align:middle;'>&#9888;</span>"
            )
            return (badge, "vermelho")

        # Dentro da banda de tolerância — amarelo discreto
        tip = f"Dentro da tolerância (desvio de {abs_pct:.1f}% vs orçado, banda ±{var_threshold:.0f}%)"
        badge = (
            f"<span class='alert-badge alert-amarelo' title='{tip}' "
            f"onclick='event.stopPropagation();' "
            f"style='display:inline-block;margin-left:6px;color:var(--c-warning,#F59E0B);"
            f"font-size:11px;cursor:help;vertical-align:middle;opacity:.7;'>&#9679;</span>"
        )
        return (badge, "amarelo")

    def _td_orc(label: str, valor: float, orc: float, orc_ano: float = 0.0,
                prov: float = None) -> str:
        """Gera células HTML de Orçado, Var%, Real/Orc Ano% e Prov. para uma linha da DRE."""
        # Célula Prov.
        if prov is not None and not df_prov.empty:
            prov_cor = "var(--c-text-2,#94A3B8)" if prov == 0 else ("var(--c-success,#22C55E)" if prov > 0 else "var(--c-danger,#F87171)")
            td_prov = f"<td class='td-prov' style='color:{prov_cor};'>{_fmt(prov) if prov != 0 else '—'}</td>"
        else:
            td_prov = "<td class='td-prov' style='color:var(--c-text-4c,#334155);'>—</td>"

        if df_orc.empty:
            return f"<td class='td-orc'></td><td class='td-var'></td><td class='td-exe'></td>{td_prov}"
        orc_fmt = _fmt(orc) if orc != 0 else "—"

        # Célula Real/Orc Ano%
        if orc_ano != 0:
            exe_pct = (valor / abs(orc_ano)) * 100
            exe_cor = "var(--c-success,#22C55E)" if exe_pct >= 100 else ("var(--c-warning,#F59E0B)" if exe_pct >= 75 else "var(--c-danger,#EF4444)")
            td_exe = f"<td class='td-exe' style='color:{exe_cor};'>{exe_pct:.1f}%</td>"
        else:
            td_exe = "<td class='td-exe' style='color:var(--c-text-3e,#475569);'>—</td>"

        if orc == 0:
            return (
                f"<td class='td-orc'>{orc_fmt}</td>"
                f"<td class='td-var' style='color:var(--c-text-2,#94A3B8);'>—</td>"
                f"{td_exe}{td_prov}"
            )

        var_pct = (valor - orc) / abs(orc) * 100
        ruim = valor < orc
        cor_var = "var(--c-danger,#EF4444)" if ruim else "var(--c-success,#22C55E)"
        sinal_v = "▲" if var_pct > 0 else ("▼" if var_pct < 0 else "")
        var_str = f"{sinal_v} {abs(var_pct):.1f}%"
        return (
            f"<td class='td-orc'>{orc_fmt}</td>"
            f"<td class='td-var' style='color:{cor_var};font-weight:600;'>{var_str}</td>"
            f"{td_exe}{td_prov}"
        )

    uid = [0]  # contador de IDs para grupos colapsáveis
    def next_id():
        uid[0] += 1
        return f"g{uid[0]}"

    # ── estilos inline base ───────────────────────────────────────────────────
    F = "font-family:'Inter',sans-serif;"

    # Categorias que recebem coluna de % (pós-Margem de Contribuição)
    NOMES_COM_PCT = {
        "Impostos Incidentes s/ Receita Tributável",
        "Despesas Administrativa, Comercial e Mkt",
        "(+) Receitas Financeiras",
        "INVESTIMENTOS",
    }

    def _pct_html(valor: float, mc: float, cls_extra: str = "") -> str:
        """Retorna <td> com o percentual sobre MC, ou vazio se MC=0 ou não aplicável."""
        if mc == 0 or mc is None:
            return f"<td class='td-pct {cls_extra}'></td>"
        pct = (valor / mc) * 100
        cor = "var(--c-danger,#EF4444)" if pct < 0 else "var(--c-success,#22C55E)"
        s = f"{abs(pct):.1f}%"
        s = f"({s})" if pct < 0 else s
        return f"<td class='td-pct {cls_extra}' style='color:{cor};'>{s}</td>"

    def _pct_vazio() -> str:
        return "<td class='td-pct'></td>"

    def _chart_icon(chart_key: str) -> str:
        """Retorna o ícone de gráfico que abre o modal de evolução mensal."""
        if not chart_key:
            return ""
        import html as _html_mod
        safe = _html_mod.escape(chart_key, quote=True)
        return (
            f"<span class='chart-icon' data-chart-key=\"{safe}\" "
            f"onclick=\"event.stopPropagation();showChart(this.getAttribute('data-chart-key'))\" "
            f"title='Ver evolução mensal vs orçado' "
            f"style='display:inline-block;margin-left:6px;cursor:pointer;"
            f"color:var(--c-accent,#3B82F6);font-size:11px;vertical-align:middle;opacity:.55;"
            f"transition:opacity .15s;' "
            f"onmouseover=\"this.style.opacity='1'\" "
            f"onmouseout=\"this.style.opacity='.55'\">&#128202;</span>"
        )

    def tr_secao(titulo: str) -> str:
        _cols = 7 + len(meses_ativos)
        return (
            f"<tr class='tr-sec'>"
            f"<td colspan='{_cols}' class='td-sec'>{titulo}</td></tr>"
        )

    def tr_categoria(label: str, valor: float, gid: str, mc: float = None,
                     orc: float = 0.0, orc_ano: float = 0.0, prov: float = None,
                     td_meses: str = '', chart_key: str = None) -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc) if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc, orc_ano, prov)
        alert_html, alert_level = _alert_badge(valor, orc)
        chart_html = _chart_icon(chart_key)
        cls_alert = (" row-alert-" + alert_level) if alert_level else ""
        return (
            f"<tr class='tr-cat{cls_alert}' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-cat-label'>"
            f"<span id='arrow-{gid}' class='arrow'>&#9658;</span>"
            f"&nbsp;{label}{chart_html}{alert_html}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val' style='color:{cor};font-weight:600;'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_grupo(label: str, valor: float, gid: str, pgid: str, mc: float = None,
                orc: float = 0.0, orc_ano: float = 0.0, prov: float = None,
                td_meses: str = '', chart_key: str = None) -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc, "td-val-sm") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc, orc_ano, prov)
        alert_html, alert_level = _alert_badge(valor, orc)
        chart_html = _chart_icon(chart_key)
        cls_alert = (" row-alert-" + alert_level) if alert_level else ""
        return (
            f"<tr class='sub-{pgid} owner-{gid} tr-grp{cls_alert}' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-grp-label'>"
            f"<span id='arrow-{gid}' class='arrow'>&#9658;</span>"
            f"&nbsp;{label}{chart_html}{alert_html}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-val-sm' style='color:{cor};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_subgrupo(label: str, valor: float, gid: str, pgid: str, mc: float = None,
                   orc: float = 0.0, orc_ano: float = 0.0, prov: float = None,
                   td_meses: str = '', chart_key: str = None) -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc, "td-val-sm") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc, orc_ano, prov)
        alert_html, alert_level = _alert_badge(valor, orc)
        chart_html = _chart_icon(chart_key)
        cls_alert = (" row-alert-" + alert_level) if alert_level else ""
        return (
            f"<tr class='sub-{pgid} owner-{gid} tr-subg{cls_alert}' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-subg-label'>"
            f"<span id='arrow-{gid}' class='arrow arrow-sm'>&#9658;</span>"
            f"&nbsp;{label}{chart_html}{alert_html}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-val-sm' style='color:{cor};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_td(label: str, valor: float, pgid: str, modal_key: str, mc: float = None,
             orc: float = 0.0, orc_ano: float = 0.0, prov: float = None,
             td_meses_arg: str = '') -> str:
        cor = _cor(valor)
        import html as _html_mod
        data_key = _html_mod.escape(modal_key, quote=True)
        pct = _pct_html(valor, mc, "td-val-xs") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc, orc_ano, prov)
        alert_html, alert_level = _alert_badge(valor, orc)
        cls_alert = (" row-alert-" + alert_level) if alert_level else ""
        return (
            f"<tr class='sub-{pgid} tr-leaf{cls_alert}' data-key=\"{data_key}\"" 
            f" style='cursor:pointer;' title='Clique para ver detalhes'>"
            f"<td class='td-label td-leaf-label'>"
            f"<span style='color:var(--c-text-2,#94A3B8);font-size:10px;margin-right:4px;'>&#128269;</span>"
            f"{label}{alert_html}</td>"
            f"{pct}"
            f"{td_meses_arg}"
            f"<td class='td-val td-val-xs' style='color:{cor};'>{_fmt(valor, 2)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_subtotal(label: str, valor: float, is_final: bool = False, mc: float = None,
                   orc: float = 0.0, orc_ano: float = 0.0, prov: float = None,
                   td_meses: str = '', chart_key: str = None) -> str:
        pct = _pct_html(valor, mc, "td-subtotal-val") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc, orc_ano, prov)
        alert_html, alert_level = _alert_badge(valor, orc)
        chart_html = _chart_icon(chart_key)
        cls_alert = (" row-alert-" + alert_level) if alert_level else ""
        n_mes_cols = len(meses_ativos)
        total_cols = 7 + n_mes_cols
        if is_final:
            cor_v = "var(--c-text-2b,#86EFAC)" if valor >= 0 else "var(--c-text-1b,#FCA5A5)"
            pct_final = _pct_html(valor, mc, "td-total-val") if mc is not None else _pct_vazio()
            return (
                f"<tr class='tr-total-final{cls_alert}'>"
                f"<td class='td-label td-total-label' style='color:var(--c-text-1,#E2E8F0);'>(=) {label}{chart_html}{alert_html}</td>"
                f"{pct_final}"
                f"{td_meses}"
                f"<td class='td-val td-total-val' style='color:{cor_v};'>{_fmt(valor)}</td>"
                f"{td_orc_html}</tr>"
                f"<tr><td colspan='{total_cols}' style='height:4px;background:var(--c-bg-3,#060D1A);'></td></tr>"
            )
        cor_v = _cor(valor)
        return (
            f"<tr class='tr-subtotal{cls_alert}'>"
            f"<td class='td-label td-subtotal-label'>(=) {label}{chart_html}{alert_html}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-subtotal-val' style='color:{cor_v};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
            f"<tr><td colspan='{total_cols}' style='height:2px;background:var(--c-bg-3,#060D1A);'></td></tr>"
        )


    # ── pré-calcula a Margem de Contribuição ─────────────────────────────────
    # MC = soma das categorias que a compõem (até "(+) Reembolso de Custos" inclusive)
    _mc_cats = {
        "VENDA BRUTA":                  +1,
        "(-) Comissão sobre Vendas":    -1,
        "(-) Custo das Vendas":         -1,
        "(+) Reembolso de Custos":      +1,
    }
    margem_contribuicao = sum(
        _soma(df_f[df_f["dre"] == c], s)
        for c, s in _mc_cats.items()
        if not df_f[df_f["dre"] == c].empty
    )

    # MC mês a mês — usada para calcular % MC por mês nas células mensais
    _mc_por_mes = {
        m: sum(
            _soma_mes(df_f[df_f["dre"] == c], s, m)
            for c, s in _mc_cats.items()
            if not df_f[df_f["dre"] == c].empty
        )
        for m in meses_disponiveis
    }

    # Venda Bruta mês a mês — divisor para % MC da linha de MC
    _vb_cats = {"VENDA BRUTA": +1}
    _vb_por_mes = {
        m: sum(
            _soma_mes(df_f[df_f["dre"] == c], s, m)
            for c, s in _vb_cats.items()
            if not df_f[df_f["dre"] == c].empty
        )
        for m in meses_disponiveis
    }
    _venda_bruta_total = sum(
        _soma(df_f[df_f["dre"] == c], s)
        for c, s in _vb_cats.items()
        if not df_f[df_f["dre"] == c].empty
    )

    # ── Detecção de desvios no mês mais recente ──────────────────────────────
    # Thresholds meio-termo
    _ALERTA_MOM   = 0.40   # MoM% >= 40% → alerta vermelho
    _ATENCAO_MOM  = 0.20   # MoM% >= 20% → atenção amarelo
    _ALERTA_MEDIA = 0.50   # desvio vs média >= 50% → alerta vermelho
    _ATENCAO_MEDIA= 0.25   # desvio vs média >= 25% → atenção amarelo
    _mes_atual    = max(meses_ativos) if meses_ativos else None

    def _calcular_desvio(vals_por_mes, sinal_contabil=+1, eh_resultado=False):
        """
        Retorna (nivel, motivo) para o mês mais recente.

        Trabalha no espaço do VALOR EXIBIDO (já com sinal aplicado pelo DataFrame):
          - Receitas: valores positivos  → crescimento = bom
          - Despesas: valores negativos  → ficar menos negativo = bom (despesa caiu)
          - Resultados (EBITDA etc.): podem ser + ou - → crescimento sempre = bom

        Regra única: um movimento é RUIM quando o valor do mês atual vai
        na direção errada vs o histórico:
          - Receita/Resultado: v_atual < histórico  → ruim
          - Despesa (negativo): v_atual < histórico (mais negativo) → ruim
        
        Ou seja: para TUDO, v_atual < média_histórica = piora econômica.
        Para despesas: -38k -39k -20k -17k → média_ant=-32k, v_atual=-17k
        -17k > -32k → MELHOROU → sem alerta. ✓
        """
        if _mes_atual is None or len(meses_ativos) < 2:
            return None, ""

        v_atual   = vals_por_mes.get(_mes_atual, 0.0)
        meses_ant = [m for m in meses_ativos if m < _mes_atual]
        vals_ant  = [vals_por_mes.get(m, 0.0) for m in meses_ant]

        if v_atual == 0.0 and all(v == 0.0 for v in vals_ant):
            return None, ""

        motivos = []
        nivel   = None

        def _upgrade(novo):
            nonlocal nivel
            if nivel != "alerta":
                nivel = novo

        # Para despesas (valores negativos), "maior" numericamente = menos gasto = bom.
        # Para receitas (valores positivos), "maior" = mais receita = bom.
        # Em ambos os casos: v_atual > referência = MELHOROU, v_atual < referência = PIOROU.
        # Usamos o valor bruto diretamente — a comparação numérica já é correta.

        # ── Sinal 1: MoM% ────────────────────────────────────────────────────
        v_prev = vals_ant[-1] if vals_ant else 0.0
        if v_prev != 0.0:
            # Variação relativa no espaço do valor exibido
            mom = (v_atual - v_prev) / abs(v_prev)
            # Determina se a variação é ruim:
            # Receita positiva: mom < 0 = caiu = ruim
            # Despesa negativa: mom < 0 = ficou mais negativa = aumentou = ruim
            # Logo: mom < 0 sempre significa piora, para qualquer tipo de linha
            if mom < 0 and not eh_resultado:
                if abs(mom) >= _ALERTA_MOM:
                    _upgrade("alerta")
                    motivos.append(f"MoM: variação de {abs(mom)*100:.1f}% vs mês anterior")
                elif abs(mom) >= _ATENCAO_MOM:
                    _upgrade("atencao")
                    motivos.append(f"MoM: variação de {abs(mom)*100:.1f}% vs mês anterior")

        # ── Sinal 2: desvio vs média dos meses anteriores ───────────────────
        if len(vals_ant) >= 2:
            media_ant = sum(vals_ant) / len(vals_ant)
            if media_ant != 0.0:
                desvio = (v_atual - media_ant) / abs(media_ant)
                # desvio < 0: ficou abaixo da média histórica
                # Receita: abaixo = ruim | Despesa negativa: abaixo (mais negativa) = ruim
                if desvio < 0 and not eh_resultado:
                    if abs(desvio) >= _ALERTA_MEDIA:
                        _upgrade("alerta")
                        motivos.append(f"Média: {abs(desvio)*100:.1f}% abaixo da média histórica")
                    elif abs(desvio) >= _ATENCAO_MEDIA:
                        _upgrade("atencao")
                        motivos.append(f"Média: {abs(desvio)*100:.1f}% abaixo da média histórica")

        # ── Sinal 3: tendência (3+ meses consecutivos na mesma direção) ─────
        if len(meses_ativos) >= 3:
            todos = [vals_por_mes.get(m, 0.0) for m in meses_ativos]
            direcoes = [1 if todos[i] > todos[i-1] else (-1 if todos[i] < todos[i-1] else 0)
                        for i in range(1, len(todos))]
            if len(direcoes) >= 2 and len(set(direcoes[-2:])) == 1 and direcoes[-1] != 0:
                n_meses = len(direcoes[-2:]) + 1
                # +1 = cada mês maior que anterior (receita subindo OU despesa ficando menos negativa = bom)
                # -1 = cada mês menor que anterior (receita caindo OU despesa aumentando = ruim)
                if direcoes[-1] == 1:
                    motivos.append(f"Tendência ↗ positiva por {n_meses} meses")
                else:
                    motivos.append(f"Tendência ↘ negativa por {n_meses} meses")
                    if not eh_resultado and nivel is None:
                        _upgrade("atencao")

        return nivel, " | ".join(motivos)

    def _badge_desvio(nivel, motivo):
        """Retorna HTML do ícone de alerta com tooltip."""
        if nivel == "alerta":
            return (
                f"<span title='{motivo}' style='"
                f"display:inline-block;width:7px;height:7px;border-radius:50%;"
                f"background:var(--c-danger,#E53E3E);margin-left:4px;vertical-align:middle;"
                f"cursor:help;flex-shrink:0;'></span>"
            )
        if nivel == "atencao":
            return (
                f"<span title='{motivo}' style='"
                f"display:inline-block;width:7px;height:7px;border-radius:50%;"
                f"background:var(--c-warning,#D97706);margin-left:4px;vertical-align:middle;"
                f"cursor:help;flex-shrink:0;'></span>"
            )
        return ""

    # processar_categoria: acumula e gera todas as linhas de um bloco DRE
    def _build_td_meses(vals_por_mes, cls_size="", mostrar_pct_mc=False,
                        sinal_contabil=+1, eh_resultado=False, divisor_por_mes=None):
        """Gera células <td> mensais. Se mostrar_pct_mc=True, inclui o % MC do mês.
        divisor_por_mes: dict {mes: valor} usado como divisor customizado para o %.
                         Se None, usa _mc_por_mes (comportamento padrão).
        No mês mais recente inclui badge de desvio quando aplicável."""
        nivel, motivo = _calcular_desvio(vals_por_mes,
                                         sinal_contabil=sinal_contabil,
                                         eh_resultado=eh_resultado)
        cells = ""
        for m in meses_ativos:
            v = vals_por_mes.get(m, 0.0)
            cor = _cor(v)
            extra = (" " + cls_size) if cls_size else ""
            eh_atual = (m == _mes_atual)
            badge = _badge_desvio(nivel, motivo) if eh_atual else ""

            # Fundo sutil de destaque no mês atual com desvio
            bg_style = ""
            if eh_atual and nivel == "alerta":
                bg_style = "background:rgba(229,62,62,.07);"
            elif eh_atual and nivel == "atencao":
                bg_style = "background:rgba(217,119,6,.07);"

            if mostrar_pct_mc:
                _div_map = divisor_por_mes if divisor_por_mes is not None else _mc_por_mes
                mc_m = _div_map.get(m, 0.0)
                if mc_m:
                    pct_v = (v / mc_m) * 100
                    pct_str = f"({abs(pct_v):.1f}%)" if pct_v < 0 else f"{pct_v:.1f}%"
                    pct_cor = "var(--c-danger,#C0392B)" if pct_v < 0 else "var(--c-text-4b,#1A7A4A)"
                    cells += (
                        f"<td class='td-mes{extra}' style='color:{cor};{bg_style}'>"
                        f"<span style='display:inline-flex;align-items:center;justify-content:flex-end;'>"
                        f"{_fmt(v)}{badge}</span>"
                        f"<div style='font-size:9px;color:{pct_cor};line-height:1.2;margin-top:1px;'>{pct_str}</div>"
                        f"</td>"
                    )
                else:
                    cells += (
                        f"<td class='td-mes{extra}' style='color:{cor};{bg_style}'>"
                        f"<span style='display:inline-flex;align-items:center;justify-content:flex-end;'>"
                        f"{_fmt(v)}{badge}</span>"
                        f"</td>"
                    )
            else:
                cells += (
                    f"<td class='td-mes{extra}' style='color:{cor};{bg_style}'>"
                    f"<span style='display:inline-flex;align-items:center;justify-content:flex-end;'>"
                    f"{_fmt(v)}{badge}</span>"
                    f"</td>"
                )
        return cells

    def processar_categoria(nome_dre, label_exib, sinal_pad):
        nonlocal acumulador, acumulador_orc, acumulador_orc_ano, acumulador_prov
        df_cat = df_f[df_f["dre"] == nome_dre]
        valor  = _soma(df_cat, sinal_pad) if not df_cat.empty else 0.0
        acumulador += valor

        # Orçado nível categoria
        orc_cat     = _soma_orc(df_cat, sinal_pad, nivel="cat", nome_dre=nome_dre)
        orc_ano_cat = _soma_orc_ano(sinal_pad, nome_dre=nome_dre, nivel="cat")
        prov_cat    = _soma_prov(sinal_pad, nome_dre=nome_dre, nivel="cat")
        acumulador_orc     += orc_cat
        acumulador_orc_ano += orc_ano_cat
        acumulador_prov    += prov_cat

        # Determina se esta categoria exibe % sobre MC
        exibe_pct = nome_dre in NOMES_COM_PCT
        mc = margem_contribuicao if exibe_pct else None

        # Valores mensais da categoria (com % MC se aplicável)
        vals_mes_cat = {m: _soma_mes(df_cat, sinal_pad, m) for m in meses_ativos}
        td_meses_cat = _build_td_meses(vals_mes_cat, mostrar_pct_mc=exibe_pct, sinal_contabil=sinal_pad)

        # chart_key da categoria (registra dados do ano inteiro para o mini-gráfico)
        cat_chart_key = f"cat::{nome_dre}"
        chart_data[cat_chart_key] = _chart_for(sinal_pad, label_exib,
                                               nome_dre=nome_dre, nivel="cat")

        if nome_dre in secoes:
            linhas_html.append(tr_secao(secoes[nome_dre]))

        # Não renderiza categoria com valor 0
        if valor == 0.0:
            if nome_dre in subtotais:
                label_sub, _ = subtotais[nome_dre]
                resumo[label_sub] = acumulador
                is_final = label_sub == "Resultado Liquido do Exercicio"
                linhas_html.append(tr_subtotal(label_sub, acumulador, is_final,
                                               mc=mc if exibe_pct else None,
                                               orc=acumulador_orc,
                                               orc_ano=acumulador_orc_ano,
                                               prov=acumulador_prov))
            return valor

        cat_id = next_id()
        linhas_html.append(tr_categoria(label_exib, valor, cat_id, mc=mc, orc=orc_cat,
                                        orc_ano=orc_ano_cat, prov=prov_cat,
                                        td_meses=td_meses_cat, chart_key=cat_chart_key))

        if not df_cat.empty:
            grupos = sorted(df_cat["Grupo"].unique())
            for grupo in grupos:
                df_g  = df_cat[df_cat["Grupo"] == grupo]
                val_g = _soma(df_g, sinal_pad)

                if val_g == 0.0:
                    continue

                vals_mes_grp = {m: _soma_mes(df_g, sinal_pad, m) for m in meses_ativos}
                td_meses_grp = _build_td_meses(vals_mes_grp, "td-val-sm", mostrar_pct_mc=exibe_pct, sinal_contabil=sinal_pad)

                orc_grp     = _soma_orc(df_cat, sinal_pad, nivel="grp", nome_dre=nome_dre, grupo=grupo)
                orc_ano_grp = _soma_orc_ano(sinal_pad, nome_dre=nome_dre, grupo=grupo, nivel="grp")
                prov_grp    = _soma_prov(sinal_pad, nome_dre=nome_dre, grupo=grupo, nivel="grp")

                subgrupos = sorted(df_g["SubGrupo"].unique())

                mostrar_grupo = not (
                    len(grupos) == 1 and
                    grupo.strip().upper() in (nome_dre.strip().upper(), label_exib.strip().upper())
                )

                if mostrar_grupo:
                    grp_id = next_id()
                    linhas_html.append(tr_grupo(grupo, val_g, grp_id, cat_id, mc=mc,
                                                orc=orc_grp, orc_ano=orc_ano_grp, prov=prov_grp,
                                                td_meses=td_meses_grp))
                    pai_subg = grp_id
                else:
                    grp_id   = cat_id
                    pai_subg = cat_id

                for subg in subgrupos:
                    df_sg  = df_g[df_g["SubGrupo"] == subg]
                    val_sg = _soma(df_sg, sinal_pad)

                    if val_sg == 0.0:
                        continue

                    vals_mes_sg = {m: _soma_mes(df_sg, sinal_pad, m) for m in meses_ativos}
                    td_meses_sg = _build_td_meses(vals_mes_sg, "td-val-sm", mostrar_pct_mc=exibe_pct, sinal_contabil=sinal_pad)

                    orc_sg     = _soma_orc(df_cat, sinal_pad, nivel="subg", nome_dre=nome_dre, grupo=grupo, subg=subg)
                    orc_ano_sg = _soma_orc_ano(sinal_pad, nome_dre=nome_dre, grupo=grupo, subg=subg, nivel="subg")
                    prov_sg    = _soma_prov(sinal_pad, nome_dre=nome_dre, grupo=grupo, subg=subg, nivel="subg")

                    ref_nome = grupo if mostrar_grupo else label_exib
                    mostrar_subg = not (
                        len(subgrupos) == 1 and
                        subg.strip().upper() in (ref_nome.strip().upper(), nome_dre.strip().upper(), label_exib.strip().upper())
                    )

                    if mostrar_subg:
                        sg_id = next_id()
                        linhas_html.append(tr_subgrupo(subg, val_sg, sg_id, pai_subg, mc=mc,
                                                       orc=orc_sg, orc_ano=orc_ano_sg, prov=prov_sg,
                                                       td_meses=td_meses_sg))
                        pai_td = sg_id
                    else:
                        pai_td = pai_subg

                    tds = (
                        df_sg.groupby("Tipo_Documento", dropna=False)
                        .apply(lambda g: _soma(g, sinal_pad), include_groups=False)
                        .reset_index().rename(columns={0: "v"})
                        .sort_values("Tipo_Documento")
                    )
                    for _, r in tds[tds["v"] != 0].iterrows():
                        td_nome = r["Tipo_Documento"]
                        modal_key = f"{nome_dre}|||{td_nome}"
                        orc_td     = _soma_orc(df_cat, sinal_pad, nivel="td", nome_dre=nome_dre, grupo=grupo, subg=subg, td=td_nome)
                        orc_ano_td = _soma_orc_ano(sinal_pad, nome_dre=nome_dre, grupo=grupo, subg=subg, td=td_nome, nivel="td")
                        prov_td    = _soma_prov(sinal_pad, nome_dre=nome_dre, grupo=grupo, subg=subg, td=td_nome, nivel="td")

                        df_td = df_sg[df_sg["Tipo_Documento"] == td_nome]
                        vals_mes_td = {m: _soma_mes(df_td, sinal_pad, m) for m in meses_ativos}
                        td_meses_td = _build_td_meses(vals_mes_td, "td-val-xs", mostrar_pct_mc=exibe_pct, sinal_contabil=sinal_pad)

                        cols_exib = ["data", "Empresa", "cp_ms", "Tipo_Documento",
                                     "Grupo", "SubGrupo",
                                     "valor_real_quitado", "valor_real_aberto", "valor_total"]
                        cols_ok = [c for c in cols_exib if c in df_td.columns]
                        linhas_det = []
                        for _, row in df_td[cols_ok].iterrows():
                            d = {}
                            for c in cols_ok:
                                v = row[c]
                                if hasattr(v, "isoformat"):
                                    d[c] = v.strftime("%d/%m/%Y") if not pd.isnull(v) else ""
                                elif isinstance(v, float):
                                    d[c] = v
                                else:
                                    d[c] = str(v)
                            d["_saldo"] = float((df_td.loc[row.name, "valor_total"]) * (
                                row.get("sinal", sinal_pad) if "sinal" in df_td.columns else sinal_pad
                            )) if "valor_total" in df_td.columns else 0.0
                            linhas_det.append(d)
                        detalhe_data[modal_key] = {
                            "titulo": td_nome,
                            "total": float(r["v"]),
                            "linhas": linhas_det,
                            "cols": cols_ok,
                        }

                        linhas_html.append(tr_td(td_nome, r["v"], pai_td, modal_key, mc=mc,
                                                 orc=orc_td, orc_ano=orc_ano_td, prov=prov_td,
                                                 td_meses_arg=td_meses_td))

        if nome_dre in subtotais:
            label_sub, _ = subtotais[nome_dre]
            resumo[label_sub] = acumulador
            is_final = label_sub == "Resultado Liquido do Exercicio"
            orc_sub = acumulador_orc
            acc_by_mes = {}
            for nome2, _, sp2 in estrutura:
                for m in meses_ativos:
                    df2 = df_f[df_f["dre"] == nome2]
                    acc_by_mes[m] = acc_by_mes.get(m, 0.0) + _soma_mes(df2, sp2, m)
                if nome2 == nome_dre:
                    break
            _eh_mc = (label_sub == "Margem de Contribuição / Lucro Bruto")
            _div_mes = _vb_por_mes if _eh_mc else None
            td_meses_sub = _build_td_meses(acc_by_mes, mostrar_pct_mc=(exibe_pct or _eh_mc),
                                           eh_resultado=True, divisor_por_mes=_div_mes)
            mc_sub = _venda_bruta_total if _eh_mc else (mc if exibe_pct else None)

            # Constrói chart_data para o subtotal (real + orçado, ano inteiro,
            # somando todas as categorias da DRE até este subtotal)
            sub_chart_key = f"sub::{label_sub}"
            real_full = {str(m): 0.0 for m in range(1, 13)}
            orc_full  = {str(m): 0.0 for m in range(1, 13)}
            for _n, _, _sp in estrutura:
                _cat_chart = chart_data.get(f"cat::{_n}")
                if _cat_chart:
                    for _m in range(1, 13):
                        real_full[str(_m)] += _cat_chart["real"].get(str(_m), 0.0)
                        orc_full[str(_m)]  += _cat_chart["orc"].get(str(_m), 0.0)
                if _n == nome_dre:
                    break
            chart_data[sub_chart_key] = {"label": label_sub, "real": real_full, "orc": orc_full}

            linhas_html.append(tr_subtotal(label_sub, acumulador, is_final, mc=mc_sub,
                                           orc=orc_sub, orc_ano=acumulador_orc_ano,
                                           prov=acumulador_prov, td_meses=td_meses_sub,
                                           chart_key=sub_chart_key))

        return valor

    # loop principal
    for nome_dre, label_exib, sinal_pad in estrutura:
        if nome_dre in dres_no_arquivo:
            processar_categoria(nome_dre, label_exib, sinal_pad)
            dres_mapeadas.add(nome_dre)
        else:
            if nome_dre in secoes:
                linhas_html.append(tr_secao(secoes[nome_dre]))
            acumulador += 0.0
            if nome_dre in subtotais:
                label_sub, _ = subtotais[nome_dre]
                resumo[label_sub] = acumulador
                is_final = label_sub == "Resultado Liquido do Exercicio"
                linhas_html.append(tr_subtotal(label_sub, acumulador, is_final,
                                               orc=acumulador_orc, orc_ano=acumulador_orc_ano,
                                               prov=acumulador_prov))

    if fora_dre in dres_no_arquivo:
        linhas_html.append(tr_secao("MOVIMENTAÇÕES DE CAIXA"))
        processar_categoria(fora_dre, "Movimentações de Caixa", +1)
        dres_mapeadas.add(fora_dre)

    orfas = dres_no_arquivo - dres_mapeadas - {"Sem Classificacao"}
    if orfas and mostrar_orfaos:
        linhas_html.append(tr_secao("CONTAS SEM POSICAO NO DRE"))
        for conta in sorted(orfas):
            processar_categoria(conta, conta, -1)
            dres_mapeadas.add(conta)

    import json as _json

    # ── Pós-processamento: resumo_meses (subtotais mês a mês para AV/AH) ───────
    # Recalcula fora de processar_categoria para evitar problemas com early-returns.
    _acc_m = {m: 0.0 for m in meses_ativos}
    for _nd, _, _sp in estrutura:
        _df2 = df_f[df_f["dre"] == _nd]
        for _m in meses_ativos:
            _acc_m[_m] = _acc_m[_m] + _soma_mes(_df2, _sp, _m)
        if _nd in subtotais:
            _lsub, _ = subtotais[_nd]
            resumo_meses[_lsub] = dict(_acc_m)

    # Sanitiza strings com surrogates inválidos antes de serializar
    def _sanitize(obj, _visited=None):
        if _visited is None:
            _visited = set()
        oid = id(obj)
        if oid in _visited:
            return obj
        _visited.add(oid)
        if isinstance(obj, str):
            # Remove apenas surrogates isolados (inválidos em UTF-8),
            # preservando emojis e outros caracteres multibyte válidos
            return obj.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
        if isinstance(obj, dict):
            return {_sanitize(k, _visited): _sanitize(v, _visited) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_sanitize(i, _visited) for i in obj]
        return obj

    # Serializa dados de detalhe — ensure_ascii=True evita problemas de encoding;
    # escapa </script> para nao fechar o bloco <script> prematuramente
    detalhe_json = _json.dumps(_sanitize(detalhe_data), ensure_ascii=True, default=str)
    detalhe_json_safe = detalhe_json.replace("</" , "<\\/")

    # Serializa dados de gráfico (evolução mensal por linha) e threshold de alerta
    chart_json = _json.dumps(_sanitize(chart_data), ensure_ascii=True, default=str)
    chart_json_safe = chart_json.replace("</", "<\\/")
    var_threshold_safe = float(var_threshold)

    # Nomes amigáveis das colunas
    COL_LABELS = {
        "data": "Data", "Empresa": "Empresa", "cp_ms": "Cenário",
        "Tipo_Documento": "Tipo Doc.", "Grupo": "Grupo", "SubGrupo": "SubGrupo",
        "valor_real_quitado": "Vl. Quitado (R$)", "valor_real_aberto": "Vl. Aberto (R$)",
        "valor_total": "Vl. Total (R$)",
    }

    tbody  = "\n".join(linhas_html)
    # Conta apenas linhas visíveis de nível 1 (seções + categorias + subtotais)
    # Grupos/subgrupos/folhas começam collapsed, não contribuem para a altura inicial
    n_visiveis = sum(
        1 for h in linhas_html
        if any(cls in h for cls in ("tr-sec", "tr-cat", "tr-subtotal", "tr-total-final"))
    )
    altura_dre = max(500, n_visiveis * 36 + 80) + 260  # +260px para o painel de KPIs embaixo

    # Dados para o painel lateral (KPIs + gráficos)
    venda_bruta = sum(
        _soma(df_f[df_f["dre"] == c], s)
        for c, s in {"VENDA BRUTA": +1}.items()
        if not df_f[df_f["dre"] == c].empty
    )
    panel_data = {
        "venda_bruta":          venda_bruta,
        "margem_contribuicao":  margem_contribuicao,
        "pct_mc_venda":         (margem_contribuicao / venda_bruta * 100) if venda_bruta else 0,
        "resumo":               resumo,
        "resumo_meses":         {k: {str(m): v for m, v in mv.items()} for k, mv in resumo_meses.items()},
        "vb_por_mes":           {str(m): v for m, v in _vb_por_mes.items()},
        "meses_ativos":         [str(m) for m in meses_ativos],
    }
    venda_bruta = sum(
        _soma(df_f[df_f["dre"] == c], s)
        for c, s in {"VENDA BRUTA": +1}.items()
        if not df_f[df_f["dre"] == c].empty
    )
    panel_data = {
        "venda_bruta":          venda_bruta,
        "margem_contribuicao":  margem_contribuicao,
        "pct_mc_venda":         (margem_contribuicao / venda_bruta * 100) if venda_bruta else 0,
        "resumo":               resumo,
        "resumo_meses":         {k: {str(m): v for m, v in mv.items()} for k, mv in resumo_meses.items()},
        "vb_por_mes":           {str(m): v for m, v in _vb_por_mes.items()},
        "meses_ativos":         [str(m) for m in meses_ativos],
    }

    html = ("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=display=swap" rel="stylesheet">
""" + _build_theme_css(tema) + """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; background: var(--c-bg-3,#060D1A); font-family: var(--font-sans, 'Inter', sans-serif); font-size: 13px; color: var(--c-text-1b,#CBD5E1); }

/* ── LAYOUT COMMAND CENTER ───────────────────────────── */
.cc-shell {
  display: grid;
  grid-template-columns: 1fr 290px;
  gap: 0;
  border: 1px solid var(--c-border-1,#1A2E4A);
  border-radius: 10px;
  overflow: visible;
  box-shadow: 0 4px 32px rgba(0,0,0,.5);
  align-items: start;
  background: var(--c-bg-2,#0A1628);
}

/* ── COLUNA ESQUERDA — DRE ───────────────────────────── */
.cc-dre { overflow: hidden; border-right: 1px solid var(--c-border-1,#1A2E4A); border-radius: 10px 0 0 10px; background: var(--c-bg-1,#080F1C); }

table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.td-label { width: 57%; padding: 0 14px; text-align: left; border: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-pct   { width: 12%; padding: 0 8px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 11px; font-style: italic; color: var(--c-text-3f,#64748B); }
.td-val   { width: 22%; padding: 0 14px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums;
            font-feature-settings: "tnum" 1, "kern" 1; letter-spacing: 0.01em; }
.td-orc   { width: 18%; padding: 0 10px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums;
            font-feature-settings: "tnum" 1; color: var(--c-text-4d,#3D5A78); font-size: 14px;
            font-weight: 400; letter-spacing: 0.01em; }
.td-var   { width: 10%; padding: 0 10px; text-align: right; border: none;
            white-space: nowrap; font-size: 14px; letter-spacing: 0.02em; }
.td-exe   { width: 9%; padding: 0 8px; text-align: right; border: none;
            white-space: nowrap; font-size: 11px; font-style: italic;
            color: var(--c-text-3f,#64748B); letter-spacing: 0.01em; }
.td-prov  { width: 10%; padding: 0 10px; text-align: right; border: none;
            white-space: nowrap; font-size: 13px; font-style: italic;
            color: var(--c-text-3f,#64748B); letter-spacing: 0.01em; border-left: 1px solid var(--c-border-1,#1E293B); }
.td-label { width: 40%; }
.td-pct   { width: 10%; }

/* cabeçalho de colunas */
thead tr { background: var(--c-bg-3,#060D1A); border-bottom: 1px solid var(--c-border-1,#1A2E4A); }
thead th { padding: 8px 14px; font-size: 9.5px; font-weight: 700; text-transform: uppercase;
           letter-spacing: .12em; color: var(--c-text-4d,#3D5A78); text-align: right; white-space: nowrap; border: none; }
thead th:first-child { text-align: left; color: var(--c-text-3d,#4A6680); }
thead th.td-mes { color: var(--c-text-4b,#2A4560); font-size: 9px; }

/* seções */
.tr-sec { background: var(--c-bg-3,#06101E); }
.td-sec { padding: 6px 14px; color: var(--c-text-4,#2A5080); font-size: 9px; font-weight: 700;
          letter-spacing: 0.18em; text-transform: uppercase; border: none; border-top: 1px solid var(--c-bg-4,var(--c-bg-4,#0F1E30)); }

/* categoria nível 1 */
.tr-cat { background: var(--c-bg-2,#0B1627); border-top: 1px solid var(--c-border-1,#111E30); cursor: pointer; transition: background .12s; }
.tr-cat:hover { background: var(--c-bg-4,#0E1C33); }
.td-cat-label { padding-top: 9px; padding-bottom: 9px; font-weight: 600; color: var(--c-text-1,#C8D9EC); font-size: 13px; }

/* grupo nível 2 */
.tr-grp  { display: none; background: var(--c-bg-1,#09131F); border-top: 1px solid var(--c-bg-5,#0F1A28); cursor: pointer; transition: background .12s; }
.tr-grp:hover { background: var(--c-bg-5,#0C1828); }
.td-grp-label { padding: 7px 14px 7px 32px; color: var(--c-text-2b,#8FAEC8); font-weight: 600; font-size: 12.5px; }

/* subgrupo nível 3 */
.tr-subg { display: none; background: var(--c-bg-3,#07101C); border-top: 1px solid var(--c-bg-5,#0D1825); cursor: pointer; transition: background .12s; }
.tr-subg:hover { background: var(--c-bg-2,#0A1526); }
.td-subg-label { padding: 6px 14px 6px 50px; color: var(--c-text-3,#607A90); font-size: 12px; }

/* folha nível 4 */
.tr-leaf { display: none; background: var(--c-bg-3,#060E1A); border-top: 1px solid var(--c-bg-5,#0C1824); cursor: pointer; transition: background .12s; }
.tr-leaf:hover { background: var(--c-bg-2,#091422); }
.td-leaf-label { padding: 5px 14px 5px 68px; color: var(--c-text-3b,#3D6080); font-size: 11.5px; }

/* valores */
.td-val     { padding-top: 9px; padding-bottom: 9px; font-weight: 600; font-size: 16px;
              font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }
.td-val-sm  { padding-top: 7px; padding-bottom: 7px; font-weight: 500; font-size: 15px;
              font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }
.td-val-xs  { padding-top: 5px; padding-bottom: 5px; font-weight: 400; font-size: 14.5px;
              font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }

/* cores dos valores — sobrescreve o inline do Python */
.pos-val { color: var(--c-success,#22C55E) !important; }
.neg-val { color: var(--c-danger,#EF4444) !important; }

/* subtotais */
.tr-subtotal { background: var(--c-bg-2,#0D1E32); border-top: 1px solid var(--c-border-2,#1A3050); border-bottom: 1px solid var(--c-border-2,#1A3050); }
.td-subtotal-label { padding: 8px 14px; color: var(--c-text-2b,#A8C0D8); font-weight: 700; font-size: 12.5px; }
.td-subtotal-val   { padding: 8px 14px; font-weight: 700; font-size: 12.5px; }
.tr-total-final { background: var(--c-bg-2,#0A1E3A); border-top: 2px solid var(--c-border-2,#1A3A60); }
.td-total-label { padding: 12px 14px; color: var(--c-text-1,#E2E8F0); font-weight: 700; font-size: 13px; }
.td-total-val   { padding: 12px 14px; font-weight: 700; font-size: 16px; }

.td-mes {
  width: 80px; min-width: 70px; padding: 3px 8px; text-align: right; border: none;
  font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1;
  color: var(--c-text-4d,#3D5A78); font-size: 14px; font-weight: 400; background: rgba(6,13,26,.3);
  border-left: 1px solid var(--c-bg-4,var(--c-bg-4,#0F1E30));
  vertical-align: middle; line-height: 1.3;
}
/* Meses escondidos */
.meses-off .td-mes { display: none !important; }
.meses-off th.td-mes { display: none !important; }

/* seta */
.arrow    { display: inline-block; width: 14px; color: var(--c-text-4b,#2A4560); font-size: 10px;
            transition: transform .15s; transform: rotate(-90deg); margin-right: 2px; }
.arrow-sm { width: 12px; font-size: 9px; }

/* botão meses */
.btn-meses {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--c-bg-2,#0C1A2C); border: 1px solid var(--c-border-2,#1A3050); border-radius: 5px;
  color: var(--c-accent,#4A7FA8); font-size: 10px; font-weight: 700; letter-spacing: .08em;
  padding: 5px 10px; cursor: pointer; margin: 6px 14px; text-transform: uppercase;
  transition: all .15s;
}
.btn-meses:hover { background: var(--c-bg-4,#0F2040); border-color: var(--c-text-4,#2A5080); color: var(--c-accent-bright,#7DD3FC); }

/* ── COLUNA DIREITA — PAINEL ─────────────────────────── */
.cc-panel {
  background: var(--c-bg-2,#0A1628);
  display: flex; flex-direction: column;
  overflow-y: auto;
  position: sticky;
  top: 0;
  max-height: 100vh;
  border-radius: 0 10px 10px 0;
}

/* título do painel */
.cc-panel-top {
  padding: 10px 12px 8px;
  border-bottom: 1px solid var(--c-border-1,#1A2E4A);
  background: var(--c-bg-3,#060D1A);
  border-radius: 0 10px 0 0;
}
.cc-panel-top-title {
  font-size: 8.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .16em;
  color: var(--c-text-4,#2A5080); margin-bottom: 1px;
}
.cc-panel-top-sub {
  font-size: 9.5px; color: var(--c-text-4d,#3D5A78); font-weight: 500;
}

/* KPI cards */
.cc-kpi-list { padding: 10px 10px 6px; display: flex; flex-direction: column; gap: 6px; }
.cc-kpi {
  background: var(--c-bg-5,#0C1825); border-radius: 7px; padding: 9px 11px;
  border: 1px solid var(--c-bg-4,#152030);
  border-left: 3px solid var(--c-border-2,#1A3A60);
}
.cc-kpi-label { font-size: 9.5px; color: var(--c-text-4d,#3D5A78); font-weight: 700; text-transform: uppercase;
                letter-spacing: .07em; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cc-kpi-val { font-size: 17px; font-weight: 500; line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
              font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; letter-spacing: -0.01em; }
.cc-kpi-val.pos { color: var(--c-success,#22C55E); }
.cc-kpi-val.neg { color: var(--c-danger,#EF4444); }
.cc-kpi-sub { font-size: 9.5px; color: var(--c-text-4b,#2A4560); margin-top: 3px; }
.cc-kpi-sub b { color: var(--c-text-3b,#3D6080); }

/* Divisor de painel */
.cc-panel-title {
  font-size: 8.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .14em;
  color: var(--c-text-4b,#2A4560); padding: 10px 12px 5px; border-top: 1px solid var(--c-bg-4,var(--c-bg-4,#0F1E30)); margin-top: 2px;
  background: var(--c-bg-3,#060D1A);
}

/* Barras de composição */
.cc-bar-list { padding: 0 10px 10px; display: flex; flex-direction: column; gap: 10px; }
.cc-bar-item { }
.cc-bar-header { display: flex; justify-content: space-between; align-items: baseline;
                 font-size: 11px; color: var(--c-text-3,#607A90); margin-bottom: 4px; font-weight: 500; }
.cc-bar-header span:last-child { font-size: 11px; font-weight: 700; font-variant-numeric: tabular-nums; color: var(--c-text-2b,#8FAEC8); }
.cc-bar-track { height: 6px; background: var(--c-bg-4,var(--c-bg-4,#0F1E30)); border-radius: 4px; overflow: hidden; }
.cc-bar-fill  { height: 100%; border-radius: 4px; transition: width .5s ease; }

/* Cascata */
.cc-waterfall { padding: 0 10px 14px; }
.cc-wf-grid { display: flex; align-items: flex-end; gap: 5px; height: 110px; }
.cc-wf-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; min-width: 0; }
.cc-wf-bar { width: 100%; border-radius: 3px 3px 0 0; }
.cc-wf-lbl { font-size: 8.5px; color: var(--c-text-4d,#3D5A78); text-align: center; white-space: nowrap;
             overflow: hidden; text-overflow: ellipsis; width: 100%; font-weight: 700; }
.cc-wf-val { font-size: 7.5px; color: var(--c-text-4c,#2A4060); text-align: center; white-space: nowrap; font-weight: 500;
             font-family: 'Inter', sans-serif; }

/* ── MODAL ───────────────────────────────────────────── */
#modal-overlay {
  display: none; position: absolute; top: 0; left: 0; width: 100%;
  background: rgba(4,8,18,.75); backdrop-filter: blur(4px);
  z-index: 9999;
}
#modal-overlay.open { display: block; }
#modal-box {
  background: var(--c-bg-2,#0A1628); border: 1px solid var(--c-border-2,#1A3050); border-radius: 12px;
  box-shadow: 0 24px 64px rgba(0,0,0,.6);
  width: 94%; max-width: 1020px; max-height: 500px;
  display: flex; flex-direction: column; overflow: hidden;
  animation: mIn .18s ease;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
@keyframes mIn { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
#modal-header { background: var(--c-bg-3,#060D1A); border-bottom: 1px solid var(--c-border-2,#1A3050); padding: 14px 20px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
#modal-title  { color: var(--c-text-1b,#CBD5E1); font-size: 14px; font-weight: 700; }
#modal-total  { color: var(--c-text-3b,#3D6080); font-size: 11.5px; margin-top: 2px; }
#modal-close  { background: none; border: none; color: var(--c-text-4,#2A5080); font-size: 22px; cursor: pointer; line-height: 1; padding: 0 4px; }
#modal-close:hover { color: var(--c-accent-bright,#7DD3FC); }
#modal-body { overflow-y: auto; flex: 1; background: var(--c-bg-1,#080F1C); }
#modal-table { width: 100%; border-collapse: collapse; font-size: 12px; }
#modal-table thead th { position: sticky; top: 0; background: var(--c-bg-3,#060D1A); padding: 8px 12px;
  text-align: left; font-weight: 700; color: var(--c-text-4,#2A5080); font-size: 9.5px;
  text-transform: uppercase; letter-spacing: .08em; border-bottom: 1px solid var(--c-border-1,#1A2E4A); white-space: nowrap; }
#modal-table thead th.num { text-align: right; }
#modal-table tbody tr { border-bottom: 1px solid var(--c-bg-5,#0C1828); }
#modal-table tbody tr:hover { background: var(--c-bg-5,#0A1525); }
#modal-table tbody td { padding: 7px 12px; color: var(--c-text-3,#607A90); }
#modal-table tbody td.num { text-align: right; font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; white-space: nowrap; font-weight: 500; }
#modal-table tbody td.pos { color: var(--c-success,#22C55E); }
#modal-table tbody td.neg { color: var(--c-danger,#EF4444); }
#modal-footer { background: var(--c-bg-3,#060D1A); border-top: 1px solid var(--c-border-1,#1A2E4A); padding: 9px 20px;
  display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: var(--c-text-4b,#2A4560); }

/* ── ALERTAS DE LINHA (variação Real vs Orçado vs threshold) ──
   Verde   → Real superou orçado em ≥T%  (favorável)
   Amarelo → Dentro da banda ±T%          (dentro da tolerância)
   Vermelho→ Real ficou ≥T% pior          (desfavorável)
*/
.row-alert-vermelho {
  position: relative;
  box-shadow: inset 3px 0 0 0 var(--c-danger,#EF4444) !important;
}
.row-alert-vermelho .td-label { background: rgba(239, 68, 68, .05) !important; }

.row-alert-verde {
  position: relative;
  box-shadow: inset 3px 0 0 0 var(--c-success,#22C55E) !important;
}
.row-alert-verde .td-label { background: rgba(34, 197, 94, .04) !important; }

/* Amarelo é discreto: linha sem barra lateral (apenas o badge inline) */
.row-alert-amarelo { position: relative; }

.alert-badge { user-select: none; }
.alert-badge.alert-vermelho:hover { color: var(--c-danger,#F87171) !important; }
.alert-badge.alert-verde:hover    { color: var(--c-success,#4ADE80) !important; }
.alert-badge.alert-amarelo:hover  { color: var(--c-warning,#FBBF24) !important; opacity: 1 !important; }

/* ── ÍCONE DE GRÁFICO INLINE ── */
.chart-icon { user-select: none; }
.chart-icon:hover { color: var(--c-accent,#60A5FA) !important; opacity: 1 !important; }

/* ── MODAL DE GRÁFICO ── */
#chart-modal-overlay {
  display: none; position: absolute; top: 0; left: 0; width: 100%;
  background: rgba(4,8,18,.75); backdrop-filter: blur(4px);
  z-index: 9998;
}
#chart-modal-overlay.open { display: block; }
#chart-modal-box {
  background: var(--c-bg-2,#0A1628); border: 1px solid var(--c-border-2,#1A3050); border-radius: 12px;
  box-shadow: 0 24px 64px rgba(0,0,0,.6);
  width: 92%; max-width: 880px;
  display: flex; flex-direction: column; overflow: hidden;
  animation: mIn .18s ease;
  position: absolute; left: 50%; transform: translateX(-50%);
}
#chart-modal-header {
  background: var(--c-bg-3,#060D1A); border-bottom: 1px solid var(--c-border-2,#1A3050);
  padding: 14px 20px; display: flex; align-items: center;
  justify-content: space-between; flex-shrink: 0;
}
#chart-modal-title { color: var(--c-text-1b,#CBD5E1); font-size: 14px; font-weight: 700; }
#chart-modal-sub   { color: var(--c-text-3b,#3D6080); font-size: 11.5px; margin-top: 2px; }
#chart-modal-close { background: none; border: none; color: var(--c-text-4,#2A5080); font-size: 22px; cursor: pointer; line-height: 1; padding: 0 4px; }
#chart-modal-close:hover { color: var(--c-accent-bright,#7DD3FC); }
#chart-modal-body { padding: 18px 20px 14px; background: var(--c-bg-1,#080F1C); }
#chart-modal-legend {
  display: flex; gap: 18px; padding: 0 20px 10px;
  font-size: 11px; color: var(--c-text-3,#607A90); background: var(--c-bg-1,#080F1C);
}
#chart-modal-legend .lg-it { display: inline-flex; align-items: center; gap: 6px; }
#chart-modal-legend .lg-sw { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
#chart-modal-footer {
  background: var(--c-bg-3,#060D1A); border-top: 1px solid var(--c-border-1,#1A2E4A);
  padding: 8px 20px; font-size: 11px; color: var(--c-text-4b,#2A4560);
}
.chart-svg { width: 100%; height: 280px; display: block; }
.chart-svg .bar-real { fill: var(--c-accent,#3B82F6); }
.chart-svg .bar-orc  { fill: var(--c-text-3e,#475569); }
.chart-svg .grid-line { stroke: var(--c-border-1,#1A2E4A); stroke-width: 1; stroke-dasharray: 2,3; }
.chart-svg .axis-text { fill: var(--c-text-3d,#4A6680); font-family: 'Inter', sans-serif; font-size: 10px; }
.chart-svg .bar-label { fill: var(--c-text-3,#607A90); font-family: 'Inter', sans-serif; font-size: 9px; }
</style>

<script>
(function() {
  function r() {
    try { window.parent.document.querySelectorAll('iframe').forEach(function(f) {
      if (f.contentWindow === window) { f.style.width='100%'; if(f.parentElement) f.parentElement.style.width='100%'; }
    }); } catch(e) {}
  }
  document.readyState==='loading' ? document.addEventListener('DOMContentLoaded',r) : r();
  window.addEventListener('load',r);

  // Força fundo escuro no iframe e no seu container pai
  function forceDarkBg() {
    try {
      document.documentElement.style.background = 'var(--c-bg-5,#0B1120)';
      document.body.style.background = 'var(--c-bg-5,#0B1120)';
      window.parent.document.querySelectorAll('iframe').forEach(function(f) {
        if (f.contentWindow === window) {
          f.style.background = 'var(--c-bg-5,#0B1120)';
          f.style.colorScheme = 'dark';
          if (f.parentElement) f.parentElement.style.background = 'var(--c-bg-5,#0B1120)';
        }
      });
    } catch(e) {}
  }
  forceDarkBg();
  document.addEventListener('DOMContentLoaded', forceDarkBg);
  window.addEventListener('load', forceDarkBg);

  // Auto-resize iframe to actual content height
  function sendHeight() {
    if (!document.body) return;
    var h = document.body.scrollHeight;
    try {
      window.parent.document.querySelectorAll('iframe').forEach(function(f) {
        if (f.contentWindow === window) { f.style.height = h + 'px'; }
      });
    } catch(e) {}
  }
  window.addEventListener('load', sendHeight);
  if (typeof ResizeObserver !== 'undefined') {
    // Garante que o body existe antes de observar
    var observer = new ResizeObserver(sendHeight);
    if (document.body) {
      observer.observe(document.body);
    } else {
      document.addEventListener('DOMContentLoaded', function() {
        observer.observe(document.body);
      });
    }
  }
})();

var DETALHE = """ + detalhe_json_safe + """;
var CHART_DATA = """ + chart_json_safe + """;
var VAR_THRESHOLD = """ + str(var_threshold_safe) + """;
var NUM_COLS = ["valor_real_quitado","valor_real_aberto","valor_total"];
var COL_LABELS = {"data":"Data","Empresa":"Empresa","cp_ms":"Cenário","Tipo_Documento":"Tipo Doc.",
  "Grupo":"Grupo","SubGrupo":"SubGrupo","valor_real_quitado":"Vl. Quitado (R$)",
  "valor_real_aberto":"Vl. Aberto (R$)","valor_total":"Vl. Total (R$)"};

function fmtBR(v,d){ if(typeof v!=='number') return v;
  var a=Math.abs(v).toLocaleString('pt-BR',{minimumFractionDigits:d||2,maximumFractionDigits:d||2});
  return v<0?'('+a+')':a; }

</script>
</head>
<body>

<script>
  // A Delegação de Eventos intercepta o clique com precisão milimétrica em qualquer navegador
  // Usamos window.addEventListener para garantir captura em alguns ambientes de iframe
  window.addEventListener('click', function(e) {
    // Verifica se o utilizador clicou numa linha de detalhe
    var leaf = e.target.closest('.tr-leaf');
    if (!leaf) return;
    
    // Impede que o clique se propague (evita conflitos com outros handlers)
    e.preventDefault();
    e.stopPropagation();

    var key = leaf.getAttribute('data-key');
    if (!key) return;

    var d = DETALHE[key];
    if (!d) { console.warn('Modal key not found:', key); return; }

    // Preenche os textos e a tabela do modal
    document.getElementById('modal-title').textContent = d.titulo;
    document.getElementById('modal-total').textContent = 'Total no período: ' + fmtBR(d.total, 2);
    
    var cols = d.cols;
    var thead = '<tr>'; 
    cols.forEach(function(c) { 
      var n = NUM_COLS.indexOf(c) >= 0;
      thead += '<th class="' + (n ? 'num' : '') + '">' + (COL_LABELS[c] || c) + '</th>'; 
    }); 
    thead += '</tr>';
    document.getElementById('modal-thead').innerHTML = thead;
    
    var rows = ''; 
    d.linhas.forEach(function(row) { 
      rows += '<tr>';
      cols.forEach(function(c) { 
        var n = NUM_COLS.indexOf(c) >= 0; 
        var v = row[c];
        var cls = 'class="' + (n ? 'num ' + (v < 0 ? 'neg' : (v > 0 ? 'pos' : '')) : '') + '"';
        rows += '<td ' + cls + '>' + (n ? fmtBR(v, 2) : (v || '')) + '</td>'; 
      }); 
      rows += '</tr>'; 
    });
    document.getElementById('modal-tbody').innerHTML = rows ||
      '<tr><td colspan="' + cols.length + '" style="padding:20px;text-align:center;color:var(--c-text-2,#94A3B8)">Nenhuma linha</td></tr>';
    document.getElementById('modal-count').textContent = d.linhas.length + ' registro' + (d.linhas.length !== 1 ? 's' : '');

    // 1. O SEGREDO DO FUNDO: Força o overlay escuro a cobrir a altura total da DRE
    var overlay = document.getElementById('modal-overlay');
    overlay.style.height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) + 'px';

    // 2. O SEGREDO DA POSIÇÃO: Coloca a caixa do modal acompanhando a coordenada Y do rato
    var box = document.getElementById('modal-box');
    if (e && (e.pageY || e.clientY)) {
      var topPos = (e.pageY || e.clientY) - 100; 
      if (topPos < 20) topPos = 20; 
      box.style.top = topPos + 'px';
    } else {
      box.style.top = '50px'; // Fallback
    }

    // A MÁGICA AQUI: Força o fundo escuro a cobrir a tabela inteira!
    overlay.style.height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) + 'px';
    overlay.classList.add('open');
  });
function closeModal(){ document.getElementById('modal-overlay').classList.remove('open'); }
function closeChartModal(){ document.getElementById('chart-modal-overlay').classList.remove('open'); }
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){ closeModal(); closeChartModal(); }
});

/* ── MODAL DE GRÁFICO: evolução mensal Real vs Orçado ── */
var MESES_CURTO_JS = ['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

function _fmtChartLabel(v){
  var a = Math.abs(v);
  var s;
  if (a >= 1e6) s = (a/1e6).toFixed(1).replace('.',',') + 'M';
  else if (a >= 1e3) s = (a/1e3).toFixed(0) + 'k';
  else s = a.toFixed(0);
  return v < 0 ? '-' + s : s;
}

function _fmtChartFull(v){
  var s = Math.abs(v).toLocaleString('pt-BR', {minimumFractionDigits:0,maximumFractionDigits:0});
  return v < 0 ? '(R$ ' + s + ')' : 'R$ ' + s;
}

function showChart(key){
  var d = CHART_DATA[key];
  if(!d){ console.warn('Chart key not found:', key); return; }

  // Coleta valores de 1 a 12, calcula faixa para escala
  var meses = [];
  var maxAbs = 0;
  for(var m=1; m<=12; m++){
    var mk = String(m);
    var r = (d.real && d.real[mk]) || 0;
    var o = (d.orc  && d.orc[mk])  || 0;
    meses.push({m:m, real:r, orc:o});
    maxAbs = Math.max(maxAbs, Math.abs(r), Math.abs(o));
  }
  if(maxAbs === 0) maxAbs = 1; // evita divisão por zero quando tudo for zero

  // Decisão de layout do SVG
  var W = 800, H = 280;
  var padL = 50, padR = 20, padT = 18, padB = 36;
  var plotW = W - padL - padR;
  var plotH = H - padT - padB;

  // Detecta se há valores negativos para usar eixo zero centralizado
  var minVal = 0, maxVal = 0;
  meses.forEach(function(x){
    minVal = Math.min(minVal, x.real, x.orc);
    maxVal = Math.max(maxVal, x.real, x.orc);
  });
  // Padding visual
  var span = Math.max(Math.abs(maxVal), Math.abs(minVal)) * 1.08;
  if(span === 0) span = 1;
  var yMin = minVal < 0 ? -span : 0;
  var yMax = maxVal > 0 ? span : 0;
  if(yMin === yMax){ yMax = yMin + 1; }
  var range = yMax - yMin;

  function yPos(v){ return padT + plotH * (1 - (v - yMin) / range); }
  var y0 = yPos(0);

  // Largura por mês — 2 barras por mês com pequeno gap
  var slotW = plotW / 12;
  var barW = slotW * 0.35;
  var gap  = slotW * 0.05;

  // Grid lines (zero e ~4 linhas)
  var gridVals = [];
  for(var i=0; i<=4; i++){
    gridVals.push(yMin + (range * i/4));
  }

  var svg = '';
  // Grid horizontal + ticks Y
  gridVals.forEach(function(gv){
    var yp = yPos(gv);
    svg += '<line class="grid-line" x1="' + padL + '" y1="' + yp + '" x2="' + (W-padR) + '" y2="' + yp + '"/>';
    svg += '<text class="axis-text" x="' + (padL-6) + '" y="' + (yp+3) + '" text-anchor="end">' + _fmtChartLabel(gv) + '</text>';
  });
  // Linha de zero mais marcada
  svg += '<line x1="' + padL + '" y1="' + y0 + '" x2="' + (W-padR) + '" y2="' + y0 + '" stroke="var(--c-text-4b,#2A4560)" stroke-width="1"/>';

  // Barras + labels do eixo X
  meses.forEach(function(x, idx){
    var cx = padL + slotW * idx + slotW/2;
    var xReal = cx - barW - gap/2;
    var xOrc  = cx + gap/2;

    // Barra Real
    var yR = yPos(x.real);
    var hR = Math.abs(yR - y0);
    var topR = Math.min(yR, y0);
    svg += '<rect class="bar-real" x="' + xReal + '" y="' + topR + '" width="' + barW + '" height="' + hR + '" rx="2">';
    svg += '<title>' + MESES_CURTO_JS[x.m] + ' • Realizado: ' + _fmtChartFull(x.real) + '</title></rect>';

    // Barra Orçado
    var yO = yPos(x.orc);
    var hO = Math.abs(yO - y0);
    var topO = Math.min(yO, y0);
    svg += '<rect class="bar-orc" x="' + xOrc + '" y="' + topO + '" width="' + barW + '" height="' + hO + '" rx="2">';
    svg += '<title>' + MESES_CURTO_JS[x.m] + ' • Orçado: ' + _fmtChartFull(x.orc) + '</title></rect>';

    // Label do mês
    svg += '<text class="axis-text" x="' + cx + '" y="' + (H - padB + 16) + '" text-anchor="middle">' + MESES_CURTO_JS[x.m] + '</text>';

    // Valor (label discreto) acima da barra mais alta — só se houver espaço
    var topY = Math.min(topR, topO);
    if(topY > padT + 14){
      var val = Math.abs(x.real) >= Math.abs(x.orc) ? x.real : x.orc;
      svg += '<text class="bar-label" x="' + cx + '" y="' + (topY - 4) + '" text-anchor="middle">' + _fmtChartLabel(val) + '</text>';
    }
  });

  document.getElementById('chart-svg').innerHTML = svg;

  // Título + subtítulo
  document.getElementById('chart-modal-title').textContent = 'Evolução Mensal — ' + (d.label || 'Linha');
  var totalReal = 0, totalOrc = 0;
  meses.forEach(function(x){ totalReal += x.real; totalOrc += x.orc; });
  var sub = 'Realizado acumulado: ' + _fmtChartFull(totalReal);
  if(totalOrc !== 0){
    var diff = totalReal - totalOrc;
    var pct  = (diff/Math.abs(totalOrc))*100;
    var sinal = diff >= 0 ? '▲' : '▼';
    sub += '  •  Orçado: ' + _fmtChartFull(totalOrc) + '  •  Var: ' + sinal + ' ' + Math.abs(pct).toFixed(1) + '%';
  }
  document.getElementById('chart-modal-sub').textContent = sub;

  // Abre overlay e posiciona
  var overlay = document.getElementById('chart-modal-overlay');
  overlay.style.height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) + 'px';
  var box = document.getElementById('chart-modal-box');
  // Posiciona próximo ao scroll atual da janela do iframe
  var scrollY = window.scrollY || window.pageYOffset || 0;
  box.style.top = (scrollY + 60) + 'px';
  overlay.classList.add('open');
}

function mesesAbertos(){
  return !document.getElementById('dre-table').classList.contains('meses-off');
}
function toggleMeses(){
  var tbl = document.getElementById('dre-table');
  var opening = !mesesAbertos();
  if(opening){ tbl.classList.remove('meses-off'); } else { tbl.classList.add('meses-off'); }
  var btn = document.getElementById('btn-meses');
  btn.setAttribute('data-open', opening ? '1' : '0');
  btn.textContent = opening ? '▼ MESES' : '▶ MESES';
  btn.style.background = opening ? 'var(--c-bg-4,#0A2040)' : 'var(--c-bg-2,#0C1A2C)';
  btn.style.borderColor = opening ? 'var(--c-text-4,#2A5080)' : 'var(--c-border-2,#1A3050)';
}

function toggle(gid){
  var rows=document.querySelectorAll('.sub-'+gid); if(!rows.length) return;
  var opening=rows[0].style.display==='none'||rows[0].style.display==='';
  rows.forEach(function(r){
    r.style.display=opening?'table-row':'none';
  });
  var arrow=document.getElementById('arrow-'+gid);
  if(arrow) arrow.style.transform=opening?'rotate(0deg)':'rotate(-90deg)';
  if(!opening){ rows.forEach(function(r){ r.className.split(' ').forEach(function(cls){
    if(cls.startsWith('owner-')){ var cid=cls.replace('owner-','');
      document.querySelectorAll('.sub-'+cid).forEach(function(rr){ rr.style.display='none'; });
      var a2=document.getElementById('arrow-'+cid); if(a2) a2.style.transform='rotate(-90deg)';
    }
  }); }); }
}
</script>

<!-- MODAL -->
<div id="modal-overlay" onclick="if(event.target===this)closeModal()">
  <div id="modal-box">
    <div id="modal-header">
      <div><div id="modal-title"></div><div id="modal-total"></div></div>
      <button id="modal-close" onclick="closeModal()">&#x2715;</button>
    </div>
    <div id="modal-body">
      <table id="modal-table"><thead id="modal-thead"></thead><tbody id="modal-tbody"></tbody></table>
    </div>
    <div id="modal-footer">
      <span id="modal-count"></span>
      <span>Pressione <kbd style="background:var(--c-bg-5,#0C1828);border:1px solid var(--c-border-2,#1A3050);border-radius:3px;padding:1px 6px;font-size:10px;color:var(--c-text-3c,#4A7090);">Esc</kbd> para fechar</span>
    </div>
  </div>
</div>

<!-- MODAL DE GRÁFICO (evolução mensal Real vs Orçado) -->
<div id="chart-modal-overlay" onclick="if(event.target===this)closeChartModal()">
  <div id="chart-modal-box">
    <div id="chart-modal-header">
      <div>
        <div id="chart-modal-title"></div>
        <div id="chart-modal-sub"></div>
      </div>
      <button id="chart-modal-close" onclick="closeChartModal()">&#x2715;</button>
    </div>
    <div id="chart-modal-body">
      <svg id="chart-svg" class="chart-svg" viewBox="0 0 800 280" preserveAspectRatio="xMidYMid meet"></svg>
    </div>
    <div id="chart-modal-legend">
      <span class="lg-it"><span class="lg-sw" style="background:var(--c-accent,#3B82F6);"></span> Realizado</span>
      <span class="lg-it"><span class="lg-sw" style="background:var(--c-text-3e,#475569);"></span> Orçado</span>
    </div>
    <div id="chart-modal-footer">
      <span>Valores acumulados por mês (R$). Passe o mouse sobre as barras para ver o valor exato.</span>
    </div>
  </div>
</div>

<!-- COMMAND CENTER -->
<div class="cc-shell">

  <!-- COLUNA ESQUERDA: DRE -->
  <div class="cc-dre">
    <table id="dre-table" class="meses-off">
      <thead>
        <tr style="background:var(--c-bg-3,#060D1A);border-bottom:1px solid var(--c-border-1,#1A2E4A);">
          <th class="td-label" style="padding:10px 14px;text-align:left;font-size:10px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;"><button id="btn-meses" onclick="toggleMeses()" style="background:var(--c-bg-2,#0C1A2C);border:1px solid var(--c-border-2,#1A3050);border-radius:5px;color:var(--c-text-3b,#3D6080);font-size:9px;font-weight:700;letter-spacing:.05em;cursor:pointer;padding:3px 7px;margin-right:8px;vertical-align:middle;transition:all .15s;">▶ MESES</button>Descrição</th>
          <th class="td-pct"  style="padding:10px 8px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;">% MC</th>
""" + 
    "".join(
        f'          <th class="td-mes" data-mes="{m}" style="padding:10px 8px;text-align:right;font-size:9px;font-weight:700;'
        f'color:var(--c-border-2,#1E3A58);letter-spacing:.08em;text-transform:uppercase;border:none;white-space:nowrap;">{MESES_CURTO[m]}</th>'
        for m in meses_ativos
    ) + """
          <th class="td-val"  style="padding:10px 14px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;">Total (R$)</th>
          <th class="td-orc"  style="padding:10px 10px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;">Orçado (R$)</th>
          <th class="td-var"  style="padding:10px 10px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;">Var%</th>
          <th class="td-exe"  style="padding:10px 8px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;">Real/Orc Ano</th>
          <th class="td-prov" style="padding:10px 10px;text-align:right;font-size:9.5px;font-weight:700;color:var(--c-text-4,#2A5080);letter-spacing:.12em;text-transform:uppercase;border:none;white-space:nowrap;border-left:1px solid var(--c-border-1,#1E293B);">Prov.</th>
        </tr>
      </thead>
      <tbody>
""" + tbody + """
      </tbody>
    </table>
  </div>

  <!-- COLUNA DIREITA: PAINEL -->
  <div class="cc-panel" id="side-panel">

    <div style="background:var(--c-bg-3,#060D1A);padding:10px 12px;border-bottom:1px solid var(--c-border-1,#1A2E4A);border-radius:0 10px 0 0;">
      <div style="font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.18em;color:var(--c-text-4,#2A5080);">Command Center</div>
      <div style="font-size:10px;color:var(--c-text-4d,#3D5A78);margin-top:2px;font-weight:500;">Resumo Executivo</div>
    </div>

    <div class="cc-kpi-list" id="kpi-list">
      <!-- preenchido pelo JS abaixo -->
    </div>

    <div class="cc-panel-title">Composição das Despesas / MC</div>
    <div class="cc-bar-list" id="bar-list"></div>

    <div class="cc-panel-title">Cascata de Resultado</div>
    <div class="cc-waterfall">
      <div class="cc-wf-grid" id="wf-grid"></div>
    </div>

  </div>
</div>

<script>
/* ── Dados do painel ── */
var PANEL = """ + __import__('json').dumps(panel_data, ensure_ascii=False, default=str) + """;

function fmtK(v){
  var a=Math.abs(v);
  var s = a>=1000000 ? (a/1000000).toFixed(1)+'M' : a>=1000 ? (a/1000).toFixed(0)+'K' : a.toFixed(0);
  s=s.replace('.',',');
  return v<0?'('+s+')':s;
}
function fmtFull(v){
  var s=Math.abs(v).toLocaleString('pt-BR',{minimumFractionDigits:0,maximumFractionDigits:0});
  return v<0?'('+s+')':s;
}
function pct(v,base){ return base?((v/base)*100).toFixed(1)+'%':'—'; }

var R = PANEL.resumo;
var MC = PANEL.margem_contribuicao;
var VB = PANEL.venda_bruta;

/* ── KPI Cards ── */
var kpis = [
  { label:'Venda Bruta',      val:VB,                            sub: '100% da receita', pos: VB>=0 },
  { label:'Margem de Contribuição', val:MC,                      sub: pct(MC,VB)+' da venda bruta', pos: MC>=0 },
  { label:'EBITDA',           val:R['Resultado Operacional (EBITDA)']||0,
    sub: pct(R['Resultado Operacional (EBITDA)']||0, MC)+' da MC', pos:(R['Resultado Operacional (EBITDA)']||0)>=0 },
  { label:'Resultado Líquido',val:R['Resultado Líquido do Exercício']||0,
    sub: pct(R['Resultado Líquido do Exercício']||0, MC)+' da MC', pos:(R['Resultado Líquido do Exercício']||0)>=0 },
];
var kpiHTML='';
kpis.forEach(function(k){
  kpiHTML+='<div class="cc-kpi">'
    +'<div class="cc-kpi-label">'+k.label+'</div>'
    +'<div class="cc-kpi-val '+(k.pos?'pos':'neg')+'">'+fmtFull(k.val)+'</div>'
    +'<div class="cc-kpi-sub">'+k.sub+'</div>'
    +'</div>';
});
document.getElementById('kpi-list').innerHTML=kpiHTML;

/* ── Barras de composição ── */
var desp_keys = [
  { label:'Impostos',      key:'Receita Líquida',                  cor:'#D85A30' },
  { label:'Desp. Operac.', key:'Resultado Operacional (EBITDA)',    cor:'var(--c-text-4,#185FA5)' },
  { label:'Financeiro',    key:'Resultado Líquido do Exercício',    cor:'var(--c-text-4b,#0F6E56)' },
];
/* Calcula cada parcela como diferença entre subtotais consecutivos */
var rl   = R['Receita Líquida']||0;
var ebit = R['Resultado Operacional (EBITDA)']||0;
var liq  = R['Resultado Líquido do Exercício']||0;
var parcelas = [
  { label:'Impostos',      val: Math.abs(MC - rl),   cor:'var(--c-danger,#D84B20)' },
  { label:'Desp. Operac.', val: Math.abs(rl - ebit), cor:'var(--c-text-4,#1E5FA8)' },
  { label:'Financeiro',    val: Math.abs(ebit - liq), cor:'var(--c-text-4b,#0E6E56)' },
];
var barHTML='';
parcelas.forEach(function(b){
  var p=MC?Math.min(100,(b.val/Math.abs(MC))*100):0;
  barHTML+='<div class="cc-bar-item">'
    +'<div class="cc-bar-header"><span>'+b.label+'</span>'
    +'<span style="color:'+b.cor+'">'+p.toFixed(1)+'%</span></div>'
    +'<div class="cc-bar-track"><div class="cc-bar-fill" style="width:'+p+'%;background:'+b.cor+'"></div></div>'
    +'</div>';
});
document.getElementById('bar-list').innerHTML=barHTML;

/* ── Cascata ── */
var mc_abs  = Math.abs(MC);
var rl_abs  = Math.abs(rl);
var eb_abs  = Math.abs(ebit);
var liq_abs = Math.abs(liq);
var maxV    = Math.max(Math.abs(VB), mc_abs, rl_abs, eb_abs, liq_abs) || 1;
var H=110;
function barH(v){ return Math.max(6, Math.round((Math.abs(v)/maxV)*H)); }

var wfItems = [
  { lbl:'Venda', val:VB,   cor:'#1D9E75' },
  { lbl:'MC',    val:MC,   cor:'var(--c-text-2b,#5DCAA5)' },
  { lbl:'Rec.L.',val:rl,   cor:'#378ADD' },
  { lbl:'EBITDA',val:ebit, cor: ebit>=0?'var(--c-text-2b,#7FADD4)':'var(--c-danger,#F0997B)' },
  { lbl:'Líq.',  val:liq,  cor: liq>=0?'#1D9E75':'#D85A30' },
];
var wfHTML='';
wfItems.forEach(function(w){
  wfHTML+='<div class="cc-wf-col">'
    +'<div class="cc-wf-bar" style="height:'+barH(w.val)+'px;background:'+w.cor+'"></div>'
    +'<div class="cc-wf-lbl">'+w.lbl+'</div>'
    +'<div class="cc-wf-val">'+fmtK(w.val)+'</div>'
    +'</div>';
});
document.getElementById('wf-grid').innerHTML=wfHTML;
</script>

<!-- ── LEGENDA DE DESVIOS ── -->
<div style="display:flex;align-items:center;gap:16px;padding:6px 4px 10px;font-family:'Inter',sans-serif;font-size:10px;color:var(--c-text-4c,#2A4060);">
  <span style="font-weight:700;color:var(--c-text-4,#2A5080);text-transform:uppercase;letter-spacing:.08em;font-size:9px;">Desvios no mês atual:</span>
  <span style="display:inline-flex;align-items:center;gap:5px;">
    <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--c-danger,#EF4444);"></span>
    Alerta — MoM &gt;40% ou desvio vs média &gt;50%
  </span>
  <span style="display:inline-flex;align-items:center;gap:5px;">
    <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--c-warning,#F59E0B);"></span>
    Atenção — MoM &gt;20% ou desvio vs média &gt;25%
  </span>
  <span style="color:var(--c-border-2,#1A3050);font-size:9.5px;">(passe o mouse sobre o ícone para detalhes)</span>
</div>

<!-- ── LEGENDA DE ALERTAS VS ORÇADO + AÇÕES POR LINHA ── -->
<div style="display:flex;align-items:center;gap:16px;padding:0 4px 12px;font-family:'Inter',sans-serif;font-size:10px;color:var(--c-text-4c,#2A4060);flex-wrap:wrap;">
  <span style="font-weight:700;color:var(--c-text-4,#2A5080);text-transform:uppercase;letter-spacing:.08em;font-size:9px;">Desempenho Real vs Orçado (banda ±""" + f"{int(var_threshold_safe)}" + """%):</span>
  <span style="display:inline-flex;align-items:center;gap:5px;">
    <span style="display:inline-block;width:3px;height:11px;background:var(--c-success,#22C55E);"></span>
    <span style="color:var(--c-success,#22C55E);font-size:11px;">&#9650;</span>
    Favorável: Real superou orçado em &ge; """ + f"{int(var_threshold_safe)}" + """%
  </span>
  <span style="display:inline-flex;align-items:center;gap:5px;">
    <span style="color:var(--c-warning,#F59E0B);font-size:11px;opacity:.7;">&#9679;</span>
    Dentro da tolerância: desvio &lt; """ + f"{int(var_threshold_safe)}" + """%
  </span>
  <span style="display:inline-flex;align-items:center;gap:5px;">
    <span style="display:inline-block;width:3px;height:11px;background:var(--c-danger,#EF4444);"></span>
    <span style="color:var(--c-danger,#EF4444);font-size:11px;">&#9888;</span>
    Desfavorável: Real ficou &ge; """ + f"{int(var_threshold_safe)}" + """% pior
  </span>
  <span style="display:inline-flex;align-items:center;gap:5px;color:var(--c-accent,#3B82F6);">
    <span style="font-size:11px;">&#128202;</span>
    <span style="color:var(--c-text-4c,#2A4060);">Clique no ícone azul para evolução mensal vs orçado</span>
  </span>
</div>

<!-- ── PAINEL DE KPIs FINANCEIROS (dentro do iframe, sem sobreposição) ── -->
<style>
.kpi-outer-wrap {
  display: flex; gap: 8px; padding: 12px 0 10px 0; width: 100%;
  font-family: 'Inter', sans-serif;
}
.kpi-wrap-inner {
  flex: 1; background: var(--c-bg-1,#080F1C); border: 1px solid var(--c-border-1,#111E30);
  border-radius: 9px; overflow: hidden; min-width: 0;
}
.kpi-head-inner {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 12px 8px; background: var(--c-bg-3,#060D1A); border-bottom: 2px solid;
}
.kpi-head-dot-inner { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.kpi-head-title-inner {
  font-size: 10.5px; font-weight: 700; color: var(--c-text-2,#A0B8CC);
  line-height: 1.3; white-space: nowrap;
}
.kpi-body-inner { display: flex; flex-direction: column; gap: 5px; padding: 7px; }
.kpi-c-inner {
  border-radius: 6px; padding: 8px 10px 7px;
  border: 1px solid rgba(255,255,255,.04); position: relative;
  transition: border-color .12s;
}
.kpi-c-inner:hover { border-color: rgba(255,255,255,.09); }
.kpi-c-stripe-inner {
  position: absolute; top: 0; left: 0; right: 0;
  height: 2px; border-radius: 6px 6px 0 0;
}
.kpi-c-lbl-inner {
  font-size: 9px; font-weight: 700; color: var(--c-text-4b,#2A4560);
  text-transform: uppercase; letter-spacing: .07em;
  margin-bottom: 3px; line-height: 1.3;
}
.kpi-c-val-inner {
  font-size: 14px; font-weight: 500; line-height: 1.15;
  font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; letter-spacing: -0.01em;
}
</style>
<div class="kpi-outer-wrap" id="kpi-bottom-panel"></div>
<script>
(function(){
  var R = """ + _json.dumps(_sanitize(resumo), ensure_ascii=True) + """;
  var VB = """ + str(venda_bruta) + """;
  var MC = R['Margem de Contribui\u00e7\u00e3o / Lucro Bruto']||0;
  var VL = R['Venda L\u00edquida']||0;
  var RL = R['Receita L\u00edquida']||0;
  var EB = R['Resultado Operacional (EBITDA)']||0;
  var LQ = R['Resultado L\u00edquido do Exerc\u00edcio']||0;
  var IMP = MC - RL;
  var DOPER = RL - EB;
  var RFIN = EB - LQ;

  function pct(num,den){
    if(!den) return '\u2014';
    var v=(num/den)*100;
    return (v>=0?'\u25b2 ':'\u25bc ')+Math.abs(v).toFixed(1)+'%';
  }
  function fmtVal(v){
    var s=Math.abs(v).toLocaleString('pt-BR',{minimumFractionDigits:0,maximumFractionDigits:0});
    return v<0?'(R$ '+s+')':'R$ '+s;
  }
  function corV(v){ return v>=0?'var(--c-success,#22C55E)':'var(--c-danger,#EF4444)'; }
  function bgV(v){ return v>=0?'rgba(34,197,94,.07)':'rgba(239,68,68,.07)'; }
  function rawPct(num,den){ return den?(num/den)*100:0; }

  var grupos = [
    { titulo:'&#128202; Rentabilidade', cor:'var(--c-text-4,#1560A0)', kpis:[
      { lbl:'Margem Bruta',     val:pct(MC,VB),  raw:rawPct(MC,VB)  },
      { lbl:'Margem EBITDA',    val:pct(EB,VB),  raw:rawPct(EB,VB)  },
      { lbl:'Margem L\u00edquida',   val:pct(LQ,VB),  raw:rawPct(LQ,VB)  },
      { lbl:'Margem Rec. L\u00edq.', val:pct(RL,VB),  raw:rawPct(RL,VB)  },
    ]},
    { titulo:'&#128184; Estrutura de Custos', cor:'var(--c-danger,#A0440A)', kpis:[
      { lbl:'Impostos / VB',     val:pct(IMP,VB),   raw:rawPct(IMP,VB)   },
      { lbl:'Desp. Oper. / VB',  val:pct(DOPER,VB), raw:rawPct(DOPER,VB) },
      { lbl:'Result. Fin. / VB', val:pct(RFIN,VB),  raw:rawPct(RFIN,VB)  },
      { lbl:'Efici\u00eancia Oper.',  val:pct(DOPER,MC), raw:rawPct(DOPER,MC) },
    ]},
    { titulo:'&#128200; Convers\u00e3o de Resultado', cor:'var(--c-text-4b,#0E6040)', kpis:[
      { lbl:'Reten\u00e7\u00e3o de MC',   val:pct(MC,VL),  raw:rawPct(MC,VL)  },
      { lbl:'EBITDA / MC',      val:pct(EB,MC),  raw:rawPct(EB,MC)  },
      { lbl:'L\u00edq. / EBITDA',    val:pct(LQ,EB),  raw:rawPct(LQ,EB)  },
      { lbl:'Aproveit. Global', val:pct(LQ,MC),  raw:rawPct(LQ,MC)  },
    ]},
    { titulo:'&#127974; Valores do Per\u00edodo', cor:'var(--c-text-4c,#1E2E7C)', kpis:[
      { lbl:'Venda Bruta',         val:fmtVal(VB), raw:VB },
      { lbl:'Margem Contribui\u00e7\u00e3o', val:fmtVal(MC), raw:MC },
      { lbl:'EBITDA',              val:fmtVal(EB), raw:EB },
      { lbl:'Resultado L\u00edquido',   val:fmtVal(LQ), raw:LQ },
    ]},
  ];

  var html='';
  grupos.forEach(function(g){
    var cards='';
    g.kpis.forEach(function(k){
      var cv=corV(k.raw), bg=bgV(k.raw);
      cards+='<div class="kpi-c-inner" style="background:'+bg+';">'
            +'<div class="kpi-c-stripe-inner" style="background:'+g.cor+';"></div>'
            +'<div class="kpi-c-lbl-inner">'+k.lbl+'</div>'
            +'<div class="kpi-c-val-inner" style="color:'+cv+';">'+k.val+'</div>'
            +'</div>';
    });
    html+='<div class="kpi-wrap-inner">'
         +'<div class="kpi-head-inner" style="border-color:'+g.cor+';">'
         +'<span class="kpi-head-dot-inner" style="background:'+g.cor+';"></span>'
         +'<span class="kpi-head-title-inner">'+g.titulo+'</span></div>'
         +'<div class="kpi-body-inner">'+cards+'</div></div>';
  });
  document.getElementById('kpi-bottom-panel').innerHTML=html;
})();
</script>

<!-- ══════════════════════════════════════════════════════════════
     ANÁLISE VERTICAL (AV) + ANÁLISE HORIZONTAL (AH)
     ══════════════════════════════════════════════════════════════ -->
<style>
.analise-wrap {
  margin-top: 20px; border: 1px solid var(--c-border-1,#1A2E4A);
  border-radius: 10px; overflow: hidden; background: var(--c-bg-1,#080F1C);
}
.analise-header {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 16px; background: var(--c-bg-3,#060D1A);
  border-bottom: 1px solid var(--c-border-1,#1A2E4A);
  cursor: pointer; user-select: none;
}
.analise-header-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.analise-header-title {
  font-size: 11px; font-weight: 700; color: var(--c-text-1,#C8D9EC);
  text-transform: uppercase; letter-spacing: .14em;
}
.analise-header-sub { font-size: 10px; color: var(--c-text-4d,#3D5A78); margin-left: auto; font-weight: 500; }
.analise-toggle { color: var(--c-text-4,#2A5080); font-size: 11px; transition: transform .2s; margin-left: 10px; }
.analise-body { display: none; overflow-x: auto; }
.analise-body.open { display: block; }
.at { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.at thead th {
  position: sticky; top: 0; padding: 8px 14px;
  background: var(--c-bg-1,#06111E); border-bottom: 1px solid var(--c-border-1,#1A2E4A);
  font-size: 9px; font-weight: 700; color: var(--c-text-4,#2A5080);
  text-transform: uppercase; letter-spacing: .12em;
  white-space: nowrap; text-align: right;
}
.at thead th:first-child { text-align: left; min-width: 200px; }
.at tbody tr { border-bottom: 1px solid var(--c-bg-5,#0C1828); transition: background .1s; }
.at tbody tr:hover { background: var(--c-bg-5,#0A1525); }
.at tbody tr.at-ref { background: var(--c-bg-3,#07101C); }
.at tbody tr.at-sub { background: var(--c-bg-2,#0D1E32); border-top: 1px solid var(--c-border-2,#1A3050); }
.at tbody tr.at-sub td { font-weight: 700; }
.at tbody td {
  padding: 8px 14px; color: var(--c-text-3,#607A90); text-align: right;
  white-space: nowrap; font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;
}
.at tbody td:first-child { text-align: left; color: var(--c-text-2b,#8FAEC8); font-weight: 500; }
.at tbody tr.at-ref td:first-child { color: var(--c-text-1,#E2E8F0); font-weight: 700; }
.at tbody tr.at-sub td:first-child { color: var(--c-text-1,#C8D9EC); }
.at-pos { color: var(--c-success,#22C55E) !important; }
.at-neg { color: var(--c-danger,#EF4444) !important; }
.at-neu { color: var(--c-text-4b,#2A4560) !important; }
.at-bar { display:inline-block;vertical-align:middle;width:40px;height:5px;
          background:var(--c-bg-4,var(--c-bg-4,#0F1E30));border-radius:3px;margin-left:6px;overflow:hidden; }
.at-bar span { display:block;height:100%;border-radius:3px; }
.ah-up   { color: var(--c-success,#22C55E) !important; font-weight: 600; }
.ah-dn   { color: var(--c-danger,#EF4444) !important; font-weight: 600; }
.ah-zero { color: var(--c-text-4b,#2A4560) !important; }
</style>

<div class="analise-wrap">
  <div class="analise-header" onclick="toggleAna('av-body','av-arr')">
    <span class="analise-header-dot" style="background:#378ADD;"></span>
    <span class="analise-header-title">Análise Vertical (AV)</span>
    <span class="analise-header-sub">Participação % de cada linha sobre Venda Bruta — por mês e total</span>
    <span class="analise-toggle" id="av-arr">▼</span>
  </div>
  <div class="analise-body open" id="av-body">
    <table class="at" id="av-table"></table>
  </div>
</div>

<div class="analise-wrap" style="margin-top:14px;margin-bottom:4px;">
  <div class="analise-header" onclick="toggleAna('ah-body','ah-arr')">
    <span class="analise-header-dot" style="background:#1D9E75;"></span>
    <span class="analise-header-title">Análise Horizontal (AH)</span>
    <span class="analise-header-sub">Variação % mês a mês (MoM) e acumulado do período</span>
    <span class="analise-toggle" id="ah-arr">▼</span>
  </div>
  <div class="analise-body open" id="ah-body">
    <table class="at" id="ah-table"></table>
  </div>
</div>

<script>
(function(){
  var P     = PANEL;
  var RM    = P.resumo_meses || {};
  var VBm   = P.vb_por_mes   || {};
  var MESES = P.meses_ativos  || [];
  var VB    = P.venda_bruta  || 0;
  var R     = P.resumo       || {};

  var MNM=['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
  function mnm(m){ return MNM[parseInt(m)]||('M'+m); }
  function fmtP(v){ return v.toFixed(1)+'%'; }
  function corCls(v){ return v>0.05?'at-pos':v<-0.05?'at-neg':'at-neu'; }
  function miniBar(v){
    var p=Math.min(100,Math.abs(v)); var c=v>=0?'var(--c-success,#22C55E)':'var(--c-danger,#EF4444)';
    return '<span class="at-bar"><span style="width:'+p+'%;background:'+c+';"></span></span>';
  }
  function fmtMoM(v){
    if(Math.abs(v)<0.05) return '<span class="ah-zero">—</span>';
    var cl=v>0?'ah-up':'ah-dn',ar=v>0?'▲':'▼';
    return '<span class="'+cl+'">'+ar+' '+Math.abs(v).toFixed(1)+'%</span>';
  }

  /* Sequência de linhas — subtotais intercalados com derivadas */
  var LABELS = {
    'Venda Líquida':                        'Venda Líquida',
    'Margem de Contribuição / Lucro Bruto': 'Margem de Contribuição',
    'Receita Líquida':                      'Receita Líquida',
    'Resultado Operacional (EBITDA)':       'EBITDA',
    'Resultado Líquido do Exercício':       'Resultado Líquido',
  };

  /* Pega valor mensal de um subtotal */
  function vMes(key,m){ return RM[key]?(RM[key][String(m)]||0):0; }
  function vTot(key){   return R[key]||0; }

  /* Derivada entre dois subtotais (ou VB) para um dado mês */
  function vDerivMes(keyDe, keyAte, m){
    var curr = RM[keyDe] ? (RM[keyDe][String(m)]||0) : 0;
    var prev = keyAte===null ? (VBm[String(m)]||0) : (RM[keyAte]?(RM[keyAte][String(m)]||0):0);
    return curr - prev;
  }
  function vDerivTot(keyDe, keyAte){
    return (R[keyDe]||0) - (keyAte===null ? VB : (R[keyAte]||0));
  }

  /* Linhas em ordem DRE */
  var SEQ = [
    { tipo:'deriv', lbl:'(-) Deduções s/ Venda',    de:'Venda Líquida',                       ate:null },
    { tipo:'sub',   lbl:'Venda Líquida',             key:'Venda Líquida' },
    { tipo:'deriv', lbl:'(-) Custo das Vendas',      de:'Margem de Contribuição / Lucro Bruto',ate:'Venda Líquida' },
    { tipo:'sub',   lbl:'Margem de Contribuição',    key:'Margem de Contribuição / Lucro Bruto' },
    { tipo:'deriv', lbl:'(-) Impostos s/ Receita',   de:'Receita Líquida',                     ate:'Margem de Contribuição / Lucro Bruto' },
    { tipo:'sub',   lbl:'Receita Líquida',           key:'Receita Líquida' },
    { tipo:'deriv', lbl:'(-) Despesas Operacionais', de:'Resultado Operacional (EBITDA)',       ate:'Receita Líquida' },
    { tipo:'sub',   lbl:'EBITDA',                    key:'Resultado Operacional (EBITDA)' },
    { tipo:'deriv', lbl:'(-) Result. Financeiro',    de:'Resultado Líquido do Exercício',       ate:'Resultado Operacional (EBITDA)' },
    { tipo:'sub',   lbl:'Resultado Líquido',         key:'Resultado Líquido do Exercício' },
  ];

  function getValMes(s,m){
    return s.tipo==='sub' ? vMes(s.key,m) : vDerivMes(s.de,s.ate,m);
  }
  function getValTot(s){
    return s.tipo==='sub' ? vTot(s.key) : vDerivTot(s.de,s.ate);
  }

  /* ── ANÁLISE VERTICAL ──────────────────────────────────── */
  var avH='<thead><tr><th>Linha DRE</th>';
  MESES.forEach(function(m){ avH+='<th>'+mnm(m)+'</th>'; });
  avH+='<th style="border-left:1px solid var(--c-border-1,#1A2E4A);color:var(--c-text-3d,#4A6680);">Total</th></tr></thead><tbody>';

  /* VB = base 100% */
  avH+='<tr class="at-ref"><td>Venda Bruta <span style="color:var(--c-text-4b,#2A4560);font-size:9px;">(base = 100%)</span></td>';
  MESES.forEach(function(){ avH+='<td class="at-neu">100.0%'+miniBar(100)+'</td>'; });
  avH+='<td style="border-left:1px solid var(--c-border-1,#1A2E4A);color:var(--c-text-4b,#2A4560);">100.0%</td></tr>';

  SEQ.forEach(function(s){
    var cls=s.tipo==='sub'?'at-sub':'';
    avH+='<tr class="'+cls+'"><td>'+s.lbl+'</td>';
    MESES.forEach(function(m){
      var vbm=VBm[String(m)]||0;
      var val=getValMes(s,m);
      var p=vbm?(val/vbm)*100:0;
      avH+='<td class="'+corCls(p)+'">'+fmtP(p)+miniBar(p)+'</td>';
    });
    var tot=getValTot(s);
    var pTot=VB?(tot/VB)*100:0;
    avH+='<td class="'+corCls(pTot)+'" style="border-left:1px solid var(--c-border-1,#1A2E4A);">'+fmtP(pTot)+miniBar(pTot)+'</td>';
    avH+='</tr>';
  });
  avH+='</tbody>';
  document.getElementById('av-table').innerHTML=avH;

  /* ── ANÁLISE HORIZONTAL ────────────────────────────────── */
  var ahH='<thead><tr><th>Linha DRE</th>';
  for(var i=1;i<MESES.length;i++){
    ahH+='<th>'+mnm(MESES[i-1])+' → '+mnm(MESES[i])+'</th>';
  }
  if(MESES.length>=2){
    ahH+='<th style="border-left:1px solid var(--c-border-1,#1A2E4A);">'+mnm(MESES[0])+' → '+mnm(MESES[MESES.length-1])
        +'<br><span style="color:var(--c-text-4b,#2A4560);font-size:8px;font-weight:400;">Acumulado</span></th>';
  }
  ahH+='</tr></thead><tbody>';

  /* VB */
  ahH+='<tr class="at-ref"><td>Venda Bruta</td>';
  for(var i=1;i<MESES.length;i++){
    var v0=VBm[MESES[i-1]]||0,v1=VBm[MESES[i]]||0;
    ahH+='<td>'+fmtMoM(v0?(v1-v0)/Math.abs(v0)*100:0)+'</td>';
  }
  if(MESES.length>=2){
    var v0=VBm[MESES[0]]||0,vn=VBm[MESES[MESES.length-1]]||0;
    ahH+='<td style="border-left:1px solid var(--c-border-1,#1A2E4A);">'+fmtMoM(v0?(vn-v0)/Math.abs(v0)*100:0)+'</td>';
  }
  ahH+='</tr>';

  SEQ.forEach(function(s){
    var cls=s.tipo==='sub'?'at-sub':'';
    ahH+='<tr class="'+cls+'"><td>'+s.lbl+'</td>';
    for(var i=1;i<MESES.length;i++){
      var v0=getValMes(s,MESES[i-1]),v1=getValMes(s,MESES[i]);
      ahH+='<td>'+fmtMoM(v0?(v1-v0)/Math.abs(v0)*100:0)+'</td>';
    }
    if(MESES.length>=2){
      var v0=getValMes(s,MESES[0]),vn=getValMes(s,MESES[MESES.length-1]);
      ahH+='<td style="border-left:1px solid var(--c-border-1,#1A2E4A);">'+fmtMoM(v0?(vn-v0)/Math.abs(v0)*100:0)+'</td>';
    }
    ahH+='</tr>';
  });
  ahH+='</tbody>';
  document.getElementById('ah-table').innerHTML=ahH;

  window.toggleAna=function(bodyId,arrId){
    var b=document.getElementById(bodyId);
    var open=b.classList.toggle('open');
    document.getElementById(arrId).style.transform=open?'':'rotate(-90deg)';
  };
})();
</script>

</body>
</html>""")
    # ─────────────────────────────────────────────────────────────────────────
    # EXECUTIVE BRIEF — bloco narrativo no topo, antes da DRE
    # Calculado a partir de df_f, df_orc, df_yoy e demais dados
    # ─────────────────────────────────────────────────────────────────────────
    brief_html = _build_executive_brief(
        df_f=df_f, df_orc=df_orc, df_orc_ano=df_orc_ano, df_yoy=df_yoy,
        estrutura=estrutura, subtotais=subtotais,
        empresas_sel=empresas_sel or [], meses_ativos=meses_ativos or [],
        ano_sel=ano_sel, var_threshold=var_threshold
    )
    # Injeta o brief antes do '<!-- COMMAND CENTER -->'
    html = html.replace("<!-- COMMAND CENTER -->", brief_html + "\n<!-- COMMAND CENTER -->", 1)
    # Aumenta a altura para acomodar o brief (~230px)
    altura_dre += 230

    return html, resumo, altura_dre
    
    
    
    
import base64

# ─────────────────────────────────────────────────────────────────────────────
# GESTÃO DE LOGOTIPOS LOCAIS
# ─────────────────────────────────────────────────────────────────────────────
# Mapeie partes do nome da empresa para os ficheiros correspondentes na sua pasta
ARQUIVOS_LOGOS = {
    "ASSETUR": "stella.png",
    "PRESC": "4bts.png",
    "LYNX": "lynx.png",
    "NEST": "nest.png"   
    
}

LOGO_GENERICA = "aguia.jpg" # Ficheiro que servirá de fallback

def get_image_base64(filepath: str) -> str:
    """Lê um ficheiro de imagem local e converte para string Base64."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
            ext = filepath.split('.')[-1].lower()
            mime_type = f"image/{ext}" if ext in ['png', 'jpg', 'jpeg', 'svg'] else "image/png"
            return f"data:{mime_type};base64,{encoded}"
    return None

def obter_logo_html(nome_limpo: str) -> str:
    """Busca o ficheiro local, converte para Base64 e devolve a tag HTML."""
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo = LOGO_GENERICA 
    
    for chave, arquivo in ARQUIVOS_LOGOS.items():
        if chave.upper() in nome_limpo.upper():
            nome_arquivo = arquivo
            break
            
    caminho_logo = os.path.join(diretorio_atual, nome_arquivo)
    b64_img = get_image_base64(caminho_logo)
    
    if not b64_img and nome_arquivo != LOGO_GENERICA:
        caminho_generica = os.path.join(diretorio_atual, LOGO_GENERICA)
        b64_img = get_image_base64(caminho_generica)
        
    if b64_img:
        # Ajustado para 85px de altura e largura
        return f"<img src='{b64_img}' style='height:85px; width:85px; object-fit:contain; vertical-align:middle; margin-right:15px; margin-bottom:5px;'>"
    
    return ""



# ─────────────────────────────────────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────────────────────────────────────
if df_f.empty:
    periodo_str = "—"
elif mes_de == mes_ate:
    periodo_str = f"{MESES_PT[mes_de]} / {ano_sel}"
else:
    periodo_str = f"{MESES_CURTO[mes_de]} a {MESES_CURTO[mes_ate]} / {ano_sel}"

# 1. Limpa o texto dos CRDs para a legenda
crd_limpos = [x.split(" - ", 1)[-1] if " - " in x else x for x in crd_sel]
crd_str = ', '.join(crd_limpos) if len(crd_limpos) <= 3 else f"{len(crd_limpos)} selecionados"

# 2. Nomes limpos das empresas selecionadas
empresas_limpas = [x.split(" - ", 1)[-1] if " - " in x else x for x in empresas_sel]

# 3. Constrói o HTML dos logos e nomes
if len(empresas_limpas) == 1:
    empresa_html_display = (
        f"<span style='display:inline-flex; align-items:center; margin-left:20px;'>"
        f"{obter_logo_html(empresas_limpas[0])}{empresas_limpas[0]}</span>"
    )
elif len(empresas_limpas) <= 3:
    empresa_html_display = " ".join([
        f"<span style='display:inline-flex; align-items:center; margin-left:20px;'>"
        f"{obter_logo_html(e)}{e}</span>"
        for e in empresas_limpas
    ])
else:
    empresa_html_display = f"<span style='margin-left:20px;'>| {len(empresas_limpas)} empresas selecionadas</span>"

# 4. Renderiza o cabeçalho completo
st.markdown(
    f"<div style='padding-bottom: 15px;'>"
    f"<h2 style='margin:0 0 8px 0; font-family:system-ui, -apple-system, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif; font-size:1.75rem;"
    f"font-weight:700; color:var(--c-text-1,#E2E8F0); display:flex; align-items:center; letter-spacing:-0.01em;'>"
    f"DRE Gerencial Consolidado "
    f"<span style='font-size: 1.3rem; color: var(--c-accent,#4A7FA8); font-weight: 500;'>{empresa_html_display}</span></h2>"
    f"<p style='margin:0; font-size:0.82rem; color:var(--c-text-4d,#3D5A78); letter-spacing:0.01em; font-family:system-ui, -apple-system, sans-serif;'>"
    f"📅 <b style='color:var(--c-text-3c,#4A7090)'>{periodo_str}</b> &nbsp;|&nbsp; "
    f"📋 <b style='color:var(--c-text-3c,#4A7090)'>{', '.join(cenarios_sel)}</b> &nbsp;|&nbsp; "
    f"🎯 CRD: <b style='color:var(--c-text-3c,#4A7090)'>{crd_str}</b></p>"
    f"</div>",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RENDERIZAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
if df_f.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

html_dre, resumo_executivo, altura_dre = build_dre_html(
    df_f, df_orc, df_orc_ano, df_prov, df_ano, ESTRUTURA_DRE, SUBTOTAIS, SECOES,
    FORA_DRE, mostrar_orfaos, meses_ativos=meses_sel,
    var_threshold=float(var_threshold), tema=tema_escolhido,
    df_yoy=df_yoy, empresas_sel=empresas_sel, ano_sel=ano_sel
)

import streamlit.components.v1 as components
# Sanitiza surrogates inválidos que possam vir dos dados antes de passar ao Streamlit
html_dre_safe = html_dre.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
components.html(html_dre_safe, height=altura_dre, scrolling=True)

# ─────────────────────────────────────────────────────────────────────────────
# RESUMO EXECUTIVO — SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    st.subheader("📌 Resumo Executivo")
    for label, valor in resumo_executivo.items():
        st.metric(
            label=label,
            value=f"R$ {abs(valor):,.0f}",
            delta="▲ positivo" if valor >= 0 else "▼ negativo",
            delta_color="normal" if valor >= 0 else "inverse",
        )