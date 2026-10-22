import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายอัตโนมัติ", page_icon="📊", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #1f77b4; margin-bottom: 5px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #333; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 ระบบสรุปยอดขาย ต้นทุน กำไร และสินค้าขายดี (Auto Detect)</p>', unsafe_allow_html=True)
st.write("อัปโหลดไฟล์รายงานอีคอมเมิร์ซ ระบบจะตรวจสอบชื่อร้าน ชีทข้อมูล และคำนวณผลการเงินให้อัตโนมัติทันที")

# ช่องอัปโหลดไฟล์แบบเปิดกว้าง รองรับทุกไฟล์
uploaded_file = st.file_uploader(
    "📂 ลากไฟล์รายงาน (.xlsx หรือ .csv) มาวางที่นี่", type=["xlsx", "csv", "xls"]
)

if uploaded_file is not None:
  try:
    file_name = uploaded_file.name
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.success(f"✅ อัปโหลดสำเร็จ: {file_name} ({file_size_mb:.2f} MB)")

    # ตรวจสอบชื่อร้านจากชื่อไฟล์อัตโนมัติแบบฉลาดๆ
    detected_store = "ไม่ระบุสาขา"
    file_lower = file_name.lower()
    if "tech-mate" in file_lower or "tech mate" in file_lower:
        detected_store = "Tech-Mate"
    elif "tech-box" in file_lower or "tech box" in file_lower:
        detected_store = "Tech-Box"
    elif "smartfixed" in file_lower:
        detected_store = "Smartfixed"
    elif "smart box" in file_lower:
        detected_store = "Smart Box"
    elif "s.fixed" in file_lower or "s-fixed" in file_lower:
        detected_store = "S.Fixed"
    elif "4c" in file_lower:
        detected_store = "4C"
    elif "ต้นทุน" in file_lower:
        detected_store = "ไฟล์ต้นทุนรวม"

    st.info(f"🏪 ระบบตรวจสอบพบว่าเป็นข้อมูลของร้าน/ประเภท: **{detected_store}**")

    # อ่านไฟล์และเลือกชีท
    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
      selected_sheet = "CSV Data"
    else:
      xls = pd.ExcelFile(uploaded_file)
      sheet_names = xls.sheet_names
      
      # ให้เลือกชีทเพราะไฟล์ Excel มีหลายชีท
      selected_sheet = st.selectbox(
          "📑 เลือกชีท (Sheet) ที่ต้องการดูรายงาน:", sheet_names
      )
      df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.write(f"--- 🔍 กำลังประมวลผลชีท: **{selected_sheet}** (พบข้อมูล {len(df):,} แถว) ---")

    # คำนวณตัวเลขการเงิน (ยอดขาย, ต้นทุน, กำไร)
    sales_col = 'รวมทั้งสิ้น' if 'รวมทั้งสิ้น' in df.columns else ('Amount' if 'Amount' in df.columns else None)
    sales_val = df[sales_col].sum() if sales_col and sales_col in df.columns else 0
    
    cost_col = 'ทุน' if 'ทุน' in df.columns else None
    cost_val = df[cost_col].sum() if cost_col and cost_col in df.columns else (sales_val * 0.65)
    
    profit_val = sales_val - cost_val
    margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

    # แสดงผลตัวเลขการเงิน
    st.markdown('<p class="sub-header">💰 สรุปผลประกอบการทางการเงิน</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("ยอดขายรวมทั้งสิ้น", f"{sales_val:,.2f} ฿")
    with c2: st.metric("ต้นทุนสินค้ารวม", f"{cost_val:,.2f} ฿")
    with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
    with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

    # จัดอันดับสินค้าขายดี Top 10
    if 'รายละเอียด' in df.columns:
      st.markdown('<p class="sub-header">🏆 10 อันดับสินค้าขายดีที่สุด (เรียงตามยอดขาย)</p>', unsafe_allow_html=True)
      val_c = sales_col if sales_col else df.select_dtypes(include=["number"]).columns[0]
      group_cols = ['รายละเอียด', 'รหัส'] if 'รหัส' in df.columns else ['รายละเอียด']
      
      agg_d = {val_c: 'sum'}
      if 'จำนวน' in df.columns: agg_d['จำนวน'] = 'sum'
      if 'ทุน' in df.columns: agg_d['ทุน'] = 'sum'
      
      top10 = df.groupby(group_cols).agg(agg_d).reset_index()
      top10 = top10.rename(columns={val_c: 'ยอดขายรวม'})
      if 'ทุน' in top10.columns:
        top10['กำไรขั้นต้น'] = top10['ยอดขายรวม'] - top10['ทุน']
      top10 = top10.sort_values(by='ยอดขายรวม', ascending=False).head(10)
      top10.index = range(1, len(top10) + 1)
      
      st.dataframe(top10, use_container_width=True)

    elif "Lazada" in selected_sheet or "LAZADA" in selected_sheet:
      total_amount = df['Amount'].sum() if 'Amount' in df.columns else 0
      total_vat = df['VAT in Amount'].sum() if 'VAT in Amount' in df.columns else 0
      st.markdown('<p class="sub-header">📦 สรุปรายงาน Lazada</p>', unsafe_allow_html=True)
      c1, c2, c3 = st.columns(3)
      with c1: st.metric("ยอดรวมธุรกรรม", f"{total_amount:,.2f} ฿")
      with c2: st.metric("ภาษีมูลค่าเพิ่ม (VAT)", f"{total_vat:,.2f} ฿")
      with c3: st.metric("จำนวนรายการ", f"{len(df):,} รายการ")

    # ตารางดูข้อมูลดิบ
    with st.expander(f"🔍 ตรวจสอบข้อมูลดิบในชีท: {selected_sheet}"):
      st.dataframe(df, use_container_width=True)

  except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานของคุณเพื่อเริ่มใช้งานระบบได้ทันที")
    
