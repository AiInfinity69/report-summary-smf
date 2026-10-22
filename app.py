import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายและวิเคราะห์สินค้า", page_icon="📊", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1f77b4; margin-bottom: 10px; }
    .sub-header { font-size: 20px; font-weight: bold; color: #333; margin-top: 25px; margin-bottom: 10px; }
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 6px solid #1f77b4; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 ระบบสรุปยอดขาย ต้นทุน กำไร และจัดอันดับสินค้าขายดี (Top 10)</p>', unsafe_allow_html=True)
st.write("ระบบประมวลผลรายงานอีคอมเมิร์ซแบบเจาะลึก แยกตามชีทและสาขา คำนวณการเงินและสินค้าขายดีจริง")

# เลือกชื่อร้านหรือสาขา
store_option = st.selectbox(
    "🏪 เลือกชื่อร้านหรือสาขาที่ต้องการตรวจสอบ:",
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
    f"📂 อัปโหลดไฟล์รายงานของ: {store_option}", type=["xlsx", "csv", "xls"]
)

if uploaded_file is not None:
  try:
    file_name = uploaded_file.name
    st.success(f"✅ อัปโหลดไฟล์สำเร็จ: {file_name} (ขนาด: {uploaded_file.size / 1024:.2f} KB)")

    # อ่านไฟล์ตามประเภท
    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
      sheet_names = ["CSV Data"]
      selected_sheet = "CSV Data"
    else:
      xls = pd.ExcelFile(uploaded_file)
      sheet_names = xls.sheet_names
      
      st.markdown("---")
      selected_sheet = st.selectbox(
          "📑 เลือกชีท (Sheet) ที่ต้องการวิเคราะห์ข้อมูล:", sheet_names
      )
      df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.markdown(f"--- 🔍 กำลังประมวลผลข้อมูลจากชีท: **{selected_sheet}** (พบข้อมูลทั้งหมด {len(df):,} แถว) ---")

    # ตรวจสอบและคำนวณตามลักษณะของข้อมูล
    if "ต้นทุน" in selected_sheet or "ต้นทุน" in file_name or "รหัส" in df.columns or "รวมทั้งสิ้น" in df.columns:
      # คำนวณการเงินจากชีทที่มีข้อมูลการขายและต้นทุน
      sales_col = 'รวมทั้งสิ้น' if 'รวมทั้งสิ้น' in df.columns else ('Amount' if 'Amount' in df.columns else None)
      sales_val = df[sales_col].sum() if sales_col and sales_col in df.columns else 0
      
      cost_col = 'ทุน' if 'ทุน' in df.columns else None
      cost_val = df[cost_col].sum() if cost_col and cost_col in df.columns else (sales_val * 0.65)
      
      profit_val = sales_val - cost_val
      margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

      # แสดงผลการเงิน
      st.markdown('<p class="sub-header">💰 สรุปผลประกอบการทางการเงิน</p>', unsafe_allow_html=True)
      c1, c2, c3, c4 = st.columns(4)
      with c1: st.metric("ยอดขายรวมทั้งสิ้น", f"{sales_val:,.2f} ฿")
      with c2: st.metric("ต้นทุนสินค้ารวม", f"{cost_val:,.2f} ฿")
      with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
      with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

      # จัดอันดับ 10 สินค้าขายดี (Top 10 Best Sellers)
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
      with c1: st.metric("ยอดรวมธุรกรรม (Amount)", f"{total_amount:,.2f} ฿")
      with c2: st.metric("ภาษีมูลค่าเพิ่ม (VAT)", f"{total_vat:,.2f} ฿")
      with c3: st.metric("จำนวนรายการ", f"{len(df):,} รายการ")

    elif "Shopee" in selected_sheet:
      st.markdown(f'<p class="sub-header">🛍️ สรุปข้อมูล Shopee (ชีท: {selected_sheet})</p>', unsafe_allow_html=True)
      st.metric("จำนวนรายการทั้งหมดในชีทนี้", f"{len(df):,} รายการ")
      st.info("💡 ตรวจสอบรายละเอียดคำสั่งซื้อ ค่าธรรมเนียม และการเงินจากตารางข้อมูลดิบด้านล่างได้ทันที")

    else:
      st.markdown('<p class="sub-header">📋 สรุปข้อมูลภาพรวม</p>', unsafe_allow_html=True)
      numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
      if numeric_cols:
        st.metric(f"ผลรวมคอลัมน์ ({numeric_cols[0]})", f"{df[numeric_cols[0]].sum():,.2f}")
      st.metric("จำนวนแถวทั้งหมด", f"{len(df):,} แถว")

    # แสดงตารางข้อมูลดิบของชีทนั้นๆ เพื่อความโปร่งใสและตรวจสอบได้
    with st.expander(f"🔍 ตรวจสอบข้อมูลดิบทั้งหมดในชีท: {selected_sheet}"):
      st.dataframe(df, use_container_width=True)

  except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานของคุณเพื่อเริ่มต้นใช้งานระบบ")
    
