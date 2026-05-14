# ============================================================
# sidebar.py — Navigasi Sidebar dengan Status Tahapan
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
from src.utils.constants import (
    PAGE_ORDER, PAGE_ICONS,
    SS_WORKFLOW_STATUS, SS_RAW_DATA, SS_VALIDATION_RESULT,
    SS_CLEAN_DATA, SS_TIME_SERIES, SS_MODEL_RESULT,
    SS_EVAL_METRICS, SS_FORECAST_RESULT,
    APP_TITLE, APP_VERSION,
)


def _compute_workflow_status() -> dict[str, str]:
    """
    Hitung status tiap tahapan berdasarkan session state.
    Returns dict: {page_name: "done" | "active" | "locked"}
    """
    # Menyimpan status navigasi tiap halaman (done, active, atau pending)
    status = {}
    # Mendapatkan halaman yang saat ini dibuka dari session state.
    # Jika belum ada, gunakan halaman pertama dari daftar PAGE_ORDER.
    current_page = st.session_state.get("current_page", PAGE_ORDER[0])

    # Kondisi "selesai" per halaman
    # Dictionary ini mendefinisikan syarat (boolean) agar sebuah tahapan dianggap sudah selesai.
    # Biasanya dicek berdasarkan eksistensi data spesifik di st.session_state.
    done_conditions = {
        # Halaman Beranda selalu dianggap bisa diakses/selesai
        "Beranda":                    True,
        # Selesai jika raw data (dataset mentah) sudah diunggah dan tersimpan
        "Upload Dataset":             SS_RAW_DATA in st.session_state and st.session_state[SS_RAW_DATA] is not None,
        # Selesai jika hasil proses pengecekan kualitas data sudah ada
        "Validasi Data":              SS_VALIDATION_RESULT in st.session_state and st.session_state[SS_VALIDATION_RESULT] is not None,
        # Selesai jika dataset sudah dibersihkan dari nilai kosong/anomali
        "Preprocessing":              SS_CLEAN_DATA in st.session_state and st.session_state[SS_CLEAN_DATA] is not None,
        # Selesai jika data sudah dibentuk ulang ke dalam format time series
        "Transformasi Time Series":   SS_TIME_SERIES in st.session_state and st.session_state[SS_TIME_SERIES] is not None,
        # Selesai jika analisis time series sudah dapat dilakukan (syarat sama dengan transformasi)
        "Analisis Time Series":       SS_TIME_SERIES in st.session_state and st.session_state[SS_TIME_SERIES] is not None,
        # Selesai jika model SARIMA sudah selesai dilatih dan menghasilkan output
        "Pemodelan SARIMA":           SS_MODEL_RESULT in st.session_state and st.session_state[SS_MODEL_RESULT] is not None,
        # Selesai jika metrik performa model (MAE, RMSE, MAPE) sudah dihitung
        "Evaluasi Model":             SS_EVAL_METRICS in st.session_state and st.session_state[SS_EVAL_METRICS] is not None,
        # Selesai jika hasil peramalan ke masa depan telah di-generate
        "Forecasting":                SS_FORECAST_RESULT in st.session_state and st.session_state[SS_FORECAST_RESULT] is not None,
        # Halaman perbandingan dan kesimpulan dianggap true (karena informatif, bisa diakses jika sudah sampai tahapnya)
        "Perbandingan Dataset":       True,
        "Kesimpulan":                 True,
    }

    # Iterasi semua halaman secara berurutan untuk menentukan status masing-masing
    for page in PAGE_ORDER:
        # Ambil status boolean selesai/belum, fallback ke False
        is_done = done_conditions.get(page, False)
        
        if is_done:
            status[page] = "done"      # Halaman ini sudah memenuhi syarat dan selesai
        elif page == current_page:
            status[page] = "active"    # Halaman ini sedang dibuka saat ini
        else:
            status[page] = "pending"   # Halaman ini belum selesai dan belum bisa diakses

    return status


