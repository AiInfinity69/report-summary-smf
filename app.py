import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายอัตโนมัติ", page_icon="📊", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #ff5722; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 ระบบสรุปยอดขายและค่าธรรมเนียมอัตโนมัติ</p>', unsafe_allow_html=True)
st.write("อัปโหลดไฟล์รายงานจากอีคอมเมิร์ซ ระบบจะตรวจสอบและสรุปยอดให้ทันที พร้อมแจ้งเตือนหากมีข้อผิดพลาด")

uploaded_file = st.file_uploader(
    "📂 อัปโหลดไฟล์รายงาน (Excel หรือ CSV)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    # ตรวจสอบนามสกุลและพยายามอ่านไฟล์พร้อมดักจับข้อผิดพลาดทุกขั้นตอน
    file_name = uploaded_file.name
    st.info(f"กำลังประมวลผลไฟล์: {file_name} (ขนาด: {uploaded_file.size / 1024:.2f} KB)")

    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    else:
      # ใช้ openpyxl อ่านไฟล์ excel พร้อมระบุเตือนถ้าอ่านไม่ได้
      try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
      except Exception as ex:
        st.error(f"❌ อ่านไฟล์ Excel ไม่สำเร็จ: อาจเป็นเพราะรูปแบบไฟล์เสียหาย มีการเข้ารหัส หรือไม่ใช่ไฟล์ Excel แท้ ({ex})")
        st.stop()

    st.success("✅ อัปโหลดและอ่านข้อมูลสำเร็จ!")
    
    with st.expander("🔍 ดูตัวอย่างข้อมูลดิบในไฟล์"):
      st.dataframe(df.head(5))

    # ค้นหาคอลัมน์ตัวเลขเพื่อหายอดรวม
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_cols:
      st.write("---")
      st.subheader("📌 ผลการสรุปยอดเบื้องต้น")
      
      col1, col2 = st.columns(2)
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
    else:
      st.warning("⚠️ ไฟล์นี้อัปโหลดสำเร็จ แต่ไม่พบคอลัมน์ที่เป็นตัวเลขสำหรับนำมาคำนวณยอดรวม กรุณาตรวจสอบหัวตารางในไฟล์ของคุณ")

  except Exception as e:
    # แจ้งเตือนข้อผิดพลาดแบบละเอียดยิบให้ผู้ใช้รู้ทันที
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
    st.warning("คำแนะนำ: ลองตรวจสอบว่าไฟล์ Excel เปิดค้างไว้ หรือมีชีทที่ว่างเปล่า/รูปแบบตารางผิดปกติหรือไม่")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานของคุณเพื่อเริ่มคำนวณ")
    
