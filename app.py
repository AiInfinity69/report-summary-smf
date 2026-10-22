import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายอีคอมเมิร์ซทุกร้าน", page_icon="📈", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1f77b4; }
    .sub-text { color: #555; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📈 ระบบสรุปยอดขายและค่าธรรมเนียมอัตโนมัติ (ทุกร้าน)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">รองรับรายงานจาก Lazada, Shopee, TikTok และข้อมูลต้นทุนรายร้านแบบครบถ้วน</p>', unsafe_allow_html=True)

# เลือกหมวดหมู่ร้านหรือประเภทไฟล์
store_option = st.selectbox(
    "🏪 เลือกชื่อร้านหรือประเภทรายงานที่ต้องการประมวลผล:",
    [
        "Tech-Mate",
        "Tech-Box",
        "Smartfixed",
        "Smart Box",
        "S.Fixed",
        "4C",
        "ไฟล์ต้นทุนรวม (ต้นทุน พค.69)",
    ],
)

uploaded_file = st.file_uploader(
    f"📂 อัปโหลดไฟล์ Excel สำหรับ: {store_option}", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    file_name = uploaded_file.name
    st.info(f"กำลังโหลดไฟล์: {file_name} (ขนาด: {uploaded_file.size / 1024:.2f} KB)")

    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
      st.success("✅ อ่านไฟล์ CSV สำเร็จ")
      st.dataframe(df.head(5))
    else:
      # อ่านไฟล์ Excel ที่มีหลายชีท
      xls = pd.ExcelFile(uploaded_file)
      sheet_names = xls.sheet_names
      st.success(f"✅ พบชีทข้อมูลทั้งหมดในไฟล์: {', '.join(sheet_names)}")

      # ให้ผู้ใช้เลือกชีทที่ต้องการดูหรือสรุป
      selected_sheet = st.selectbox("📑 เลือกชีท (Sheet) ที่ต้องการตรวจสอบ:", sheet_names)
      
      df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
      
      st.write(f"--- 📊 แสดงข้อมูลจากชีท: **{selected_sheet}** ---")
      st.dataframe(df.head(10))

      # วิเคราะห์ข้อมูลเบื้องต้นตามชีท
      numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
      if numeric_cols:
        st.subheader("📌 สรุปตัวเลขเบื้องต้นในชีทนี้")
        col1, col2 = st.columns(2)
        
        # เลือกคอลัมน์แรกที่เป็นตัวเลขหรือคอลัมน์ Amount ถ้ามี
        target_col = 'Amount' if 'Amount' in df.columns else numeric_cols[0]
        total_sum = df[target_col].sum() if target_col in df.columns else 0

        with col1:
          st.metric(label=f"💰 ผลรวม ({target_col})", value=f"{total_sum:,.2f} บาท")
        with col2:
          st.metric(label="📦 จำนวนแถวข้อมูล", value=f"{len(df):,} แถว")
      else:
        st.warning("⚠️ ชีทนี้ไม่พบคอลัมน์ที่เป็นตัวเลขสำหรับคำนวณ")

  except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
    st.warning("คำแนะนำ: กรุณาตรวจสอบว่าไฟล์ Excel ไม่ได้ถูกเข้ารหัส หรือรูปแบบตารางเสียหาย")
else:
  st.info(f"📌 กรุณาอัปโหลดไฟล์ Excel ของร้าน **{store_option}** เพื่อเริ่มวิเคราะห์ข้อมูล")
    
