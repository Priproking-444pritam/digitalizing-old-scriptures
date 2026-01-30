import streamlit as st
import sqlite3
import os
from PIL import Image
from IndicPhotoOCR.ocr import OCR

# ================= PAGE =================
st.set_page_config("Digitalization of old Scriptures (Odia)", "📜", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
/* Remove Streamlit top gap */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0 !important;
}

/* Remove broken overlay div */
.overlay {
    display: none !important;
}

/* Elegant vintage manuscript background */
.stApp {
    background: linear-gradient(135deg, 
        #f8f3e9 0%, 
        #f5efdf 25%, 
        #f2e9d5 50%, 
        #efe3cb 75%, 
        #ecddc1 100%);
    background-attachment: fixed;
    background-size: cover;
}

/* Main content wrapper with subtle texture */
.main-wrapper {
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" opacity="0.03"><defs><pattern id="paper" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="40" height="40" fill="none" stroke="%235d4037" stroke-width="0.5"/></pattern></defs><rect width="100%25" height="100%25" fill="url(%23paper)"/></svg>'),
                linear-gradient(to bottom, rgba(255, 253, 248, 0.95), rgba(255, 251, 240, 0.98));
    border-radius: 24px;
    box-shadow: 
        0 15px 50px rgba(93, 64, 55, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    padding: 2.5rem 3rem;
    margin: 1.5rem auto;
    max-width: 1400px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(166, 124, 82, 0.2);
}

/* Decorative corner elements */
.main-wrapper::before,
.main-wrapper::after {
    content: '';
    position: absolute;
    width: 80px;
    height: 80px;
    background: transparent;
    z-index: 1;
}

.main-wrapper::before {
    top: 15px;
    left: 15px;
    border-top: 3px solid #a67c52;
    border-left: 3px solid #a67c52;
    border-radius: 10px 0 0 0;
}

.main-wrapper::after {
    bottom: 15px;
    right: 15px;
    border-bottom: 3px solid #a67c52;
    border-right: 3px solid #a67c52;
    border-radius: 0 0 10px 0;
}

/* Custom tab styling - elegant book-like tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
    padding: 0 1rem;
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    padding: 1rem 2.5rem;
    border-radius: 15px 15px 0 0;
    background: linear-gradient(to bottom, #f5f0e6, #e8dfd0);
    font-weight: 700;
    font-size: 1.1rem;
    color: #5d4037;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid #d7ccc8;
    border-bottom: none;
    position: relative;
    transform: translateY(2px);
    box-shadow: 0 -3px 10px rgba(0, 0, 0, 0.05);
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(to bottom, #f9f5ec, #f0e9dc);
    transform: translateY(0);
    box-shadow: 0 -5px 15px rgba(166, 124, 82, 0.1);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(to bottom, #ffffff, #f8f3e9) !important;
    color: #3e2723 !important;
    border-color: #a67c52 !important;
    border-bottom: 2px solid transparent !important;
    z-index: 10;
    transform: translateY(0);
    box-shadow: 0 0 20px rgba(166, 124, 82, 0.15);
}

/* Hero header */
.hero-header {
    text-align: center;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid #e0d6cc;
    position: relative;
}

.hero-header h1 {
    color: #3e2723;
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
    font-size: 3.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    letter-spacing: 1px;
}

.hero-tagline {
    color: #6d4c41;
    font-size: 1.3rem;
    font-style: italic;
    margin-bottom: 1rem;
    font-family: 'Georgia', serif;
}

/* Decorative separator */
.separator {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 2rem 0;
    color: #8d6e63;
}

.separator::before,
.separator::after {
    content: '';
    flex: 1;
    border-bottom: 2px solid #d7ccc8;
}

.separator::before {
    margin-right: 1.5rem;
}

.separator::after {
    margin-left: 1.5rem;
}

/* Button styling - elegant with icon */
.stButton>button {
    background: linear-gradient(135deg, #a67c52 0%, #8d6e63 100%);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    padding: 1rem 2.5rem;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(166, 124, 82, 0.3);
    font-size: 1.1rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    position: relative;
    overflow: hidden;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(166, 124, 82, 0.4);
    background: linear-gradient(135deg, #b8946a 0%, #9d7e73 100%);
}

.stButton>button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent 30%,
        rgba(255, 255, 255, 0.1) 50%,
        transparent 70%
    );
    transform: rotate(45deg);
    transition: all 0.5s ease;
}

.stButton>button:hover::after {
    left: 100%;
}

/* Manuscript card - sophisticated design */
.manuscript-card {
    background: linear-gradient(to bottom right, #fffef7, #fcf9f0);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    border-left: 6px solid #a67c52;
    box-shadow: 
        0 8px 30px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(213, 196, 176, 0.3);
}

.manuscript-card:hover {
    transform: translateY(-8px);
    box-shadow: 
        0 15px 40px rgba(93, 64, 55, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.manuscript-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, 
        #a67c52 0%, 
        #d7ccc8 25%, 
        #a67c52 50%, 
        #d7ccc8 75%, 
        #a67c52 100%);
    background-size: 200% 100%;
    animation: shimmer 3s infinite linear;
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Form input styling */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 2px solid #d7ccc8;
    padding: 14px;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease;
    font-family: 'Georgia', serif;
}

.stTextInput>div>div>input:focus {
    border-color: #a67c52;
    box-shadow: 0 0 0 3px rgba(166, 124, 82, 0.1);
    background: white;
}

/* File uploader - elegant drop zone */
.upload-zone {
    border: 3px dashed #a67c52 !important;
    background: linear-gradient(135deg, rgba(166, 124, 82, 0.05), rgba(141, 110, 99, 0.05)) !important;
    border-radius: 20px !important;
    padding: 3rem !important;
    text-align: center;
    transition: all 0.3s ease;
}

.upload-zone:hover {
    background: linear-gradient(135deg, rgba(166, 124, 82, 0.1), rgba(141, 110, 99, 0.1)) !important;
    border-color: #8d6e63 !important;
}

/* Image preview with frame */
.image-frame {
    border: 8px solid #f5f0e6;
    border-radius: 15px;
    padding: 8px;
    background: white;
    box-shadow: 
        0 10px 30px rgba(0, 0, 0, 0.1),
        inset 0 0 0 1px rgba(166, 124, 82, 0.1);
    position: relative;
}

.image-frame::after {
    content: '';
    position: absolute;
    top: -4px;
    left: -4px;
    right: -4px;
    bottom: -4px;
    border: 2px solid rgba(166, 124, 82, 0.1);
    border-radius: 20px;
    pointer-events: none;
}

/* Metadata badges */
.metadata-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #f5efe6, #f0e6d7);
    padding: 8px 18px;
    border-radius: 25px;
    margin-right: 12px;
    margin-bottom: 12px;
    font-size: 0.95rem;
    color: #5d4037;
    border: 1px solid #e0d6cc;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.metadata-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    background: linear-gradient(135deg, #f9f5ec, #f5ecdf);
}

/* Text extraction area */
.extracted-text {
    background: linear-gradient(to bottom, #fffef7, #fcfaf3);
    border: 2px solid #e0d6cc;
    border-radius: 15px;
    padding: 1.5rem;
    font-family: 'Georgia', serif;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #4e342e;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* Search bar */
.search-bar {
    background: white;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 
        0 5px 20px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    border: 2px solid #e0d6cc;
    margin-bottom: 2rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #f9f5f0, #f5f0e6);
    border-radius: 20px;
    border: 2px dashed #d7ccc8;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: #8d6e63;
    font-size: 0.95rem;
    border-top: 1px solid rgba(166, 124, 82, 0.2);
    margin-top: 3rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .main-wrapper {
        padding: 1.5rem;
        margin: 1rem;
    }
    
    .hero-header h1 {
        font-size: 2.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ================= DB =================
ARCHIVE_DIR = "archive_images"
DB = "archive.db"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS scriptures(
id INTEGER PRIMARY KEY,
title TEXT,
author TEXT,
year TEXT,
image TEXT,
text TEXT
)
""")
conn.commit()
conn.close()

# ================= OCR =================
@st.cache_resource
def load():
    return OCR(device="cpu", identifier_lang="auto")

ocr = load()

def extract(path):
    result = ocr.ocr(path)
    words=[]
    for line in result:
        for w in line:
            if isinstance(w,str):
                words.append(w)
    return " ".join(words)

# ================= DB FUNCTIONS =================
def save(t,a,y,i,tx):
    conn=sqlite3.connect(DB)
    c=conn.cursor()
    c.execute("INSERT INTO scriptures VALUES(NULL,?,?,?,?,?)",(t,a,y,i,tx))
    conn.commit()
    conn.close()

def load_all(q=""):
    conn=sqlite3.connect(DB)
    c=conn.cursor()
    if q:
        c.execute("SELECT * FROM scriptures WHERE title LIKE ? OR author LIKE ? OR text LIKE ? ORDER BY id DESC",
                  (f"%{q}%",f"%{q}%",f"%{q}%"))
    else:
        c.execute("SELECT * FROM scriptures ORDER BY id DESC")
    data=c.fetchall()
    conn.close()
    return data
def delete_record(record_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM scriptures WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

# ================= UI =================
st.markdown("<div class='main-wrapper'>", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class='hero-header'>
    <h1>📜 Digitalization of old Scriptures</h1>
    <div class='hero-tagline'>Preserving Ancient Odia Scriptures Through Digital Technology</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✍️ Digitize Scripture", "📚 Scripture Archive"])

# ================= DIGITIZE TAB =================
with tab1:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2>Digitize New Scripture</h2>
        <p style='color: #6d4c41;'>Upload an image of an Odia Scripture to extract and archive its text</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered form layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("<div class='separator'>Scripture Details</div>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                title = st.text_input("📖 Title", "Odia Scripture", 
                                    help="Enter the title of the scripture")
                author = st.text_input("👤 Author", "Unknown", 
                                     help="Author or compiler of the scripture")
            with col_b:
                year = st.text_input("📅 Year", "1455", 
                                   help="Year of creation or transcription")
            
            st.markdown("<div class='separator'>Scripture Image</div>", unsafe_allow_html=True)
            
            # File uploader with custom styling
            file = st.file_uploader("Drag and drop scripture image here", 
                                   type=["png", "jpg", "jpeg"],
                                   help="Supported formats: PNG, JPG, JPEG • Max 200MB",
                                   key="uploader")
            
            if file:
                # Preview in center
                st.markdown("### 📸 Preview")
                img = Image.open(file)
                col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                with col_img2:
                    st.markdown("<div class='image-frame'>", unsafe_allow_html=True)
                    st.image(img, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Extract button - centered and prominent
                st.markdown("<br>", unsafe_allow_html=True)
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    if st.button("✨ Extract & Archive Scripture", 
                               type="primary", 
                               use_container_width=True):
                        
                        with st.spinner("Processing scripture..."):
                            # Save file
                            path = os.path.join(ARCHIVE_DIR, file.name)
                            img.save(path)
                            
                            # Extract text
                            text = extract(path)
                            
                            # Save to database
                            save(title, author, year, path, text)
                        
                        st.success("✅ Scripture successfully digitized and archived!")
                        st.balloons()
                        
                        # Show extracted text in elegant box
                        st.markdown("<div class='separator'>Extracted Text</div>", unsafe_allow_html=True)
                        st.markdown("""
                        <div class='metadata-badge' style='margin-bottom: 1rem;'>
                            <span>📄 OCR Output</span>
                            <span style='color: #a67c52;'>•</span>
                            <span>{:,} characters extracted</span>
                        </div>
                        """.format(len(text)), unsafe_allow_html=True)
                        
                        st.markdown("<div class='extracted-text'>", unsafe_allow_html=True)
                        st.text_area("", text, height=200, label_visibility="collapsed", key="extracted_text")
                        st.markdown("</div>", unsafe_allow_html=True)
            
            else:
                # Empty state for upload zone
                st.markdown("""
                <div class='empty-state'>
                    <div style='font-size: 4rem; color: #d7ccc8; margin-bottom: 1rem;'>📤</div>
                    <h3 style='color: #8d6e63;'>Ready to Digitize</h3>
                    <p style='color: #795548; max-width: 500px; margin: 0 auto 1.5rem auto;'>
                        Upload a high-quality image of an Odia manuscript to begin the digitization process.
                        Our advanced OCR will extract the text for archiving and research.
                    </p>
                </div>
                """, unsafe_allow_html=True)

# ================= ARCHIVE TAB =================
with tab2:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2>📚 Scripture Archive</h2>
        <p style='color: #6d4c41;'>Browse and search through all digitized scriptures</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Elegant search bar
    st.markdown("<div class='search-bar'>", unsafe_allow_html=True)
    search = st.text_input("", 
                          placeholder="🔍 Search scriptures by title, author, or content...",
                          label_visibility="collapsed",
                          key="search")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Load data
    data = load_all(search)
    
    if data:
        # Statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Total Scriptures", len(data))
        with col_stat2:
            unique_authors = len(set([d[2] for d in data if d[2]]))
            st.metric("Unique Authors", unique_authors)
        with col_stat3:
            years = [int(d[3]) for d in data if d[3] and d[3].isdigit()]
            if years:
                st.metric("Oldest Scripture", min(years))
        
        st.markdown("<div class='separator'>Digitized Scriptures</div>", unsafe_allow_html=True)
        
        # Scripture cards
        for idx, d in enumerate(data):
            record_id, t, a, y, i, tx = d
            
            col_del1, col_del2 = st.columns([10,1])
            with col_del2:
                if st.button("🗑️", key=f"del_{record_id}"):
                    delete_record(record_id)
                    st.experimental_rerun()

            st.markdown(f"<div class='scripture-card'>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if os.path.exists(i):
                    st.image(i, use_container_width=True, 
                           caption=f"Scripture #{idx+1}")
                else:
                    st.markdown("""
                    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f0e6, #f0e9dc); 
                         border-radius: 12px; height: 200px; display: flex; align-items: center; justify-content: center;'>
                        <div>
                            <div style='font-size: 3rem; color: #d7ccc8;'>📄</div>
                            <p style='color: #8d6e63; margin-top: 1rem;'>Image Preview</p>
                            <p style='color: #a1887f; font-size: 0.9rem;'>Not available</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Title with decorative underline
                st.markdown(f"""
                <h3 style='color: #3e2723; margin-top: 0; position: relative; padding-bottom: 10px;'>
                    {t}
                    <span style='position: absolute; bottom: 0; left: 0; width: 60px; height: 3px; 
                          background: linear-gradient(90deg, #a67c52, #d7ccc8); border-radius: 2px;'></span>
                </h3>
                """, unsafe_allow_html=True)
                
                # Metadata badges
                col_meta1, col_meta2 = st.columns(2)
                with col_meta1:
                    st.markdown(f"""
                    <div class='metadata-badge'>
                        <span>👤</span>
                        <span>{a if a else 'Unknown Author'}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_meta2:
                    st.markdown(f"""
                    <div class='metadata-badge'>
                        <span>📅</span>
                        <span>{y if y else 'Unknown Year'}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Extracted text preview
                st.markdown("#### Extracted Text")
                if tx:
                    st.markdown("<div class='extracted-text' style='padding: 1rem;'>", unsafe_allow_html=True)
                    st.text_area("", tx, height=150, label_visibility="collapsed", 
                               key=f"text_{idx}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Text statistics
                    col_text1, col_text2 = st.columns(2)
                    with col_text1:
                        st.caption(f"📝 {len(tx.split())} words")
                    with col_text2:
                        st.caption(f"🔤 {len(tx)} characters")
                else:
                    st.info("No text extracted from this scripture")
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Empty archive state
        st.markdown("""
        <div class='empty-state'>
            <div style='font-size: 4rem; color: #d7ccc8; margin-bottom: 1rem;'>📭</div>
            <h3 style='color: #8d6e63;'>Archive is Empty</h3>
            <p style='color: #795548; max-width: 500px; margin: 0 auto 1.5rem auto;'>
                No manuscripts have been digitized yet. Start by uploading your first manuscript 
                in the "Digitize Manuscript" tab.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    <p>📜 <strong>Digital Scripture OCR Archive</strong> | Preserving Cultural Heritage | Odia Scripture Digitization</p>
</div>
""", unsafe_allow_html=True)