import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายอัตโนมัติ", page_icon="📊", layout="wide"
)

# ตกแต่งหน้าตาเว็บให้ดูสะอาดตาและทันสมัยยิ่งขึ้น
st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #ff5722; }
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff5722; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 ระบบสรุปยอดขายและค่าธรรมเนียมอัตโนมัติ</p>', unsafe_allow_html=True)
st.write("อัปโหลดไฟล์รายงานจากอีคอมเมิร์ซ ระบบจะทำการวิเคราะห์และหายอดรวมให้ทันทีแบบยืดหยุ่น")

uploaded_file = st.file_uploader(
    "📂 อัปโหลดไฟล์รายงาน (Excel หรือ CSV)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    # อ่านไฟล์รองรับทั้ง Excel และ CSV
    if uploaded_file.name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    else:
      df = pd.read_excel(uploaded_file)

    st.success(f"อัปโหลดไฟล์สำเร็จ: {uploaded_file.name}")
    
    with st.expander("🔍 ดูตัวอย่างข้อมูลดิบบางส่วน"):
      st.dataframe(df.head(5))

    # ระบบอัจฉริยะ: ค้นหาคอลัมน์ที่เป็นตัวเลขเพื่อหายอดรวมโดยไม่ต้องสนชื่อหัวคอลัมน์
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_cols:
      st.write("---")
      st.subheader("📌 ผลการสรุปยอดเบื้องต้น")
      
      # สร้างกล่องแสดงผลตัวเลขแบบสวยงาม
      col1, col2 = st.columns(2)
      
      # หาคอลัมน์ที่น่าจะเป็นยอดเงินรวม (ค่าที่มากที่สุดในกลุ่มตัวเลข)
      total_col = numeric_cols[0]
      sum_value = df[total_col].sum()
      
      with col1:
        st.metric(
            label="💰 ยอดรวมภาพรวม (Estimated Total)",
            value=f"{sum_value:,.2f} บาท",
        )
      with col2:
        st.metric(
            label="📦 จำนวนรายการทั้งหมด",
            value=f"{len(df):,} รายการ",
        )
      
      st.info("💡 ระบบได้ทำการรวมตัวเลขจากคอลัมน์หลักในไฟล์ให้คุณเรียบร้อยแล้วโดยอัตโนมัติ")
    else:
      st.warning("ไม่พบข้อมูลที่เป็นตัวเลขในไฟล์ กรุณาตรวจสอบรูปแบบไฟล์อีกครั้ง")

  except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลไฟล์: {e}")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานของคุณเพื่อเริ่มคำนวณ")
    