def _inject_sidebar_toggle_js():
    """
    Inject tombol ☰ floating via components.html() (iframe same-origin).
    Menggunakan window.parent untuk akses DOM halaman utama Streamlit.
    Lebih reliable daripada st.markdown() karena <script> selalu dieksekusi.
    """
    # Mengeksekusi blok HTML/JS di dalam iframe tersembunyi yang memiliki akses ke dokumen parent.
    components.html("""
    <script>
    (function() {
        // Mengambil referensi ke window dan document parent (halaman utama Streamlit)
        const parent = window.parent;
        const doc    = parent.document;

        // ── Hapus tombol lama jika sudah ada (cegah duplikat saat rerun) ──
        // Streamlit sering memanggil ulang (rerun) UI-nya. Ini mencegah tombol ditumpuk berkali-kali.
        const existing = doc.getElementById('sarima-open-btn');
        if (existing) existing.remove();

        // ── Buat tombol floating ──────────────────────────────────────────
        // Membuat elemen button secara dinamis
        const btn = doc.createElement('button');
        btn.id = 'sarima-open-btn';
        btn.title = 'Buka Navigasi';
        btn.innerHTML = '&#9776;'; // Menambahkan ikon hamburger (☰) dengan entitas HTML
        
        // Menerapkan gaya CSS untuk menempelkan tombol di tepi kiri layar
        btn.style.cssText = [
            'position:fixed',
            'top:50%',                   // Berada tepat di tengah vertikal
            'left:0',                    // Menempel di tepi paling kiri
            'transform:translateY(-50%)',// Pusatkan berdasarkan tingginya sendiri
            'z-index:99999',             // Tetap di atas semua elemen UI lainnya
            'background:#0D3B66',        // Warna biru khas tema (brand color)
            'color:#ffffff',
            'border:none',
            'border-radius:0 8px 8px 0', // Melengkung hanya di sisi kanan
            'width:2rem',
            'height:3rem',
            'cursor:pointer',
            'font-size:1.1rem',
            'display:none',              // Default tidak terlihat, hanya muncul jika sidebar tertutup
            'align-items:center',
            'justify-content:center',
            'box-shadow:2px 2px 10px rgba(0,0,0,0.35)',
            'transition:width 0.2s ease',// Efek transisi mulus saat dihover
            'font-family:sans-serif',
        ].join(';');
        
        // Memasukkan elemen tombol ke dalam body dokumen Streamlit
        doc.body.appendChild(btn);

        // ── Hover effect ─────────────────────────────────────────────────
        // Menambah sedikit animasi ukuran (memanjang) ketika kursor berada di atas tombol
        btn.onmouseenter = () => { btn.style.width = '2.5rem'; btn.style.background = '#0066CC'; };
        btn.onmouseleave = () => { btn.style.width = '2rem';   btn.style.background = '#0D3B66'; };

        // ── Klik: simulasi full pointer sequence untuk React ─────────────
        btn.addEventListener('click', function() {

            // Helper: simulasikan klik yang React bisa kenali
            // React (framework di balik Streamlit) terkadang mengabaikan '.click()' standar dari JavaScript.
            // Kita perlu menyimulasikan siklus penuh event interaksi manusia (dari hover hingga klik).
            function reactClick(el) {
                ['pointerover','pointerenter','mouseover','mouseenter',
                 'pointermove','mousemove',
                 'pointerdown','mousedown',
                 'pointerup','mouseup','click'
                ].forEach(function(type) {
                    el.dispatchEvent(new MouseEvent(type, {
                        bubbles: true,
                        cancelable: true,
                        view: parent,
                        composed: true,
                    }));
                });
            }

            // Coba semua selector tombol native Streamlit
            // Streamlit sering mengubah struktur HTML-nya pada update versi.
            // Array ini berisi berbagai kemungkinan selector untuk menargetkan tombol native Streamlit.
            const targets = [
                '[data-testid="stSidebarCollapsedControl"] button',
                '[data-testid="collapsedControl"] button',
                'button[aria-label="Open sidebar"]',
                'button[aria-label="open sidebar"]',
                'button[aria-label="Toggle sidebar visibility"]',
                '.st-emotion-cache-1dp5vir button',
            ];
            
            let clicked = false;
            // Lakukan perulangan mencoba satu-satu selector di atas
            for (const sel of targets) {
                const el = doc.querySelector(sel);
                if (el) {
                    // Jika ditemukan elemennya, simulasikan klik ala React
                    reactClick(el);
                    clicked = true;
                    break;
                }
            }

            // Fallback: paksa CSS sidebar agar terlihat langsung
            // Jika tombol native tak ditemukan sama sekali, ini opsi darurat untuk menimpa CSS sidebar secara paksa
            if (!clicked) {
                const sidebar = doc.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.setProperty('transform', 'none', 'important');
                    sidebar.style.setProperty('min-width', '21rem', 'important');
                    sidebar.style.setProperty('margin-left', '0', 'important');
                    sidebar.style.setProperty('visibility', 'visible', 'important');
                }
            }
        });

        // ── Deteksi sidebar collapsed / expanded ─────────────────────────
        // Fungsi untuk mengecek secara kontinu apakah sidebar saat ini terbuka atau tertutup
        function checkState() {
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            // Jika lebar sidebar sangat kecil (kurang dari 50px), itu tandanya tertutup (collapsed)
            const collapsed = sidebar.getBoundingClientRect().width < 50;
            // Atur tampilan tombol floating: tampilkan jika collapsed, sembunyikan jika expanded
            btn.style.display = collapsed ? 'flex' : 'none';
        }

        // Jalankan pengecekan pertama, lalu ulangi pengecekan setiap 400 milidetik (Polling)
        checkState();
        setInterval(checkState, 400);
    })();
    </script>
    """, height=0, scrolling=False) # Ukuran iframe dibuat nol agar tersembunyi tanpa merusak layout


