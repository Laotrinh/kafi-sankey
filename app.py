"""
KAFI Financial Sankey App
Chạy: streamlit run app.py
"""
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="KAFI Sankey", layout="wide", page_icon="📊")

# ─── Màu KAFI ────────────────────────────────────────────────
C = {
    "g1":"#00C391","g2":"#07746E","g3":"#00D49A",
    "r1":"#C00000","r2":"#E53E3E","r3":"#EF9A9A",
    "y2":"#E8A020","b1":"#098A7E","b2":"#4A9B7F","b3":"#26A69A",
    "sl":"#455A64",
}

def rgba(h, op):
    r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    return f"rgba({r},{g},{b},{op})"

def lbl(name, v25, v24=None):
    if v24 and v24 > 0.01:
        p = (v25 - v24) / abs(v24) * 100
        yoy = f" <b>{'+' if p>=0 else ''}{p:.0f}%</b>"
        col = C["g1"] if p >= 0 else C["r2"]
    else:
        yoy, col = "", C["g1"]
    return (f"<b>{name}</b><br>"
            f"<span style='font-size:10px'>{v25:,.1f} tỷ"
            f"<span style='color:{col}'>{yoy}</span></span>  ")

def make_sankey(nodes, links, title, h=1000):
    N  = [lbl(*n[:3]) for n in nodes]
    NC = [n[3] for n in nodes]
    S  = [l[0] for l in links]
    T  = [l[1] for l in links]
    V  = [l[2] for l in links]
    LC = [rgba(l[3], l[4]) for l in links]
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(pad=24, thickness=36, label=N, color=NC,
                  line=dict(color="rgba(0,0,0,0.06)", width=0.8),
                  hovertemplate='%{label}<extra></extra>', align='left'),
        link=dict(source=S, target=T, value=V, color=LC,
                  hovertemplate='%{source.label}→%{target.label}<br><b>%{value:,.1f}</b> tỷ<extra></extra>')
    ))
    fig.update_layout(
        title_text=title, title_x=0.5,
        title_font=dict(size=22, color=C["g2"], family="Inter, sans-serif"),
        font=dict(family="Inter, sans-serif", size=12, color="#2E2E2E"),
        height=h, paper_bgcolor="white",
        plot_bgcolor="rgba(250,250,250,0.95)",
        margin=dict(l=60, r=100, t=120, b=60)
    )
    fig.add_annotation(text="© KAFI Research", x=0.99, y=0.01,
        xref="paper", yref="paper", showarrow=False,
        font=dict(size=10, color=rgba(C["g2"], .4), family="Inter"), xanchor="right")
    return fig


# ════════════════════════════════════════════════════════════════
# UI
# ════════════════════════════════════════════════════════════════
st.title("📊 KAFI Financial Sankey")
st.caption("Cập nhật số liệu → xem chart ngay tức thì")

tab1, tab2 = st.tabs(["📈 P&L — Kết quả hoạt động", "🏦 BCĐKT — Bảng cân đối"])


