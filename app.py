import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ระบบสรุปยอดขายและรายงานผลรวม SF", page_icon="📊", layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #1f77b4; margin-bottom: 5px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #333; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 ระบบสรุปยอดขายและรายงานผลรวม SF (Smart Fixed)</p>', unsafe_allow_html=True)
st.write("ระบบวิเคราะห์รายงานอีคอมเมิร์ซและจัดการข้อมูลหลายแพลตฟอร์ม (Lazada, Shopee, TikTok) พร้อมคำนวณต้นทุน กำไร และค่าคอมมิชชั่นพนักงาน")

uploaded_file = st.file_uploader(
    "📂 อัปโหลดไฟล์รายงาน (Excel .xlsx หรือ .csv)", type=["xlsx", "csv", "xls"]
)

if uploaded_file is not None:
  try:
    file_name = uploaded_file.name
    st.success(f"✅ อัปโหลดไฟล์สำเร็จ: {file_name}")

    file_lower = file_name.lower()
    detected_store = "Smart Fixed (SF)"
    if "tech-mate" in file_lower: detected_store = "Tech-Mate"
    elif "tech-box" in file_lower: detected_store = "Tech-Box"
    elif "smartfixed" in file_lower: detected_store = "Smartfixed"
    elif "smart box" in file_lower: detected_store = "Smart Box"
    elif "s.fixed" in file_lower or "s-fixed" in file_lower: detected_store = "S.Fixed"
    elif "4c" in file_lower: detected_store = "4C"
    elif "ต้นทุน" in file_lower: detected_store = "ไฟล์ต้นทุนรวม SF"

    st.info(f"🏪 ตรวจพบข้อมูลของร้าน/สาขา: **{detected_store}**")

    if file_name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
      selected_sheet = "CSV Data"
    else:
      xls = pd.ExcelFile(uploaded_file)
      sheet_names = xls.sheet_names
      selected_sheet = st.selectbox("📑 เลือกชีท (Sheet) รายงานที่ต้องการตรวจสอบ:", sheet_names)
      df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.markdown(f"--- 🔍 กำลังวิเคราะห์ชีท: **{selected_sheet}** (พบข้อมูล {len(df):,} แถว) ---")

    sheet_lower = selected_sheet.lower()
    sales_val = 0
    cost_val = 0
    profit_val = 0
    margin_val = 0

    # --- 1. แยกตามประเภทชีทและแพลตฟอร์ม ---
    if "lazada" in sheet_lower:
        sales_val = df['Amount'].sum() if 'Amount' in df.columns else 0
        cost_val = sales_val * 0.65
        profit_val = sales_val - cost_val
        margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

        st.markdown('<p class="sub-header">📦 สรุปผลประกอบการ Lazada</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("ยอดรวมธุรกรรม (Amount)", f"{sales_val:,.2f} ฿")
        with c2: st.metric("ต้นทุนประเมิน (65%)", f"{cost_val:,.2f} ฿")
        with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
        with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

    elif "shopee" in sheet_lower:
        potential_sales = 0
        for col in df.columns:
            col_str = str(col).lower()
            if any(k in col_str for k in ['price', 'amount', 'total', 'ยอด', 'ราคา', 'รวม', 'จำนวนเงิน']):
                if pd.to_numeric(df[col], errors='coerce').sum() > 0:
                    potential_sales = pd.to_numeric(df[col], errors='coerce').sum()
                    break
        sales_val = potential_sales
        cost_val = sales_val * 0.65
        profit_val = sales_val - cost_val
        margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

        st.markdown(f'<p class="sub-header">🛍️ สรุปผลประกอบการ Shopee ({selected_sheet})</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("ยอดขายรวม Shopee", f"{sales_val:,.2f} ฿")
        with c2: st.metric("ต้นทุนประเมิน (65%)", f"{cost_val:,.2f} ฿")
        with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
        with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

    elif "tiktok" in sheet_lower:
        potential_sales = 0
        for col in df.columns:
            col_str = str(col).lower()
            if any(k in col_str for k in ['amount', 'price', 'total', 'ยอด', 'ราคา', 'รวม']):
                if pd.to_numeric(df[col], errors='coerce').sum() > 0:
                    potential_sales = pd.to_numeric(df[col], errors='coerce').sum()
                    break
        sales_val = potential_sales
        cost_val = sales_val * 0.65
        profit_val = sales_val - cost_val
        margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

        st.markdown(f'<p class="sub-header">🎵 สรุปผลประกอบการ TikTok ({selected_sheet})</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("ยอดขายรวม TikTok", f"{sales_val:,.2f} ฿")
        with c2: st.metric("ต้นทุนประเมิน (65%)", f"{cost_val:,.2f} ฿")
        with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
        with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

    else:
        # ชีทต้นทุนหรือชีทสรุปภาพรวม
        sales_col = 'รวมทั้งสิ้น' if 'รวมทั้งสิ้น' in df.columns else (df.select_dtypes(include=["number"]).columns[0] if len(df.select_dtypes(include=["number"]).columns) > 0 else None)
        sales_val = pd.to_numeric(df[sales_col], errors='coerce').sum() if sales_col and sales_col in df.columns else 0
        
        cost_col = 'ทุน' if 'ทุน' in df.columns else None
        cost_val = pd.to_numeric(df[cost_col], errors='coerce').sum() if cost_col and cost_col in df.columns else (sales_val * 0.65)
        
        profit_val = sales_val - cost_val
        margin_val = (profit_val / sales_val * 100) if sales_val > 0 else 0

        st.markdown('<p class="sub-header">💰 สรุปผลประกอบการภาพรวมและต้นทุน (SF)</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("ยอดขายรวมทั้งสิ้น", f"{sales_val:,.2f} ฿")
        with c2: st.metric("ต้นทุนสินค้ารวม", f"{cost_val:,.2f} ฿")
        with c3: st.metric("กำไรขั้นต้น", f"{profit_val:,.2f} ฿")
        with c4: st.metric("อัตรากำไร", f"{margin_val:.2f}%")

        # --- 2. สรุปค่าคอมมิชชั่นและผลงานพนักงานแยกตามรหัสและชื่อ ---
        staff_col = None
        for col in df.columns:
            if any(k in str(col).lower() for k in ['พนักงาน', 'ผู้ขาย', 'sales', 'seller', 'staff']):
                staff_col = col
                break

        if staff_col and sales_col:
            st.markdown('<p class="sub-header">👥 สรุปยอดขาย กำไร และค่าคอมมิชชั่นพนักงาน (แยกตามรหัส/ชื่อ)</p>', unsafe_allow_html=True)
            
            group_cols = [staff_col]
            if 'รหัส' in df.columns: group_cols = ['รหัส', staff_col]
            elif 'ID' in df.columns: group_cols = ['ID', staff_col]

            agg_dict = {sales_col: 'sum'}
            if 'ทุน' in df.columns: agg_dict['ทุน'] = 'sum'
            
            staff_df = df.groupby(group_cols).agg(agg_dict).reset_index()
            staff_df = staff_df.rename(columns={sales_col: 'ยอดขายรวม', 'ทุน': 'ทุนรวม'})
            
            if 'ทุนรวม' in staff_df.columns:
                staff_df['กำไรสุทธิ'] = staff_df['ยอดขายรวม'] - staff_df['ทุนรวม']
            else:
                staff_df['กำไรสุทธิ'] = staff_df['ยอดขายรวม'] * 0.35
            
            staff_df['ค่าคอมมิชชั่น (5% ของกำไร)'] = staff_df['กำไรสุทธิ'] * 0.05
            staff_df = staff_df.sort_values(by='ยอดขายรวม', ascending=False)
            staff_df.index = range(1, len(staff_df) + 1)
            
            st.dataframe(staff_df, use_container_width=True)

        # --- 3. จัดอันดับ 10 สินค้า/อะไหล่ขายดีที่สุด ---
        desc_col = None
        for col in df.columns:
            if any(k in str(col).lower() for k in ['รายละเอียด', 'item', 'product', 'sku', 'ชื่อ', 'parts', 'อะไหล่']):
                desc_col = col
                break

        if desc_col and sales_col:
            st.markdown('<p class="sub-header">🏆 10 อันดับสินค้า / อะไหล่ขายดีที่สุด (Top 10 Best Sellers)</p>', unsafe_allow_html=True)
            top10_group = [desc_col]
            if 'รหัส' in df.columns and desc_col != 'รหัส':
                top10_group = ['รหัส', desc_col]
            
            top10_agg = {sales_col: 'sum'}
            if 'จำนวน' in df.columns: top10_agg['จำนวน'] = 'sum'
            elif 'Quantity' in df.columns: top10_agg['Quantity'] = 'sum'
            if 'ทุน' in df.columns: top10_agg['ทุน'] = 'sum'

            top10 = df.groupby(top10_group).agg(top10_agg).reset_index()
            top10 = top10.rename(columns={sales_col: 'ยอดขายรวม'})
            if 'ทุน' in top10.columns:
                top10['กำไรขั้นต้น'] = top10['ยอดขายรวม'] - top10['ทุน']
            
            top10 = top10.sort_values(by='ยอดขายรวม', ascending=False).head(10)
            top10.index = range(1, len(top10) + 1)
            st.dataframe(top10, use_container_width=True)

    # แสดงตารางข้อมูลดิบ
    with st.expander(f"🔍 ตรวจสอบข้อมูลดิบทั้งหมดในชีท: {selected_sheet}"):
      st.dataframe(df.head(100), use_container_width=True)

  except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
else:
  st.info("📌 กรุณาอัปโหลดไฟล์รายงานของคุณเพื่อเริ่มใช้งานระบบ")
      
