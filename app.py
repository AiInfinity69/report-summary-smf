import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tech-Mate Order Summary", page_icon="📊", layout="wide"
)

st.title("📊 ระบบสรุปยอดขายอัตโนมัติ - Tech-Mate")
st.write(
    "อัปโหลดไฟล์รายงานจาก Lazada หรือ Shopee เพื่อสรุปยอดขาย ค่าธรรมเนียม และรายรับสุทธิทันที"
)

# เลือกแพลตฟอร์ม
platform = st.selectbox(
    "เลือกแพลตฟอร์มของไฟล์รายงาน:", ("Shopee (รายงานคำสั่งซื้อ)", "Lazada")
)

uploaded_file = st.file_uploader(
    "อัปโหลดไฟล์ Excel (.xlsx หรือ .csv)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    if "Shopee" in platform:
      df = pd.read_excel(uploaded_file)
      st.success("อัปโหลดไฟล์ Shopee สำเร็จ!")
      st.write("### ตัวอย่างข้อมูลดิบ (บางส่วน)")
      st.dataframe(df.head(5))

      if "จำนวนเงินทั้งหมด" in df.columns and "ค่าคอมมิชชั่น" in df.columns:
        total_sales = df["จำนวนเงินทั้งหมด"].sum()
        total_commission = df["ค่าคอมมิชชั่น"].sum()
        st.metric(
            label="💰 ยอดขายรวมทั้งหมด (Gross Sales)",
            value=f"{total_sales:,.2f} บาท",
        )
        st.metric(
            label="📉 ค่าคอมมิชชั่น/ค่าธรรมเนียมรวม",
            value=f"{total_commission:,.2f} บาท",
        )
      else:
        st.info(
            "ไฟล์ถูกโหลดเข้าระบบเรียบร้อยแล้ว พร้อมคำนวณตามโครงสร้างข้อมูล"
        )

    elif "Lazada" in platform:
      df = pd.read_excel(uploaded_file)
      st.success("อัปโหลดไฟล์ Lazada สำเร็จ!")
      st.write("### ตัวอย่างข้อมูลดิบ (บางส่วน)")
      st.dataframe(df.head(5))

      if "Amount" in df.columns:
        total_amount = df["Amount"].sum()
        st.metric(
            label="💰 ยอดรวมธุรกรรม Lazada", value=f"{total_amount:,.2f} บาท"
        )

  except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานเพื่อเริ่มประมวลผล")
