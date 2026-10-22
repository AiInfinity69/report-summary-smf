import pandas as pd
import streamlit as st
import datetime

st.set_page_config(
    page_title="ระบบสรุปยอดขายและสินค้าขายดี", page_icon="🏆", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1f77b4; }
    .sub-header { font-size: 18px; font-weight: bold; color: #333; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏆 ระบบสรุปยอดขาย ต้นทุน กำไร และจัดอันดับสินค้าขายดี (Top 10)</p>', unsafe_allow_html=True)
st.write("อัปโหลดไฟล์รายงานเพื่อคำนวณรายได้ ต้นทุน กำไร และจัดอันดับ 10 อันดับสินค้าขายดีอัตโนมัติทันที")

# เลือกชื่อร้านหรือประเภทรายงาน
store_option = st.selectbox(
    "🏪 เลือกชื่อร้านหรือสาขาที่ต้องการประมวลผล:",
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
    f"📂 อัปโหลดไฟล์รายงานสำหรับ: {store_option}", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    file_name = uploaded_file.name
    st.info(f"กำลังประมวลผลไฟล์: {file_name}")

    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
      sheet_name_selected = "CSV"
    else:
      xls = pd.ExcelFile(uploaded_file)
      sheet_names = xls.sheet_names
      sheet_name_selected = st.selectbox("📑 เลือกชีท (Sheet) ในไฟล์:", sheet_names)
      df = pd.read_excel(uploaded_file, sheet_name=sheet_name_selected)

    st.success(f"✅ อ่านข้อมูลสำเร็จจากชีท: {sheet_name_selected}")

    # คำนวณตัวเลขการเงินหลัก
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    sales_val = 0
    cost_val = 0
    
    if 'รวมทั้งสิ้น' in df.columns:
        sales_val = df['รวมทั้งสิ้น'].sum()
    elif 'Amount' in df.columns:
        sales_val = df['Amount'].sum()
    elif numeric_cols:
        sales_val = df[numeric_cols[0]].sum()
        
    if 'ทุน' in df.columns:
        cost_val = df['ทุน'].sum()
    else:
        cost_val = sales_val * 0.65  # ค่าสำรองถ้าไม่มีคอลัมน์ทุน

    profit_val = sales_val - cost_val
    margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0
    total_items = len(df)

    # แสดงผลการคำนวณทางการเงิน
    st.write("---")
    st.markdown('<p class="sub-header">📊 สรุปผลประกอบการทางการเงิน</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="💰 ยอดขายรวม", value=f"{sales_val:,.2f} ฿")
    with col2:
        st.metric(label="📦 ต้นทุนรวม", value=f"{cost_val:,.2f} ฿")
    with col3:
        st.metric(label="📈 กำไรขั้นต้น", value=f"{profit_val:,.2f} ฿")
    with col4:
        st.metric(label="📊 อัตรากำไร", value=f"{margin_val:.2f}%")

    # ส่วนจัดอันดับสินค้าขายดี 10 อันดับแรก (Top 10 Best Sellers)
    if 'รายละเอียด' in df.columns and 'รวมทั้งสิ้น' in df.columns:
        st.write("---")
        st.markdown('<p class="sub-header">🏆 10 อันดับสินค้าขายดีที่สุด (เรียงตามยอดขาย)</p>', unsafe_allow_html=True)
        
        group_cols = ['รายละเอียด', 'รหัส'] if 'รหัส' in df.columns else ['รายละเอียด']
        agg_dict = {'รวมทั้งสิ้น': 'sum'}
        if 'จำนวน' in df.columns:
            agg_dict['จำนวน'] = 'sum'
        if 'ทุน' in df.columns:
            agg_dict['ทุน'] = 'sum'
            
        top10_df = df.groupby(group_cols).agg(agg_dict).reset_index()
        
        if 'ทุน' in top10_df.columns:
            top10_df['กำไรขั้นต้น'] = top10_df['รวมทั้งสิ้น'] - top10_df['ทุน']
            
        top10_df = top10_df.sort_values(by='รวมทั้งสิ้น', ascending=False).head(10)
        top10_df.index = range(1, len(top10_df) + 1)
        
        st.dataframe(top10_df, use_container_width=True)

    with st.expander("🔍 ดูตัวอย่างข้อมูลดิบทั้งหมดในชีทนี้"):
        st.dataframe(df.head(20))

  except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
else:
  st.info(f"📌 กรุณาอัปโหลดไฟล์ของร้าน **{store_option}** เพื่อเริ่มคำนวณและจัดอันดับสินค้า")
    