def render_sidebar():
    """Render sidebar navigasi lengkap dengan status tahapan."""
    # Inject tombol floating buka sidebar
    # Pemanggilan ini wajib ditaruh di luar scope `with st.sidebar:` 
    # agar komponen iframe JavaScript tetap menyala/dieksekusi walau sidebar ditutup
    _inject_sidebar_toggle_js()

    # Memulai pembentukan UI untuk bagian panel kiri (sidebar)
    with st.sidebar:
        # ── Logo / Brand ─────────────────────────────────────
        # Render kop logo/judul aplikasi menggunakan HTML & CSS sebaris
        st.markdown(
            f"""
            <div style="padding:1.2rem 0.5rem 0.8rem 0.5rem;border-bottom:1px solid rgba(255,255,255,0.15);margin-bottom:1rem;">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.1em;opacity:0.6;text-transform:uppercase;">
                    Tugas Akhir
                </div>
                <div style="font-size:1.1rem;font-weight:800;margin-top:0.2rem;line-height:1.3;">
                    Dashboard Forecasting<br/>
                    <span style="color:rgba(33,150,243,0.9);">SARIMA</span>
                </div>
                <div style="font-size:0.7rem;opacity:0.5;margin-top:0.4rem;">v{APP_VERSION}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Menu Navigasi ─────────────────────────────────────
        # Label pemisah untuk sesi menu
        st.markdown(
            '<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.08em;opacity:0.55;text-transform:uppercase;margin-bottom:0.4rem;padding:0 0.5rem;">NAVIGASI</div>',
            unsafe_allow_html=True,
        )

        # Dapatkan menu yang sedang aktif saat ini
        current_page = st.session_state.get("current_page", PAGE_ORDER[0])
        # Dapatkan mapping tahapan apa saja yang berstatus selesai/active/pending
        workflow_status = _compute_workflow_status()

        # Render baris-baris tombol navigasi dari halaman ke-1 hingga terakhir
        for page in PAGE_ORDER:
            icon = PAGE_ICONS.get(page, "•") # Ambil ikon spesifik, jika tak ada gunakan dot (•)
            ws = workflow_status.get(page, "pending")

            # Jika tahapan tersebut sudah terselesaikan, maka berikan penanda checkmark
            if ws == "done":
                badge = "✓"
                badge_color = "rgba(46,204,113,0.9)"
            else:
                badge = ""
                badge_color = "transparent"

            is_active = page == current_page
            # Siapkan penanda visual aktif (garis biru di pinggir kiri) jika menu tsb aktif
            active_style = (
                "background:rgba(33,150,243,0.2);border-left:3px solid #2196F3;font-weight:600;"
                if is_active else "border-left:3px solid transparent;"
            )

            # Buat instance tombol Streamlit reguler yang mengisi panjang maksimal sidebar
            clicked = st.button(
                f"{icon}  {page}", 
                key=f"nav_{page}", 
                use_container_width=True, 
                help=f"Navigasi ke {page}",
            )
            
            # Action (aksi) yang diambil apabila menu ditekan user
            if clicked:
                st.session_state["current_page"] = page # Ubah sesi aktif sesuai yg dituju
                st.rerun()                              # Paksa muat ulang agar merender page baru

        # ── Footer Sidebar ────────────────────────────────────
        # Render catatan kecil berformat banner tempel untuk dasar layar bagian sidebar
        st.markdown(
            """
            <div style="
                position:fixed; bottom:0; left:0;
                padding:0.8rem 1.2rem;
                font-size:0.7rem;
                opacity:0.45;
                border-top:1px solid rgba(255,255,255,0.1);
                width:18rem;
                background:linear-gradient(160deg,#1E3A5F,#16324f);
            ">
                📌 Metode: SARIMA<br/>
                🔬 Data: Empiris & Simulasi
            </div>
            """,
            unsafe_allow_html=True,
        )
