# ============================================================
# preprocessing_page.py — Halaman Preprocessing (Issue 2&3)
# ============================================================

import streamlit as st
import plotly.graph_objects as go
from src.core.preprocessing import preprocess
from src.ui.cards import page_header, show_metrics_row
from src.ui.messages import show_success, show_error, show_warning, show_section_title, show_info
from src.ui.tables import show_dataframe
from src.utils.constants import SS_RAW_DATA, SS_COL_MAPPING, SS_CLEAN_DATA, COLOR_PRIMARY


def render():
    page_header(
        "Preprocessing Data",
        "Pembersihan data: konversi tipe data, hapus nilai kosong dan duplikasi, serta pengurutan.",
        "🔧",
    )

    raw_data    = st.session_state.get(SS_RAW_DATA)
    col_mapping = st.session_state.get(SS_COL_MAPPING, {})

    if raw_data is None:
        show_warning("Dataset belum tersedia. Kembali ke Upload Dataset.")
        if st.button("← Upload Dataset"):
            st.session_state["current_page"] = "Upload Dataset"
            st.rerun()
        return

    col_period   = col_mapping.get("periode")
    col_value    = col_mapping.get("nilai")
    col_category = col_mapping.get("kategori")

    # ── Jalankan Preprocessing ────────────────────────────────
    with st.spinner("Membersihkan data..."):
        clean_df, summary = preprocess(raw_data, col_period, col_value, col_category)
    st.session_state[SS_CLEAN_DATA] = clean_df

    show_success(f"Preprocessing selesai. Data siap untuk transformasi.")

    # ── Ringkasan Perubahan ───────────────────────────────────
    show_section_title("📊 Ringkasan Preprocessing")
    show_metrics_row([
        {"label": "Baris Sebelum",    "value": f"{summary['before_rows']:,}",       "color": "#9C27B0"},
        {"label": "Baris Sesudah",    "value": f"{summary['after_rows']:,}",        "color": "#4CAF50"},
        {"label": "Baris Dihapus",    "value": f"{summary['before_rows'] - summary['after_rows']:,}", "color": "#FF9800"},
        {"label": "Duplikat Dihapus", "value": str(summary["dropped_duplicates"]), "color": "#2196F3"},
    ])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Detail Proses ─────────────────────────────────────────
    show_section_title("🔍 Detail Proses Pembersihan")
    steps_done = [
        ("Penghapusan baris kosong",        f"{summary['dropped_empty']} baris dihapus"),
        ("Konversi kolom nilai ke numerik",  f"{summary['converted_numeric']} baris tidak valid dihapus"),
        ("Konversi periode ke datetime",     "Selesai"),
        ("Penghapusan duplikasi",            f"{summary['dropped_duplicates']} baris dihapus"),
        ("Pengurutan berdasarkan periode",   "Selesai"),
    ]
    rows_html = "".join(
        f"""<tr style="border-bottom:1px solid rgba(0,0,0,0.05);">
            <td style="padding:0.55rem 1rem;">✅ {s[0]}</td>
            <td style="padding:0.55rem 1rem;color:#2196F3;font-size:0.88rem;">{s[1]}</td>
        </tr>"""
        for s in steps_done
    )
    st.markdown(
        f"""
        <div class="sarima-card">
        <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;font-size:0.9rem;">
            <thead>
                <tr style="background:#1E3A5F;color:white;">
                    <th style="padding:0.65rem 1rem;text-align:left;">Proses</th>
                    <th style="padding:0.65rem 1rem;text-align:left;">Hasil</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Preview Data Bersih ───────────────────────────────────
    show_section_title("👁️ Preview Data Bersih")
    st.markdown(
        f'<div class="sarima-card" style="padding:0.5rem;margin-bottom:0.5rem;">'
        f'Menampilkan {min(10, len(clean_df))} dari {len(clean_df):,} baris data bersih.</div>',
        unsafe_allow_html=True,
    )
    show_dataframe(clean_df, max_rows=10)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Visualisasi Data Bersih ───────────────────────────────
    show_section_title("📊 Visualisasi Data Bersih")
    show_info("Grafik berikut menampilkan distribusi dan tren data setelah proses pembersihan.")

    col_hist, col_trend = st.columns(2)

    nilai_col = "nilai"
    if nilai_col in clean_df.columns:
        with col_hist:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=clean_df[nilai_col].dropna(),
                nbinsx=20,
                marker_color="#2196F3",
                opacity=0.75,
                hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>",
                name="Distribusi Nilai",
            ))
            fig_hist.update_layout(
                font=dict(family="Inter, sans-serif", size=12),
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="Nilai", yaxis_title="Frekuensi",
                title=dict(text="Histogram Distribusi Nilai", font=dict(size=14, color=COLOR_PRIMARY), x=0),
                height=300, bargap=0.05,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_trend:
            # Ambil kolom periode jika ada
            periode_col = "periode"
            if periode_col in clean_df.columns:
                df_sorted = clean_df.sort_values(periode_col)
                # Jika ada kolom kategori, ambil satu kategori saja
                if "kategori" in df_sorted.columns:
                    first_cat = df_sorted["kategori"].dropna().unique()
                    if len(first_cat) > 0:
                        df_sorted = df_sorted[df_sorted["kategori"] == first_cat[0]]
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=list(df_sorted[periode_col]),
                    y=df_sorted[nilai_col].values,
                    mode="lines+markers",
                    name="Tren Data Bersih",
                    line=dict(color="#4CAF50", width=2),
                    marker=dict(size=5),
                    fill="tozeroy", fillcolor="rgba(76,175,80,0.07)",
                    hovertemplate="%{x}<br>Nilai: %{y:,.0f}<extra></extra>",
                ))
                fig_trend.update_layout(
                    font=dict(family="Inter, sans-serif", size=12),
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Periode", yaxis_title="Nilai",
                    title=dict(text="Tren Data Bersih", font=dict(size=14, color=COLOR_PRIMARY), x=0),
                    height=300,
                )
                st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Navigasi ──────────────────────────────────────────────
    col1, col2, _ = st.columns([2, 2, 2])
    with col1:
        if st.button("← Validasi Data", use_container_width=True):
            st.session_state["current_page"] = "Validasi Data"
            st.rerun()
    with col2:
        if st.button("🔄  Lanjut ke Transformasi", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Transformasi Time Series"
            st.rerun()

