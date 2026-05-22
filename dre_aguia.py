import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="DRE Gerencial", layout="wide", page_icon="📊")

st.markdown("""
<style>
.block-container { padding-top: 2.5rem !important; padding-bottom: 2rem !important; }

/* Força o iframe do components.html a ocupar toda a largura disponível */
iframe {
    width: 100% !important;
    min-width: 100% !important;
}
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
    ("INVESTIMENTOS",                              "(-) Investimentos",             -1),
]

SUBTOTAIS = {
    "(-) Comissão sobre Vendas":                 ("Venda Líquida",                      False),
    "(+) Reembolso de Custos":                   ("Margem de Contribuição / Lucro Bruto",False),
    "Impostos Incidentes s/ Receita Tributável": ("Receita Líquida",                    True),
    "Despesas Administrativa, Comercial e Mkt":  ("Resultado Operacional (EBITDA)",     False),
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
def load_mapping(path: str) -> dict:
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
    key_col   = df["Tipo_Documento"] + SEP + df["cp_ms"]
    new_dre   = key_col.map(map_dre_exact)
    new_sinal = key_col.map(map_sig_exact)
    no_match  = new_dre.isna()
    if no_match.any():
        new_dre[no_match]   = df.loc[no_match, "Tipo_Documento"].map(map_dre_star)
        new_sinal[no_match] = df.loc[no_match, "Tipo_Documento"].map(map_sig_star)
    null2 = new_dre.isna()
    if null2.any():
        new_dre[null2] = df.loc[null2, "dre"]; new_sinal[null2] = -1
    df = df.copy()
    df["dre"]   = new_dre.values
    df["sinal"] = new_sinal.fillna(-1).astype(int).values
    return df


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DADOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(xlsx_path: str, parquet_path: str) -> pd.DataFrame:
    if os.path.exists(parquet_path) and \
       os.path.getmtime(parquet_path) >= os.path.getmtime(xlsx_path):
        df = pd.read_parquet(parquet_path)
    else:
        df = pd.read_excel(xlsx_path, sheet_name="DRE")
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)
        df.to_parquet(parquet_path, index=False)
    for col in ["dre","Grupo","SubGrupo","Tipo_Documento","Empresa","cp_ms"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace("nan","Sem Classificação")
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

with st.sidebar:
    if st.button("🔄 Recarregar dados do Excel"):
        if os.path.exists(parquet_path): os.remove(parquet_path)
        st.cache_data.clear(); st.rerun()

with st.spinner("Carregando…"):
    try:
        mapping = load_mapping(mapping_path)
        if not mapping:
            st.warning("⚠️ mapeamento_td.xlsx não encontrado — usando classificação original.")
        df_raw = load_data(xlsx_path, parquet_path)
        df     = aplicar_mapping(df_raw, mapping)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xlsx_path}"); st.stop()
    except Exception as e:
        st.error(f"Erro: {e}"); st.stop()

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
    empresas_sel = st.multiselect("🏢 Empresa", empresas_all, default=empresas_all)
    
    cenarios_all = sorted(df["cp_ms"].unique())
    cenarios_sel = st.multiselect("📋 Cenário", cenarios_all, default=cenarios_all)
    
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
    # A mágica acontece aqui: divide no " - " e pega apenas a última parte
    format_func=lambda x: x.split(" - ", 1)[-1] if " - " in x else x
)

    st.divider()
    mostrar_orfaos = st.toggle("⚠️ Mostrar contas não mapeadas", value=True)

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
    return "#C0392B" if v < 0 else "#1A7A4A"

# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUÇÃO DA TABELA HTML
# A DRE inteira é uma única tabela HTML com linhas colapsáveis via JS puro.
# Hierarquia: Seção → Categoria → Grupo → SubGrupo → TD
# ─────────────────────────────────────────────────────────────────────────────
def build_dre_html(df_f: pd.DataFrame, df_orc: pd.DataFrame, estrutura, subtotais, secoes,
                   fora_dre: str, mostrar_orfaos: bool, meses_ativos: list = None) -> str:

    dres_no_arquivo = set(df_f["dre"].unique())
    dres_mapeadas   = set()
    acumulador      = 0.0
    resumo          = {}   # para a sidebar
    detalhe_data    = {}   # chave → lista de dicts de linhas para o modal

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

    def _td_orc(label: str, valor: float, orc: float) -> str:
        """Gera células HTML de Orçado e Variação% para uma linha da DRE.
        Cor da variação:
          • Receitas (sinal >0): realizado < orçado → vermelho (ficou abaixo)
          • Despesas (sinal <0): realizado > orçado (em absoluto) → vermelho (estourou)
        Usamos a convenção simples: variação = (real - orc) / |orc|
          positiva = realizado acima do orçado.
        Para despesas, acima do orçado é ruim → vermelho.
        Para receitas, abaixo do orçado é ruim → também vermelho quando negativa.
        Ou seja: vermelho quando (real - orc) > 0 e é despesa, OU quando (real - orc) < 0 e é receita.
        Simplificado: a cor segue o sinal de (real - orc) invertida para despesas.
        Na prática, usamos:
          var_pct positiva → bom se receita, ruim se despesa
          → pintamos vermelho quando: real > orc (despesa estourou OU receita não esperada mas ok)
        """
        if df_orc.empty:
            return "<td class='td-orc'></td><td class='td-var'></td>"
        orc_fmt = _fmt(orc) if orc != 0 else "—"
        if orc == 0:
            return (
                f"<td class='td-orc'>{orc_fmt}</td>"
                f"<td class='td-var' style='color:#94A3B8;'>—</td>"
            )

        # Variação percentual sempre sobre o valor absoluto do orçado
        var_pct = (valor - orc) / abs(orc) * 100

        # Regra econômica:
        #   • valor > orc no espaço contábil = MELHOR para o resultado
        #     (receita acima do orçado OU despesa menos negativa que o orçado)
        #   • valor < orc no espaço contábil = PIOR para o resultado → VERMELHO
        # Exemplos:
        #   Receita:  real=100, orc=80  → var=+25% → verde  (acima do orçado ✓)
        #   Receita:  real=60,  orc=80  → var=-25% → vermelho (abaixo do orçado ✗)
        #   Despesa:  real=-98, orc=-110 → var=-10.9% → verde (gastou menos ✓)
        #   Despesa:  real=-130,orc=-110 → var=+18.2% → vermelho (estourou ✗)
        ruim = valor < orc   # pior que o orçado no sentido contábil
        cor_var = "#C0392B" if ruim else "#1A7A4A"

        # Seta indica direção do desvio em valor absoluto (sempre mostra a magnitude)
        sinal_v = "▲" if var_pct > 0 else ("▼" if var_pct < 0 else "")
        var_str = f"{sinal_v} {abs(var_pct):.1f}%"
        return (
            f"<td class='td-orc'>{orc_fmt}</td>"
            f"<td class='td-var' style='color:{cor_var};font-weight:600;'>{var_str}</td>"
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
        cor = "#C0392B" if pct < 0 else "#1A7A4A"
        s = f"{abs(pct):.1f}%"
        s = f"({s})" if pct < 0 else s
        return f"<td class='td-pct {cls_extra}' style='color:{cor};'>{s}</td>"

    def _pct_vazio() -> str:
        return "<td class='td-pct'></td>"

    def tr_secao(titulo: str) -> str:
        return (
            f"<tr class='tr-sec'>"
            f"<td colspan='5' class='td-sec'>{titulo}</td></tr>"
        )

    def tr_categoria(label: str, valor: float, gid: str, mc: float = None,
                     orc: float = 0.0, td_meses: str = '') -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc) if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc)
        return (
            f"<tr class='tr-cat' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-cat-label'>"
            f"<span id='arrow-{gid}' class='arrow'>&#9658;</span>"
            f"&nbsp;{label}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val' style='color:{cor};font-weight:600;'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_grupo(label: str, valor: float, gid: str, pgid: str, mc: float = None,
                orc: float = 0.0, td_meses: str = '') -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc, "td-val-sm") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc)
        return (
            f"<tr class='sub-{pgid} owner-{gid} tr-grp' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-grp-label'>"
            f"<span id='arrow-{gid}' class='arrow'>&#9658;</span>"
            f"&nbsp;{label}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-val-sm' style='color:{cor};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_subgrupo(label: str, valor: float, gid: str, pgid: str, mc: float = None,
                   orc: float = 0.0, td_meses: str = '') -> str:
        cor = _cor(valor)
        pct = _pct_html(valor, mc, "td-val-sm") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc)
        return (
            f"<tr class='sub-{pgid} owner-{gid} tr-subg' onclick=\"toggle('{gid}\')\">"
            f"<td class='td-label td-subg-label'>"
            f"<span id='arrow-{gid}' class='arrow arrow-sm'>&#9658;</span>"
            f"&nbsp;{label}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-val-sm' style='color:{cor};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_td(label: str, valor: float, pgid: str, modal_key: str, mc: float = None,
             orc: float = 0.0, td_meses_arg: str = '') -> str:
        cor = _cor(valor)
        import html as _html_mod
        data_key = _html_mod.escape(modal_key, quote=True)
        pct = _pct_html(valor, mc, "td-val-xs") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc)
        return (
            f"<tr class='sub-{pgid} tr-leaf' data-key=\"{data_key}\"" 
            f" style='cursor:pointer;' title='Clique para ver detalhes'>"
            f"<td class='td-label td-leaf-label'>"
            f"<span style='color:#94A3B8;font-size:10px;margin-right:4px;'>&#128269;</span>"
            f"{label}</td>"
            f"{pct}"
            f"{td_meses_arg}"
            f"<td class='td-val td-val-xs' style='color:{cor};'>{_fmt(valor, 2)}</td>"
            f"{td_orc_html}</tr>"
        )

    def tr_subtotal(label: str, valor: float, is_final: bool = False, mc: float = None,
                   orc: float = 0.0, td_meses: str = '') -> str:
        pct = _pct_html(valor, mc, "td-subtotal-val") if mc is not None else _pct_vazio()
        td_orc_html = _td_orc(label, valor, orc)
        n_mes_cols = len(meses_ativos)
        total_cols = 5 + n_mes_cols
        if is_final:
            cor_v = "#86EFAC" if valor >= 0 else "#FCA5A5"
            pct_final = _pct_html(valor, mc, "td-total-val") if mc is not None else _pct_vazio()
            return (
                f"<tr class='tr-total-final'>"
                f"<td class='td-label td-total-label' style='color:#fff;'>(=) {label}</td>"
                f"{pct_final}"
                f"{td_meses}"
                f"<td class='td-val td-total-val' style='color:{cor_v};'>{_fmt(valor)}</td>"
                f"{td_orc_html}</tr>"
                f"<tr><td colspan='{total_cols}' style='height:5px;background:#E8EDF2;'></td></tr>"
            )
        cor_v = _cor(valor)
        return (
            f"<tr class='tr-subtotal'>"
            f"<td class='td-label td-subtotal-label'>(=) {label}</td>"
            f"{pct}"
            f"{td_meses}"
            f"<td class='td-val td-subtotal-val' style='color:{cor_v};'>{_fmt(valor)}</td>"
            f"{td_orc_html}</tr>"
            f"<tr><td colspan='{total_cols}' style='height:3px;background:#F1F5F9;'></td></tr>"
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

    # processar_categoria: acumula e gera todas as linhas de um bloco DRE
    def _build_td_meses(vals_por_mes, cls_size=""):
        cells = ""
        for m in meses_ativos:
            v = vals_por_mes.get(m, 0.0)
            cor = _cor(v)
            extra = (" " + cls_size) if cls_size else ""
            cells += f"<td class='td-mes{extra}' style='color:{cor};'>{_fmt(v)}</td>"
        return cells

    def processar_categoria(nome_dre, label_exib, sinal_pad):
        nonlocal acumulador
        df_cat = df_f[df_f["dre"] == nome_dre]
        valor  = _soma(df_cat, sinal_pad) if not df_cat.empty else 0.0
        acumulador += valor

        # Valores mensais da categoria
        vals_mes_cat = {m: _soma_mes(df_cat, sinal_pad, m) for m in meses_ativos}
        td_meses_cat = _build_td_meses(vals_mes_cat)

        # Orçado nível categoria
        orc_cat = _soma_orc(df_cat, sinal_pad, nivel="cat", nome_dre=nome_dre)

        # Determina se esta categoria exibe % sobre MC
        exibe_pct = nome_dre in NOMES_COM_PCT
        mc = margem_contribuicao if exibe_pct else None

        if nome_dre in secoes:
            linhas_html.append(tr_secao(secoes[nome_dre]))

        # Não renderiza categoria com valor 0
        if valor == 0.0:
            if nome_dre in subtotais:
                label_sub, _ = subtotais[nome_dre]
                resumo[label_sub] = acumulador
                is_final = label_sub == "Resultado Liquido do Exercicio"
                linhas_html.append(tr_subtotal(label_sub, acumulador, is_final,
                                               mc=mc if exibe_pct else None))
            return valor

        cat_id = next_id()
        linhas_html.append(tr_categoria(label_exib, valor, cat_id, mc=mc, orc=orc_cat,
                                        td_meses=td_meses_cat))

        if not df_cat.empty:
            grupos = sorted(df_cat["Grupo"].unique())
            for grupo in grupos:
                df_g  = df_cat[df_cat["Grupo"] == grupo]
                val_g = _soma(df_g, sinal_pad)

                if val_g == 0.0:
                    continue

                vals_mes_grp = {m: _soma_mes(df_g, sinal_pad, m) for m in meses_ativos}
                td_meses_grp = _build_td_meses(vals_mes_grp, "td-val-sm")

                orc_grp = _soma_orc(df_cat, sinal_pad, nivel="grp",
                                    nome_dre=nome_dre, grupo=grupo)

                subgrupos = sorted(df_g["SubGrupo"].unique())

                mostrar_grupo = not (
                    len(grupos) == 1 and
                    grupo.strip().upper() in (nome_dre.strip().upper(), label_exib.strip().upper())
                )

                if mostrar_grupo:
                    grp_id = next_id()
                    linhas_html.append(tr_grupo(grupo, val_g, grp_id, cat_id, mc=mc,
                                                orc=orc_grp, td_meses=td_meses_grp))
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
                    td_meses_sg = _build_td_meses(vals_mes_sg, "td-val-sm")

                    orc_sg = _soma_orc(df_cat, sinal_pad, nivel="subg",
                                       nome_dre=nome_dre, grupo=grupo, subg=subg)

                    ref_nome = grupo if mostrar_grupo else label_exib
                    mostrar_subg = not (
                        len(subgrupos) == 1 and
                        subg.strip().upper() in (ref_nome.strip().upper(), nome_dre.strip().upper(), label_exib.strip().upper())
                    )

                    if mostrar_subg:
                        sg_id = next_id()
                        linhas_html.append(tr_subgrupo(subg, val_sg, sg_id, pai_subg, mc=mc,
                                                       orc=orc_sg, td_meses=td_meses_sg))
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
                        orc_td = _soma_orc(df_cat, sinal_pad, nivel="td",
                                           nome_dre=nome_dre, grupo=grupo, subg=subg, td=td_nome)

                        df_td = df_sg[df_sg["Tipo_Documento"] == td_nome]
                        vals_mes_td = {m: _soma_mes(df_td, sinal_pad, m) for m in meses_ativos}
                        td_meses_td = _build_td_meses(vals_mes_td, "td-val-xs")

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
                                                 orc=orc_td, td_meses_arg=td_meses_td))

        if nome_dre in subtotais:
            label_sub, _ = subtotais[nome_dre]
            resumo[label_sub] = acumulador
            is_final = label_sub == "Resultado Liquido do Exercicio"
            orc_sub = sum(
                _soma_orc(df_f[df_f["dre"] == c], s, nivel="cat", nome_dre=c)
                for c, s in _mc_cats.items()
            ) if label_sub in ("Margem de Contribuicao / Lucro Bruto",) else 0.0
            # Valores mensais do subtotal (acumulado até agora, mês a mês)
            acc_by_mes = {}
            for nome2, _, sp2 in estrutura:
                for m in meses_ativos:
                    df2 = df_f[df_f["dre"] == nome2]
                    acc_by_mes[m] = acc_by_mes.get(m, 0.0) + _soma_mes(df2, sp2, m)
                if nome2 == nome_dre:
                    break
            td_meses_sub = _build_td_meses(acc_by_mes)
            mc_sub = mc if exibe_pct else None
            linhas_html.append(tr_subtotal(label_sub, acumulador, is_final, mc=mc_sub,
                                           orc=orc_sub, td_meses=td_meses_sub))

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
                linhas_html.append(tr_subtotal(label_sub, acumulador, is_final))

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

    # Serializa dados de detalhe — ensure_ascii=True evita problemas de encoding;
    # escapa </script> para nao fechar o bloco <script> prematuramente
    detalhe_json = _json.dumps(detalhe_data, ensure_ascii=True, default=str)
    detalhe_json_safe = detalhe_json.replace("</" , "<\\/")

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
    altura_dre = max(500, n_visiveis * 36 + 80)

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
    }

    html = ("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; background: transparent; font-family: 'Inter', sans-serif; font-size: 13px; color: #1E293B; }

/* ── LAYOUT COMMAND CENTER ───────────────────────────── */
.cc-shell {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 0;
  border: 1px solid #CBD5E1;
  border-radius: 10px;
  overflow: visible;
  box-shadow: 0 4px 20px rgba(15,45,82,.10);
  align-items: start;
}

/* ── COLUNA ESQUERDA — DRE ───────────────────────────── */
.cc-dre { overflow: hidden; border-right: 1px solid #CBD5E1; }

table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.td-label { width: 57%; padding: 0 14px; text-align: left; border: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-pct   { width: 12%; padding: 0 8px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 11px; font-style: italic; }
.td-val   { width: 22%; padding: 0 14px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums; }
.td-orc   { width: 18%; padding: 0 10px; text-align: right; border: none;
            white-space: nowrap; font-variant-numeric: tabular-nums;
            color: #64748B; font-size: 12px; }
.td-var   { width: 10%; padding: 0 10px; text-align: right; border: none;
            white-space: nowrap; font-size: 11.5px; font-style: italic; }
.td-label { width: 40%; }
.td-pct   { width: 10%; }

/* seções */
.tr-sec { background: #0A2342; }
.td-sec { padding: 6px 14px; color: #7FADD4; font-size: 9.5px; font-weight: 700;
          letter-spacing: 0.14em; text-transform: uppercase; border: none; }

/* categoria nível 1 */
.tr-cat { background: #F8FAFC; border-top: 1px solid #E2E8F0; cursor: pointer; transition: background .1s; }
.tr-cat:hover { background: #EDF4FB; }
.td-cat-label { padding-top: 9px; padding-bottom: 9px; font-weight: 600; color: #0F2D52; font-size: 13px; }

/* grupo nível 2 */
.tr-grp  { display: none; background: #fff; border-top: 1px solid #F1F5F9; cursor: pointer; }
.tr-grp:hover { background: #F7F9FC; }
.td-grp-label { padding: 7px 14px 7px 32px; color: #334155; font-weight: 600; font-size: 12.5px; }

/* subgrupo nível 3 */
.tr-subg { display: none; background: #FAFBFC; border-top: 1px solid #F1F5F9; cursor: pointer; }
.tr-subg:hover { background: #F0F4F8; }
.td-subg-label { padding: 6px 14px 6px 50px; color: #475569; font-size: 12px; }

/* folha nível 4 */
.tr-leaf { display: none; background: #EFF5FC; border-top: 1px solid #DDE8F4; cursor: pointer; transition: background .1s; }
.tr-leaf:hover { background: #E0EDF9; }
.td-leaf-label { padding: 5px 14px 5px 68px; color: #2D5FA8; font-size: 11.5px; }

/* valores */
.td-val     { padding-top: 9px; padding-bottom: 9px; font-weight: 600; font-size: 13px; }
.td-val-sm  { padding-top: 7px; padding-bottom: 7px; font-weight: 500; font-size: 12.5px; }
.td-val-xs  { padding-top: 5px; padding-bottom: 5px; font-weight: 500; font-size: 11.5px; }

/* subtotais */
.tr-subtotal { background: #EEF2F7; border-top: 1.5px solid #C8D6E8; border-bottom: 1.5px solid #C8D6E8; }
.td-subtotal-label { padding: 8px 14px; color: #1E3A5F; font-weight: 700; font-size: 12.5px; }
.td-subtotal-val   { padding: 8px 14px; font-weight: 700; font-size: 12.5px; }
.tr-total-final { background: #0F2D52; }
.td-total-label { padding: 12px 14px; color: #fff; font-weight: 700; font-size: 13px; }
.td-total-val   { padding: 12px 14px; font-weight: 700; font-size: 13px; }

.td-mes {
  width: 80px; min-width: 70px; padding: 0 8px; text-align: right; border: none;
  white-space: nowrap; font-variant-numeric: tabular-nums;
  color: #334155; font-size: 12px; background: rgba(29,69,128,.04);
  border-left: 1px solid #E8EDF4;
}
/* Meses escondidos — classe removida pelo toggleMeses() */
.meses-off .td-mes { display: none !important; }
.meses-off th.td-mes { display: none !important; }

/* seta */
.arrow    { display: inline-block; width: 14px; color: #94A3B8; font-size: 10px;
            transition: transform .15s; transform: rotate(-90deg); margin-right: 2px; }
.arrow-sm { width: 12px; font-size: 9px; }

/* ── COLUNA DIREITA — PAINEL ─────────────────────────── */
.cc-panel {
  background: #F0F4F9;
  display: flex; flex-direction: column;
  overflow-y: auto;
  position: sticky;
  top: 0;
  max-height: 100vh;
  border-radius: 0 10px 10px 0;
}

/* KPI cards */
.cc-kpi-list { padding: 12px 10px 6px; display: flex; flex-direction: column; gap: 7px; }
.cc-kpi {
  background: #fff; border-radius: 8px; padding: 10px 12px;
  border: 1px solid #DDE5EF;
}
.cc-kpi-label { font-size: 10.5px; color: #64748B; font-weight: 600; text-transform: uppercase;
                letter-spacing: .06em; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cc-kpi-val { font-size: 17px; font-weight: 700; line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cc-kpi-val.pos { color: #0F6E56; }
.cc-kpi-val.neg { color: #9B2C2C; }
.cc-kpi-sub { font-size: 10px; color: #94A3B8; margin-top: 3px; }
.cc-kpi-sub b { color: #64748B; }

/* Divisor de painel */
.cc-panel-title {
  font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .1em;
  color: #64748B; padding: 12px 12px 6px; border-top: 1px solid #DDE5EF; margin-top: 4px;
  background: #E8EEF5;
}

/* Barras de composição */
.cc-bar-list { padding: 0 10px 10px; display: flex; flex-direction: column; gap: 10px; }
.cc-bar-item { }
.cc-bar-header { display: flex; justify-content: space-between; align-items: baseline;
                 font-size: 11.5px; color: #334155; margin-bottom: 4px; font-weight: 500; }
.cc-bar-header span:last-child { font-size: 11.5px; font-weight: 700; font-variant-numeric: tabular-nums; }
.cc-bar-track { height: 8px; background: #DDE5EF; border-radius: 4px; overflow: hidden; }
.cc-bar-fill  { height: 100%; border-radius: 4px; transition: width .4s ease; }

/* Cascata */
.cc-waterfall { padding: 0 10px 14px; }
.cc-wf-grid { display: flex; align-items: flex-end; gap: 6px; height: 120px; }
.cc-wf-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; min-width: 0; }
.cc-wf-bar { width: 100%; border-radius: 3px 3px 0 0; }
.cc-wf-lbl { font-size: 9px; color: #475569; text-align: center; white-space: nowrap;
             overflow: hidden; text-overflow: ellipsis; width: 100%; font-weight: 600; }
.cc-wf-val { font-size: 8px; color: #64748B; text-align: center; white-space: nowrap; font-weight: 500; }

/* ── MODAL ───────────────────────────────────────────── */
#modal-overlay {
  display: none; position: absolute; top: 0; left: 0; width: 100%;
  background: rgba(10,35,66,.6); backdrop-filter: blur(3px);
  z-index: 9999;
}
#modal-overlay.open { display: block; }
#modal-box {
  background: #fff; border-radius: 12px;
  box-shadow: 0 24px 64px rgba(0,0,0,.3);
  width: 94%; max-width: 1020px; max-height: 500px;
  display: flex; flex-direction: column; overflow: hidden;
  animation: mIn .18s ease;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
@keyframes mIn { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
#modal-header { background: #0F2D52; padding: 14px 20px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
#modal-title  { color: #fff; font-size: 14px; font-weight: 700; }
#modal-total  { color: #8BBAD8; font-size: 11.5px; margin-top: 2px; }
#modal-close  { background: none; border: none; color: #6FA3C8; font-size: 22px; cursor: pointer; line-height: 1; padding: 0 4px; }
#modal-close:hover { color: #fff; }
#modal-body { overflow-y: auto; flex: 1; }
#modal-table { width: 100%; border-collapse: collapse; font-size: 12px; }
#modal-table thead th { position: sticky; top: 0; background: #F1F5F9; padding: 8px 12px;
  text-align: left; font-weight: 600; color: #475569; font-size: 10.5px;
  text-transform: uppercase; letter-spacing: .05em; border-bottom: 2px solid #E2E8F0; white-space: nowrap; }
#modal-table thead th.num { text-align: right; }
#modal-table tbody tr { border-bottom: 1px solid #F1F5F9; }
#modal-table tbody tr:hover { background: #F8FAFC; }
#modal-table tbody td { padding: 7px 12px; color: #334155; }
#modal-table tbody td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; font-weight: 500; }
#modal-table tbody td.pos { color: #0F6E56; }
#modal-table tbody td.neg { color: #C0392B; }
#modal-footer { background: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 9px 20px;
  display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #64748B; }
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
      '<tr><td colspan="' + cols.length + '" style="padding:20px;text-align:center;color:#94A3B8">Nenhuma linha</td></tr>';
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
document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeModal(); });

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
  btn.style.background = opening ? '#0F4C8A' : '#1D4580';
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
      <span>Pressione <kbd style="background:#E2E8F0;border-radius:3px;padding:1px 6px;font-size:10.5px">Esc</kbd> para fechar</span>
    </div>
  </div>
</div>

<!-- COMMAND CENTER -->
<div class="cc-shell">

  <!-- COLUNA ESQUERDA: DRE -->
  <div class="cc-dre">
    <table id="dre-table" class="meses-off">
      <thead>
        <tr style="background:#0F2D52;">
          <th class="td-label" style="padding:10px 14px;text-align:left;font-size:10px;font-weight:700;color:#7FADD4;letter-spacing:.1em;text-transform:uppercase;border:none;white-space:nowrap;"><button id="btn-meses" onclick="toggleMeses()" style="background:#1D4580;border:none;border-radius:4px;color:#7FADD4;font-size:9px;font-weight:700;letter-spacing:.05em;cursor:pointer;padding:3px 7px;margin-right:8px;vertical-align:middle;">▶ MESES</button>Descrição</th>
          <th class="td-pct"  style="padding:10px 8px;text-align:right;font-size:10px;font-weight:700;color:#7FADD4;letter-spacing:.1em;text-transform:uppercase;border:none;white-space:nowrap;">% MC</th>
""" + 
    "".join(
        f'          <th class="td-mes" data-mes="{m}" style="padding:10px 8px;text-align:right;font-size:10px;font-weight:700;'
        f'color:#4A7FAA;letter-spacing:.08em;text-transform:uppercase;border:none;white-space:nowrap;">{MESES_CURTO[m]}</th>'
        for m in meses_ativos
    ) + """
          <th class="td-val"  style="padding:10px 14px;text-align:right;font-size:10px;font-weight:700;color:#7FADD4;letter-spacing:.1em;text-transform:uppercase;border:none;white-space:nowrap;">Total (R$)</th>
          <th class="td-orc"  style="padding:10px 10px;text-align:right;font-size:10px;font-weight:700;color:#7FADD4;letter-spacing:.1em;text-transform:uppercase;border:none;white-space:nowrap;">Orçado (R$)</th>
          <th class="td-var"  style="padding:10px 10px;text-align:right;font-size:10px;font-weight:700;color:#7FADD4;letter-spacing:.1em;text-transform:uppercase;border:none;white-space:nowrap;">Var%</th>
        </tr>
      </thead>
      <tbody>
""" + tbody + """
      </tbody>
    </table>
  </div>

  <!-- COLUNA DIREITA: PAINEL -->
  <div class="cc-panel" id="side-panel">

    <div style="background:#0F2D52;padding:10px 12px;border-bottom:1px solid #1D4580;">
      <div style="font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#7FADD4;">Command Center</div>
      <div style="font-size:10px;color:#4A7FAA;margin-top:1px;">Resumo Executivo</div>
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
  { label:'Desp. Operac.', key:'Resultado Operacional (EBITDA)',    cor:'#185FA5' },
  { label:'Financeiro',    key:'Resultado Líquido do Exercício',    cor:'#0F6E56' },
];
/* Calcula cada parcela como diferença entre subtotais consecutivos */
var rl   = R['Receita Líquida']||0;
var ebit = R['Resultado Operacional (EBITDA)']||0;
var liq  = R['Resultado Líquido do Exercício']||0;
var parcelas = [
  { label:'Impostos',      val: Math.abs(MC - rl),   cor:'#D85A30' },
  { label:'Desp. Operac.', val: Math.abs(rl - ebit), cor:'#185FA5' },
  { label:'Financeiro',    val: Math.abs(ebit - liq), cor:'#0F6E56' },
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
  { lbl:'MC',    val:MC,   cor:'#5DCAA5' },
  { lbl:'Rec.L.',val:rl,   cor:'#378ADD' },
  { lbl:'EBITDA',val:ebit, cor: ebit>=0?'#7FADD4':'#F0997B' },
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
</body>
</html>""")
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