# ════════════════════════════════════════════════════════════════
# TAB 1 — P&L
# ════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Nhập số liệu P&L (tỷ VND)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Doanh thu**")
        fvtpl    = st.number_input("FVTPL (tự doanh) FY25",      value=1776.1, step=0.1, key="fvtpl25")
        fvtpl4   = st.number_input("FVTPL FY24",                  value=606.1,  step=0.1, key="fvtpl24")
        afs      = st.number_input("Lãi AFS FY25",                value=123.8,  step=0.1, key="afs25")
        afs4     = st.number_input("Lãi AFS FY24",                value=0.7,    step=0.1, key="afs24")
        margin   = st.number_input("Lãi cho vay (margin) FY25",   value=775.9,  step=0.1, key="mg25")
        margin4  = st.number_input("Lãi cho vay FY24",            value=260.2,  step=0.1, key="mg24")
        mgioi    = st.number_input("Môi giới CK FY25",            value=158.9,  step=0.1, key="mgioi25")
        mgioi4   = st.number_input("Môi giới CK FY24",            value=87.6,   step=0.1, key="mgioi24")
        luuky    = st.number_input("Lưu ký CK FY25",              value=5.2,    step=0.1, key="lk25")
        luuky4   = st.number_input("Lưu ký CK FY24",              value=2.2,    step=0.1, key="lk24")
        ib       = st.number_input("IB & tư vấn tài chính FY25",  value=0.8,    step=0.1, key="ib25")
        ib4      = st.number_input("IB & tư vấn tài chính FY24",  value=0.3,    step=0.1, key="ib24")
        other    = st.number_input("Thu nhập HĐ khác FY25",       value=1.0,    step=0.1, key="oth25")
        other4   = st.number_input("Thu nhập HĐ khác FY24",       value=0.2,    step=0.1, key="oth24")

    with c2:
        st.markdown("**Chi phí**")
        cpfvtpl  = st.number_input("Lỗ/CP FVTPL FY25",            value=1142.7, step=0.1, key="cpf25")
        cpfvtpl4 = st.number_input("Lỗ/CP FVTPL FY24",            value=116.1,  step=0.1, key="cpf24")
        cpafs    = st.number_input("CP AFS FY25",                  value=21.8,   step=0.1, key="cpa25")
        cpvay    = st.number_input("CP dự phòng cho vay FY25",     value=81.7,   step=0.1, key="cpv25")
        cpvay4   = st.number_input("CP dự phòng cho vay FY24",     value=60.3,   step=0.1, key="cpv24")
        cptd     = st.number_input("CP tự doanh FY25",             value=32.5,   step=0.1, key="cptd25")
        cptd4    = st.number_input("CP tự doanh FY24",             value=12.7,   step=0.1, key="cptd24")
        cpmgioi  = st.number_input("CP môi giới CK FY25",          value=167.1,  step=0.1, key="cpm25")
        cpmgioi4 = st.number_input("CP môi giới CK FY24",          value=95.3,   step=0.1, key="cpm24")
        cpluuky  = st.number_input("CP lưu ký CK FY25",            value=9.8,    step=0.1, key="cplk25")
        cpluuky4 = st.number_input("CP lưu ký CK FY24",            value=2.6,    step=0.1, key="cplk24")

        st.markdown("**Tài chính & Quản lý**")
        cptc     = st.number_input("CP tài chính (tổng) FY25",     value=767.8,  step=0.1, key="cptc25")
        cptc4    = st.number_input("CP tài chính FY24",            value=311.5,  step=0.1, key="cptc24")
        dttc     = st.number_input("DT tài chính FY25",            value=34.7,   step=0.1, key="dttc25")
        dttc4    = st.number_input("DT tài chính FY24",            value=14.0,   step=0.1, key="dttc24")
        cpql     = st.number_input("CP quản lý FY25",              value=197.3,  step=0.1, key="cpql25")
        cpql4    = st.number_input("CP quản lý FY24",              value=116.0,  step=0.1, key="cpql24")

        st.markdown("**Kết quả**")
        lntt     = st.number_input("LNTT FY25",                    value=457.5,  step=0.1, key="lntt25")
        lntt4    = st.number_input("LNTT FY24",                    value=256.7,  step=0.1, key="lntt24")
        thue     = st.number_input("Thuế TNDN FY25",               value=92.9,   step=0.1, key="thue25")
        thue4    = st.number_input("Thuế TNDN FY24",               value=53.2,   step=0.1, key="thue24")
        lnst     = st.number_input("LN sau thuế FY25",             value=364.7,  step=0.1, key="lnst25")
        lnst4    = st.number_input("LN sau thuế FY24",             value=203.5,  step=0.1, key="lnst24")

    # Tính suy ra
    dt       = fvtpl + afs + margin + mgioi + luuky + ib + other
    dt4      = fvtpl4 + afs4 + margin4 + mgioi4 + luuky4 + ib4 + other4
    cphd     = cpfvtpl + cpafs + cpvay + cptd + cpmgioi + cpluuky
    cphd4    = cpfvtpl4 + cpvay4 + cptd4 + cpmgioi4 + cpluuky4
    lngop    = dt - cphd
    lngop4   = dt4 - cphd4
    cp_tc_net = cptc - dttc
    cp_tc_net4 = cptc4 - dttc4
    lntt_link = lngop - cp_tc_net - cpql

    st.info(f"**Tổng DT:** {dt:,.1f} tỷ | **LN gộp:** {lngop:,.1f} tỷ | **CP TC ròng:** {cp_tc_net:,.1f} tỷ | **LNTT link:** {lntt_link:,.1f} tỷ")

    PL_NODES = [
        ("FVTPL (tự doanh)",        fvtpl,    fvtpl4,  C["g2"]),
        ("Lãi AFS",                 afs,      afs4,    C["b3"]),
        ("Lãi cho vay (margin)",    margin,   margin4, C["b1"]),
        ("Môi giới CK",             mgioi,    mgioi4,  C["b2"]),
        ("Lưu ký CK",               luuky,    luuky4,  C["b2"]),
        ("IB & tư vấn tài chính",   ib,       ib4,     C["b2"]),
        ("Thu nhập HĐ khác",        other,    other4,  C["b2"]),
        ("Doanh thu hoạt động",     dt,       dt4,     C["g2"]),
        ("CP hoạt động KD",         cphd,     cphd4,   C["r1"]),
        ("Lợi nhuận gộp",           lngop,    lngop4,  C["g1"]),
        ("Lỗ/CP FVTPL",             cpfvtpl,  cpfvtpl4,C["r1"]),
        ("CP AFS",                  cpafs,    0.001,   C["r2"]),
        ("CP dự phòng cho vay",     cpvay,    cpvay4,  C["r2"]),
        ("CP tự doanh",             cptd,     cptd4,   C["r3"]),
        ("CP môi giới CK",          cpmgioi,  cpmgioi4,C["r2"]),
        ("CP lưu ký CK",            cpluuky,  cpluuky4,C["r3"]),
        ("CP tài chính (lãi vay)",  cp_tc_net,cp_tc_net4,C["r2"]),
        ("CP quản lý",              cpql,     cpql4,   C["y2"]),
        ("LNTT",                    lntt,     lntt4,   C["g2"]),
        ("Thuế TNDN",               thue,     thue4,   C["y2"]),
        ("Lợi nhuận sau thuế",      lnst,     lnst4,   C["g3"]),
    ]
    PL_LINKS = [
        (0,7,fvtpl,   C["g2"],.32),(1,7,afs,     C["b3"],.28),
        (2,7,margin,  C["b1"],.32),(3,7,mgioi,   C["b2"],.28),
        (4,7,luuky,   C["b2"],.22),(5,7,ib,      C["b2"],.20),
        (6,7,other,   C["b2"],.18),
        (7,8,cphd,    C["r1"],.25),(7,9,lngop,   C["g1"],.32),
        (8,10,cpfvtpl,C["r1"],.28),(8,11,cpafs,  C["r2"],.22),
        (8,12,cpvay,  C["r2"],.22),(8,13,cptd,   C["r3"],.20),
        (8,14,cpmgioi,C["r2"],.22),(8,15,cpluuky,C["r3"],.20),
        (9,16,cp_tc_net,C["r2"],.28),(9,17,cpql, C["y2"],.25),
        (9,18,lntt_link,C["g2"],.38),
        (18,19,thue,  C["y2"],.30),(18,20,lnst,  C["g3"],.42),
    ]

    fig_pl = make_sankey(
        PL_NODES, PL_LINKS,
        "<b>KAFI FY2025</b><br><sup>Báo cáo kết quả hoạt động - Đơn vị: tỷ VND | Kafi Research</sup>",
        h=1000
    )
    st.plotly_chart(fig_pl, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 — BCĐKT
# ════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Nhập số liệu BCĐKT (tỷ VND)")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Tài sản**")
        bs_margin   = st.number_input("Cho vay KH (margin) cuối năm",   value=10882.9, step=0.1, key="bsmg25")
        bs_margin4  = st.number_input("Cho vay KH đầu năm",             value=5359.6,  step=0.1, key="bsmg24")
        bs_fvtpl    = st.number_input("FVTPL cuối năm",                 value=8100.2,  step=0.1, key="bsfv25")
        bs_fvtpl4   = st.number_input("FVTPL đầu năm",                  value=8880.0,  step=0.1, key="bsfv24")
        bs_afs      = st.number_input("AFS (trái phiếu) cuối năm",      value=5090.7,  step=0.1, key="bsafs25")
        bs_afs4     = st.number_input("AFS đầu năm",                    value=659.9,   step=0.1, key="bsafs24")
        bs_tien     = st.number_input("Tiền & tương đương cuối năm",    value=1625.0,  step=0.1, key="bst25")
        bs_tien4    = st.number_input("Tiền & tương đương đầu năm",     value=943.9,   step=0.1, key="bst24")
        bs_pt       = st.number_input("Các khoản phải thu cuối năm",    value=254.1,   step=0.1, key="bspt25")
        bs_pt4      = st.number_input("Các khoản phải thu đầu năm",     value=123.5,   step=0.1, key="bspt24")
        bs_tsnh     = st.number_input("TS ngắn hạn khác cuối năm",      value=17.4,    step=0.1, key="bsnh25")
        bs_tsnh4    = st.number_input("TS ngắn hạn khác đầu năm",       value=8.4,     step=0.1, key="bsnh24")
        bs_tt       = st.number_input("Trả trước & PT DV cuối năm",     value=22.4,    step=0.1, key="bstt25")
        bs_tt4      = st.number_input("Trả trước & PT DV đầu năm",      value=13.6,    step=0.1, key="bstt24")
        bs_tsdh     = st.number_input("Tài sản dài hạn cuối năm",       value=139.4,   step=0.1, key="bsdh25")
        bs_tsdh4    = st.number_input("Tài sản dài hạn đầu năm",        value=75.5,    step=0.1, key="bsdh24")

    with c4:
        st.markdown("**Nguồn vốn**")
        bs_tts      = st.number_input("Tổng tài sản cuối năm",          value=26131.5, step=0.1, key="bstts25")
        bs_tts4     = st.number_input("Tổng tài sản đầu năm",           value=16054.9, step=0.1, key="bstts24")
        bs_vaynh    = st.number_input("Vay ngắn hạn cuối năm",          value=17537.6, step=0.1, key="bsvn25")
        bs_vaynh4   = st.number_input("Vay ngắn hạn đầu năm",           value=10474.1, step=0.1, key="bsvn24")
        bs_ptrahd   = st.number_input("Phải trả HĐ & người bán cuối năm",value=402.9,  step=0.1, key="bsph25")
        bs_ptrahd4  = st.number_input("Phải trả HĐ & người bán đầu năm", value=3.8,    step=0.1, key="bsph24")
        bs_nokhac   = st.number_input("Thuế, CP phải trả & khác cuối năm",value=319.2, step=0.1, key="bsnk25")
        bs_nokhac4  = st.number_input("Thuế, CP phải trả & khác đầu năm", value=290.0, step=0.1, key="bsnk24")
        bs_vongop   = st.number_input("Vốn góp cuối năm",               value=7500.0,  step=0.1, key="bsvg25")
        bs_vongop4  = st.number_input("Vốn góp đầu năm",                value=5000.0,  step=0.1, key="bsvg24")
        bs_lnpp     = st.number_input("LNST chưa phân phối cuối năm",   value=371.6,   step=0.1, key="bslnpp25")
        bs_lnpp4    = st.number_input("LNST chưa phân phối đầu năm",    value=272.7,   step=0.1, key="bslnpp24")

    BS_NODES = [
        ("Cho vay KH (margin)",      bs_margin,  bs_margin4,  C["b1"]),
        ("FVTPL (tự doanh)",         bs_fvtpl,   bs_fvtpl4,   C["g2"]),
        ("AFS (trái phiếu)",         bs_afs,     bs_afs4,     C["b2"]),
        ("Tiền & tương đương",       bs_tien,    bs_tien4,    C["g1"]),
        ("Các khoản phải thu",       bs_pt,      bs_pt4,      C["b3"]),
        ("TS ngắn hạn khác",         bs_tsnh,    bs_tsnh4,    C["b3"]),
        ("Trả trước & PT DV",        bs_tt,      bs_tt4,      C["b3"]),
        ("Tài sản dài hạn",          bs_tsdh,    bs_tsdh4,    C["b3"]),
        ("Tổng tài sản",             bs_tts,     bs_tts4,     C["sl"]),
        ("Vay ngắn hạn",             bs_vaynh,   bs_vaynh4,   C["r1"]),
        ("Phải trả HĐ & người bán",  bs_ptrahd,  bs_ptrahd4,  C["r2"]),
        ("Thuế, CP phải trả & khác", bs_nokhac,  bs_nokhac4,  C["r2"]),
        ("Vốn góp",                  bs_vongop,  bs_vongop4,  C["g2"]),
        ("LNST chưa phân phối",      bs_lnpp,    bs_lnpp4,    C["g1"]),
    ]
    BS_LINKS = [
        (0,8,bs_margin,  C["b1"],.30),(1,8,bs_fvtpl,  C["g2"],.28),
        (2,8,bs_afs,     C["b2"],.28),(3,8,bs_tien,   C["g1"],.28),
        (4,8,bs_pt,      C["b3"],.22),(5,8,bs_tsnh,   C["b3"],.20),
        (6,8,bs_tt,      C["b3"],.20),(7,8,bs_tsdh,   C["b3"],.18),
        (8,9,bs_vaynh,   C["r1"],.28),(8,10,bs_ptrahd,C["r2"],.22),
        (8,11,bs_nokhac, C["r2"],.20),(8,12,bs_vongop,C["g2"],.32),
        (8,13,bs_lnpp,   C["g1"],.30),
    ]

    fig_bs = make_sankey(
        BS_NODES, BS_LINKS,
        "<b>KAFI — Bảng cân đối kế toán 31/12/2025</b><br><sup>Cấu trúc tài sản & nguồn vốn - Đơn vị: tỷ VND | Kafi Research</sup>",
        h=900
    )
    st.plotly_chart(fig_bs, use_container_width=True)