# 2. Limpa o texto das Empresas para a legenda (A variável que estava faltando)
empresas_limpas = [x.split(" - ", 1)[-1] if " - " in x else x for x in empresas_sel]

# 3. Constrói o HTML dos logos e nomes das empresas com tamanho de 85px
if len(empresas_limpas) <= 2:
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
    f"<h2 style='margin:0 0 10px 0; font-family:Inter,sans-serif; font-size:1.8rem;"
    f"font-weight:700; color:#0A2342; display:flex; align-items:center;'>"
    f"DRE Gerencial Consolidado "
    f"<span style='font-size: 1.4rem; color: #475569; font-weight: 500;'>{empresa_html_display}</span></h2>"
    f"<p style='margin:0; font-size:0.95rem; color:#64748B;'>"
    f"📅 <b>{periodo_str}</b> &nbsp;|&nbsp; "
    f"📋 <b>{', '.join(cenarios_sel)}</b> &nbsp;|&nbsp; "
    f"🎯 CRD: <b>{crd_str}</b></p>"
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
    df_f, df_orc, ESTRUTURA_DRE, SUBTOTAIS, SECOES,
    FORA_DRE, mostrar_orfaos, meses_ativos=meses_sel
)

import streamlit.components.v1 as components
components.html(html_dre, height=altura_dre, scrolling=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAINEL DE KPIs FINANCEIROS — abaixo da DRE
# ─────────────────────────────────────────────────────────────────────────────
# ── Valores-chave para os KPIs ───────────────────────────────────────────────
_venda_bruta = sum(
    _soma(df_f[df_f["dre"] == c], s)
    for c, s in {"VENDA BRUTA": +1}.items()
    if not df_f[df_f["dre"] == c].empty
)
_venda_liq  = resumo_executivo.get("Venda Líquida", 0)
_mc         = resumo_executivo.get("Margem de Contribuição / Lucro Bruto", 0)
_rec_liq    = resumo_executivo.get("Receita Líquida", 0)
_ebitda     = resumo_executivo.get("Resultado Operacional (EBITDA)", 0)
_liq        = resumo_executivo.get("Resultado Líquido do Exercício", 0)
_impostos   = _mc - _rec_liq
_desp_oper  = _rec_liq - _ebitda
_result_fin = _ebitda - _liq

def _pct_br(num, den, casas=1):
    if not den: return "—"
    v = (num / den) * 100
    return f"{'▲' if v >= 0 else '▼'} {abs(v):.{casas}f}%"

def _fmt_br(v):
    s = f"{abs(v):,.0f}".replace(",","X").replace(".",",").replace("X",".")
    return f"(R$ {s})" if v < 0 else f"R$ {s}"

def _cor_val(v):
    return "#0F6E56" if v >= 0 else "#C0392B"

def _bg_val(v):
    return "rgba(15,110,86,.07)" if v >= 0 else "rgba(192,57,43,.07)"

# ── 16 KPIs em 4 grupos, todos lado a lado ───────────────────────────────────
grupos_kpi = [
    {
        "titulo": "📊 Rentabilidade",
        "cor": "#0A5C8A",
        "kpis": [
            {"label":"Margem Bruta",      "val":_pct_br(_mc,_venda_bruta),    "raw":_mc/_venda_bruta*100 if _venda_bruta else 0,     "tip":"MC ÷ Venda Bruta — sobra após custos e comissões"},
            {"label":"Margem EBITDA",     "val":_pct_br(_ebitda,_venda_bruta),"raw":_ebitda/_venda_bruta*100 if _venda_bruta else 0, "tip":"EBITDA ÷ Venda Bruta — eficiência operacional"},
            {"label":"Margem Líquida",    "val":_pct_br(_liq,_venda_bruta),   "raw":_liq/_venda_bruta*100 if _venda_bruta else 0,    "tip":"Resultado Líquido ÷ Venda Bruta"},
            {"label":"Margem Rec. Líq.",  "val":_pct_br(_rec_liq,_venda_bruta),"raw":_rec_liq/_venda_bruta*100 if _venda_bruta else 0,"tip":"Receita Líquida ÷ Venda Bruta — após impostos"},
        ],
    },
    {
        "titulo": "💸 Estrutura de Custos",
        "cor": "#92400E",
        "kpis": [
            {"label":"Impostos / VB",     "val":_pct_br(_impostos,_venda_bruta),  "raw":_impostos/_venda_bruta*100 if _venda_bruta else 0,  "tip":"Carga de impostos sobre a venda bruta"},
            {"label":"Desp. Oper. / VB",  "val":_pct_br(_desp_oper,_venda_bruta), "raw":_desp_oper/_venda_bruta*100 if _venda_bruta else 0,  "tip":"Desp. Adm/Comercial/Mkt ÷ Venda Bruta"},
            {"label":"Result. Fin. / VB", "val":_pct_br(_result_fin,_venda_bruta),"raw":_result_fin/_venda_bruta*100 if _venda_bruta else 0,"tip":"Investimentos e receitas financeiras ÷ Venda Bruta"},
            {"label":"Eficiência Oper.",  "val":_pct_br(_desp_oper,_mc),          "raw":_desp_oper/_mc*100 if _mc else 0,                    "tip":"Desp. Operacionais ÷ MC — menor = mais eficiente"},
        ],
    },
    {
        "titulo": "📈 Conversão de Resultado",
        "cor": "#166534",
        "kpis": [
            {"label":"Retenção de MC",       "val":_pct_br(_mc,_venda_liq),    "raw":_mc/_venda_liq*100 if _venda_liq else 0,    "tip":"MC ÷ Venda Líquida"},
            {"label":"EBITDA / MC",          "val":_pct_br(_ebitda,_mc),       "raw":_ebitda/_mc*100 if _mc else 0,              "tip":"Quanto da MC vira EBITDA"},
            {"label":"Líq. / EBITDA",        "val":_pct_br(_liq,_ebitda),      "raw":_liq/_ebitda*100 if _ebitda else 0,         "tip":"Quanto do EBITDA vira resultado líquido"},
            {"label":"Aproveit. Global",     "val":_pct_br(_liq,_mc),          "raw":_liq/_mc*100 if _mc else 0,                 "tip":"Resultado Líquido ÷ MC — aproveitamento total da margem"},
        ],
    },
    {
        "titulo": "🏦 Valores do Período",
        "cor": "#2D3A7C",
        "kpis": [
            {"label":"Venda Bruta",          "val":_fmt_br(_venda_bruta), "raw":_venda_bruta, "tip":"Receita total antes de deduções"},
            {"label":"Margem Contribuição",  "val":_fmt_br(_mc),          "raw":_mc,          "tip":"Venda Bruta − Comissões − Custos + Reembolsos"},
            {"label":"EBITDA",               "val":_fmt_br(_ebitda),      "raw":_ebitda,      "tip":"Resultado antes de investimentos e financeiro"},
            {"label":"Resultado Líquido",    "val":_fmt_br(_liq),         "raw":_liq,         "tip":"Bottom line — lucro/prejuízo final do período"},
        ],
    },
]

# ── Renderiza KPIs com st.columns (largura total garantida) ──────────────────
st.markdown("""
<style>
.kpi-wrap {
  background: #F8FAFC; border: 1px solid #E2E8F0;
  border-radius: 10px; overflow: hidden;
}
.kpi-head {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 12px 8px; background: #fff; border-bottom: 2px solid;
}
.kpi-head-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.kpi-head-title {
  font-size: 11px; font-weight: 700; color: #1E293B;
  line-height: 1.3; font-family: Inter, sans-serif;
}
.kpi-body { display: flex; flex-direction: column; gap: 6px; padding: 8px; }
.kpi-c {
  border-radius: 7px; padding: 9px 11px 8px;
  border: 1px solid rgba(0,0,0,.07); position: relative;
  font-family: Inter, sans-serif; transition: box-shadow .12s;
}
.kpi-c:hover { box-shadow: 0 3px 10px rgba(15,45,82,.12); }
.kpi-c-stripe {
  position: absolute; top: 0; left: 0; right: 0;
  height: 2px; border-radius: 7px 7px 0 0;
}
.kpi-c-lbl {
  font-size: 9.5px; font-weight: 600; color: #64748B;
  text-transform: uppercase; letter-spacing: .05em;
  margin-bottom: 3px; line-height: 1.3;
}
.kpi-c-val {
  font-size: 16px; font-weight: 700; line-height: 1.15;
  font-variant-numeric: tabular-nums;
}
</style>
""", unsafe_allow_html=True)

_kpi_cols = st.columns(4)
for _col, _g in zip(_kpi_cols, grupos_kpi):
    _cor = _g["cor"]
    _cards = ""
    for _k in _g["kpis"]:
        _cv = _cor_val(_k["raw"])
        _bg = _bg_val(_k["raw"])
        _tip = _k["tip"]
        _lbl = _k["label"]
        _val = _k["val"]
        _cards += (
            '<div class="kpi-c" style="background:' + _bg + ';" title="' + _tip + '">'
            '<div class="kpi-c-stripe" style="background:' + _cor + ';"></div>'
            '<div class="kpi-c-lbl">' + _lbl + '</div>'
            '<div class="kpi-c-val" style="color:' + _cv + ';">' + _val + '</div>'
            '</div>'
        )
    _titulo = _g["titulo"]
    _html = (
        '<div class="kpi-wrap">'
        '<div class="kpi-head" style="border-color:' + _cor + ';">'
        '<span class="kpi-head-dot" style="background:' + _cor + ';"></span>'
        '<span class="kpi-head-title">' + _titulo + '</span></div>'
        '<div class="kpi-body">' + _cards + '</div></div>'
    )
    with _col:
        st.markdown(_html, unsafe_allow_html=True)

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
