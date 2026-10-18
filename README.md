# appquanlytaichinhcanhann

import streamlit as st
import pandas as pd
from datetime import date

# =========================
# 1. CẤU HÌNH ỨNG DỤNG
# =========================
st.set_page_config(
    page_title="MoneyMate - Quản lý tài chính cá nhân",
    page_icon="💰",
    layout="wide"
)

st.title("💰 MoneyMate")
st.subheader("Trợ lý quản lý tài chính cá nhân")
st.write(
    "Lập ngân sách, kiểm soát chi tiêu và xây dựng "
    "kế hoạch tiết kiệm phù hợp với bạn."
)

st.info(
    "Nhập thông tin tài chính ở thanh bên trái. "
    "Ứng dụng sẽ phân tích và đề xuất kế hoạch cho bạn."
)

# =========================
# 2. NHẬP THÔNG TIN CÁ NHÂN
# =========================
st.sidebar.header("👤 Thông tin cá nhân")

with st.sidebar.form("finance_form"):
    age = st.number_input(
        "Tuổi",
        min_value=16,
        max_value=100,
        value=20,
        step=1
    )

    gender = st.selectbox(
        "Giới tính",
        ["Không muốn trả lời", "Nữ", "Nam", "Khác"]
    )

    occupation = st.selectbox(
        "Nghề nghiệp",
        [
            "Sinh viên",
            "Nhân viên văn phòng",
            "Kinh doanh tự do",
            "Công chức/viên chức",
            "Khác"
        ]
    )

    marital_status = st.selectbox(
        "Tình trạng hôn nhân",
        ["Độc thân", "Đã kết hôn", "Khác"]
    )

    dependents = st.number_input(
        "Số người phụ thuộc tài chính",
        min_value=0,
        max_value=20,
        value=0,
        step=1
    )

    housing = st.selectbox(
        "Tình trạng nhà ở",
        [
            "Sống cùng gia đình",
            "Thuê nhà",
            "Nhà sở hữu, không vay",
            "Nhà đang trả góp"
        ]
    )

    income_stability = st.selectbox(
        "Tính ổn định của thu nhập",
        [
            "Ổn định",
            "Không ổn định",
            "Thay đổi theo tháng"
        ]
    )

    st.divider()
    st.subheader("💵 Thu nhập và tài sản")

    income = st.number_input(
        "Tổng thu nhập mỗi tháng (VNĐ)",
        min_value=0,
        value=8000000,
        step=500000
    )

    current_savings = st.number_input(
        "Tiền tiết kiệm hiện có (VNĐ)",
        min_value=0,
        value=5000000,
        step=500000
    )

    st.divider()
    st.subheader("🧾 Chi phí mỗi tháng")

    housing_cost = st.number_input(
        "Tiền nhà/thuê nhà (VNĐ)",
        min_value=0,
        value=1500000,
        step=100000
    )

    food_cost = st.number_input(
        "Ăn uống (VNĐ)",
        min_value=0,
        value=2000000,
        step=100000
    )

    transport_cost = st.number_input(
        "Đi lại (VNĐ)",
        min_value=0,
        value=500000,
        step=100000
    )

    bills_cost = st.number_input(
        "Điện, nước, điện thoại, Internet (VNĐ)",
        min_value=0,
        value=500000,
        step=100000
    )

    education_health = st.number_input(
        "Học tập và y tế (VNĐ)",
        min_value=0,
        value=500000,
        step=100000
    )

    personal_cost = st.number_input(
        "Mua sắm, giải trí và chi phí cá nhân (VNĐ)",
        min_value=0,
        value=800000,
        step=100000
    )

    debt_payment = st.number_input(
        "Tiền trả nợ mỗi tháng (VNĐ)",
        min_value=0,
        value=0,
        step=100000
    )

    st.divider()
    st.subheader("🎯 Mục tiêu tiết kiệm")

    goal_name = st.text_input(
        "Tên mục tiêu",
        value="Quỹ dự phòng cá nhân"
    )

    goal_amount = st.number_input(
        "Số tiền muốn đạt được (VNĐ)",
        min_value=0,
        value=20000000,
        step=1000000
    )

    goal_months = st.number_input(
        "Thời gian thực hiện (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    submitted = st.form_submit_button(
        "Phân tích tài chính",
        type="primary",
        use_container_width=True
    )

# =========================
# 3. LƯU THÔNG TIN TRONG PHIÊN
# =========================
if "finance_data" not in st.session_state:
    st.session_state.finance_data = None

if submitted:
    st.session_state.finance_data = {
        "age": age,
        "gender": gender,
        "occupation": occupation,
        "marital_status": marital_status,
        "dependents": dependents,
        "housing": housing,
        "income_stability": income_stability,
        "income": income,
        "current_savings": current_savings,
        "housing_cost": housing_cost,
        "food_cost": food_cost,
        "transport_cost": transport_cost,
        "bills_cost": bills_cost,
        "education_health": education_health,
        "personal_cost": personal_cost,
        "debt_payment": debt_payment,
        "goal_name": goal_name.strip() or "Mục tiêu tiết kiệm",
        "goal_amount": goal_amount,
        "goal_months": goal_months
    }

if st.session_state.finance_data is None:
    st.markdown("### 🚀 Bắt đầu quản lý tài chính của bạn")
    st.write(
        "Điền thông tin ở thanh bên trái rồi nhấn "
        "**Phân tích tài chính** để xem kết quả."
    )

    st.markdown("### Nguyên tắc ứng dụng sử dụng")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 50% - Nhu cầu")
        st.write("Nhà ở, ăn uống, đi lại và các khoản thiết yếu.")

    with c2:
        st.markdown("#### 30% - Mong muốn")
        st.write("Giải trí, mua sắm và những khoản không thiết yếu.")

    with c3:
        st.markdown("#### 20% - Tiết kiệm")
        st.write("Tích lũy, quỹ dự phòng và mục tiêu tài chính.")

    st.caption(
        "Đây là tỷ lệ tham khảo, không phải quy tắc bắt buộc "
        "cho mọi hoàn cảnh."
    )
    st.stop()

# =========================
# 4. TÍNH TOÁN TÀI CHÍNH
# =========================
d = st.session_state.finance_data

age = d["age"]
occupation = d["occupation"]
marital_status = d["marital_status"]
dependents = d["dependents"]
housing = d["housing"]
income_stability = d["income_stability"]
income = d["income"]
current_savings = d["current_savings"]

essential_items = {
    "Nhà ở": d["housing_cost"],
    "Ăn uống": d["food_cost"],
    "Đi lại": d["transport_cost"],
    "Điện, nước, điện thoại": d["bills_cost"],
    "Học tập và y tế": d["education_health"]
}

essential_cost = sum(essential_items.values())
personal_cost = d["personal_cost"]
debt_payment = d["debt_payment"]

total_expenses = essential_cost + personal_cost + debt_payment
cash_left = income - total_expenses

# Xác định số tháng quỹ dự phòng mục tiêu
if (
    income_stability == "Không ổn định"
    or dependents > 0
    or housing == "Nhà đang trả góp"
):
    emergency_months = 6
else:
    emergency_months = 3

# Quỹ dự phòng được tính dựa trên chi phí thiết yếu và trả nợ
monthly_essentials = essential_cost + debt_payment
emergency_target = monthly_essentials * emergency_months
emergency_gap = max(0, emergency_target - current_savings)

# Tỷ lệ tiết kiệm tham khảo theo mức ổn định thu nhập
if income_stability == "Không ổn định":
    saving_rate = 0.10
elif income_stability == "Thay đổi theo tháng":
    saving_rate = 0.15
else:
    saving_rate = 0.20

# Điều chỉnh mục tiêu theo hoàn cảnh
if (
    occupation == "Sinh viên"
    and housing == "Sống cùng gia đình"
    and dependents == 0
    and debt_payment == 0
):
    saving_rate = 0.20

if housing in ["Thuê nhà", "Nhà đang trả góp"] or dependents >= 2:
    saving_rate = min(saving_rate, 0.15)

if debt_payment > 0:
    saving_rate = min(saving_rate, 0.10)

# Tỷ lệ 50/30/20 là định hướng, không ép chi phí thiết yếu
# vượt khả năng chi trả
if income > 0:
    target_needs = min(income, max(essential_cost, income * 0.50))
    target_savings = min(
        income * saving_rate,
        max(0, income - target_needs)
    )
    target_wants = max(
        0,
        income - target_needs - target_savings
    )
else:
    target_needs = 0
    target_savings = 0
    target_wants = 0

if income > 0:
    expense_ratio = total_expenses / income * 100
    actual_saving_ratio = cash_left / income * 100
else:
    expense_ratio = 0
    actual_saving_ratio = 0

goal_amount = d["goal_amount"]
goal_months = d["goal_months"]
goal_name = d["goal_name"]

goal_gap = max(0, goal_amount - current_savings)
goal_monthly = goal_gap / goal_months

# =========================
# 5. CÁC HÀM ĐỊNH DẠNG
# =========================
def money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")

def percent(value):
    return f"{value:.1f}%"

# =========================
# 6. GIAO DIỆN TỔNG QUAN
# =========================
st.divider()
st.header("📊 Tổng quan tài chính")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Thu nhập tháng", money(income))

with col2:
    st.metric("Tổng chi phí tháng", money(total_expenses))

with col3:
    st.metric(
        "Tiền còn lại",
        money(cash_left),
        delta=money(cash_left) if cash_left >= 0 else money(cash_left)
    )

with col4:
    st.metric(
        "Tỷ lệ tiền còn lại",
        percent(actual_saving_ratio)
    )

if income == 0:
    st.warning(
        "Bạn chưa nhập thu nhập. Một số tỷ lệ ngân sách "
        "không thể tính được."
    )
elif cash_left < 0:
    st.error(
        f"Chi phí đang vượt thu nhập {money(abs(cash_left))} mỗi tháng. "
        "Bạn nên rà soát chi tiêu trước khi đặt mục tiêu tiết kiệm."
    )
elif cash_left == 0:
    st.warning(
        "Bạn đang sử dụng toàn bộ thu nhập. "
        "Hãy tìm khoản chi có thể giảm để tạo phần dư tài chính."
    )
else:
    st.success(
        f"Bạn còn {money(cash_left)} sau khi tính các khoản chi "
        "đã khai báo."
    )

# =========================
# 7. PHÂN TÍCH CHI TIÊU
# =========================
st.subheader("🔎 Chi tiêu của bạn")

expense_data = {
    "Nhà ở": d["housing_cost"],
    "Ăn uống": d["food_cost"],
    "Đi lại": d["transport_cost"],
    "Điện, nước, điện thoại": d["bills_cost"],
    "Học tập và y tế": d["education_health"],
    "Mua sắm và giải trí": personal_cost,
    "Trả nợ": debt_payment
}

expense_df = pd.DataFrame(
    [
        {"Khoản chi": name, "Số tiền (VNĐ)": value}
        for name, value in expense_data.items()
    ]
)

left, right = st.columns(2)

with left:
    st.markdown("**Cơ cấu chi tiêu**")
    chart_df = expense_df[
        expense_df["Số tiền (VNĐ)"] > 0
    ].set_index("Khoản chi")

    if not chart_df.empty:
        st.bar_chart(chart_df)
    else:
        st.write("Chưa có khoản chi nào được ghi nhận.")

with right:
    st.markdown("**Chi tiết các khoản chi**")
    display_df = expense_df.copy()
    display_df["Số tiền"] = display_df["Số tiền (VNĐ)"].apply(money)
    display_df = display_df[["Khoản chi", "Số tiền"]]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# =========================
# 8. NGÂN SÁCH ĐỀ XUẤT
# =========================
st.divider()
st.header("🧮 Ngân sách đề xuất")

st.write(
    "Nguyên tắc 50/30/20 là điểm tham khảo. "
    "Ứng dụng ưu tiên chi phí thiết yếu thực tế và khả năng chi trả "
    "của bạn thay vì áp dụng cứng nhắc."
)

budget_df = pd.DataFrame({
    "Nhóm ngân sách": [
        "Nhu cầu thiết yếu",
        "Mong muốn cá nhân",
        "Tiết kiệm dự kiến"
    ],
    "Số tiền đề xuất (VNĐ)": [
        target_needs,
        target_wants,
        target_savings
    ]
})

budget_display = budget_df.copy()
budget_display["Số tiền"] = budget_display[
    "Số tiền đề xuất (VNĐ)"
].apply(money)

st.dataframe(
    budget_display[["Nhóm ngân sách", "Số tiền"]],
    use_container_width=True,
    hide_index=True
)

if income > 0:
    budget_chart = budget_df.set_index("Nhóm ngân sách")
    st.bar_chart(budget_chart)

st.caption(
    "Lưu ý: Số tiền tiết kiệm đề xuất là mục tiêu lập ngân sách, "
    "không phải khoản tiền chắc chắn bạn có thể tiết kiệm. "
    "Nếu chi phí thực tế cao, hãy điều chỉnh kế hoạch."
)

# =========================
# 9. QUỸ DỰ PHÒNG
# =========================
st.divider()
st.header("🛡️ Quỹ dự phòng khẩn cấp")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Quỹ dự phòng mục tiêu", money(emergency_target))

with c2:
    st.metric("Tiền tiết kiệm hiện có", money(current_savings))

with c3:
    st.metric("Số tiền còn thiếu", money(emergency_gap))

st.write(
    f"Với hoàn cảnh hiện tại, ứng dụng đặt mục tiêu quỹ dự phòng "
    f"bằng khoảng {emergency_months} tháng chi phí thiết yếu và trả nợ."
)

if emergency_gap == 0:
    st.success("Tiền tiết kiệm hiện có đã đạt mức quỹ dự phòng mục tiêu.")
else:
    st.info(
        "Bạn có thể xây dựng quỹ dự phòng từng bước. "
        "Ưu tiên khoản tiền dễ tiếp cận khi có tình huống khẩn cấp."
    )

# =========================
# 10. MỤC TIÊU TIẾT KIỆM
# =========================
st.divider()
st.header("🎯 Kế hoạch đạt mục tiêu")

st.write(f"**Mục tiêu:** {goal_name}")
st.write(f"**Số tiền mục tiêu:** {money(goal_amount)}")
st.write(f"**Thời hạn:** {goal_months} tháng")

if goal_gap == 0:
    st.success(
        "Số tiền tiết kiệm hiện có đã bằng hoặc vượt mục tiêu này."
    )
else:
    st.metric(
        "Cần tiết kiệm mỗi tháng",
        money(goal_monthly)
    )

    if goal_amount > 0:
        progress = min(current_savings / goal_amount, 1.0)
    else:
        progress = 1.0

    st.progress(progress)
    st.write(f"Tiến độ hiện tại: {progress * 100:.1f}%")

    if cash_left >= goal_monthly and goal_monthly > 0:
        st.success(
            "Theo thông tin bạn nhập, số tiền còn lại hiện đủ "
            "để đáp ứng mục tiêu tiết kiệm hàng tháng."
        )
    elif goal_monthly > 0:
        st.warning(
            "Mục tiêu có thể vượt quá số tiền còn lại mỗi tháng. "
            "Bạn có thể kéo dài thời hạn, giảm số tiền mục tiêu "
            "hoặc rà soát các khoản chi không thiết yếu."
        )

# =========================
# 11. LỜI KHUYÊN CÁ NHÂN HÓA
# =========================
st.divider()
st.header("💡 Lời khuyên dành cho bạn")

advice = []

if income == 0:
    advice.append(
        "Hãy xác định nguồn thu nhập và xây dựng ngân sách "
        "dựa trên số tiền thực tế."
    )
elif cash_left < 0:
    advice.append(
        "Ưu tiên cân đối thu chi. Xem xét giảm mua sắm, "
        "giải trí hoặc những khoản chưa thực sự cần thiết."
    )
elif expense_ratio > 90:
    advice.append(
        "Chi phí đang chiếm phần lớn thu nhập. "
        "Nên tạo khoản dự phòng trước khi tăng chi tiêu tùy ý."
    )
elif actual_saving_ratio < 10:
    advice.append(
        "Hãy thử dành riêng một khoản nhỏ ngay khi nhận thu nhập, "
        "sau đó điều chỉnh chi tiêu theo số tiền còn lại."
    )
else:
    advice.append(
        "Tiếp tục theo dõi thu chi hàng tháng và duy trì "
        "khoản tiền tiết kiệm phù hợp."
    )

if debt_payment > 0:
    advice.append(
        "Theo dõi lãi suất, số dư và ngày đến hạn trả nợ. "
        "Tránh vay mới để chi trả cho tiêu dùng không thiết yếu."
    )

if emergency_gap > 0:
    advice.append(
        f"Ưu tiên từng bước xây dựng quỹ dự phòng; "
        f"mục tiêu tham khảo hiện tại là {money(emergency_target)}."
    )

if income_stability != "Ổn định":
    advice.append(
        "Vì thu nhập biến động, hãy dựa vào mức thu nhập thấp "
        "thường gặp để lập ngân sách, tránh cam kết chi cố định quá cao."
    )

if housing == "Thuê nhà":
    advice.append(
        "Dành ưu tiên cho tiền thuê nhà và chi phí sinh hoạt "
        "trước khi tăng ngân sách giải trí."
    )

if dependents > 0:
    advice.append(
        "Hãy tính các chi phí chăm sóc người phụ thuộc "
        "vào ngân sách thiết yếu và quỹ dự phòng."
    )

if occupation == "Sinh viên":
    advice.append(
        "Nếu thu nhập còn hạn chế, ưu tiên chi phí học tập, "
        "sinh hoạt và một quỹ dự phòng nhỏ trước khi đầu tư rủi ro."
    )

if age < 25:
    advice.append(
        "Đây là thời điểm tốt để hình thành thói quen ghi chép "
        "chi tiêu và học kiến thức tài chính cơ bản."
    )

if marital_status == "Đã kết hôn":
    advice.append(
        "Nếu quản lý tài chính chung, hãy thống nhất các khoản "
        "chi thiết yếu, mục tiêu tiết kiệm và trách nhiệm trả nợ."
    )

if goal_gap > 0 and goal_monthly > max(cash_left, 0):
    advice.append(
        "Cân nhắc điều chỉnh thời hạn hoặc số tiền mục tiêu "
        "để phù hợp hơn với khả năng tài chính hiện tại."
    )

for i, item in enumerate(advice, start=1):
    st.write(f"{i}. {item}")

# =========================
# 12. TẢI BÁO CÁO
# =========================
st.divider()
st.header("📥 Tải báo cáo tài chính")

report_rows = [
    ("Tuổi", age),
    ("Nghề nghiệp", occupation),
    ("Tình trạng hôn nhân", marital_status),
    ("Số người phụ thuộc", dependents),
    ("Nhà ở", housing),
    ("Ổn định thu nhập", income_stability),
    ("Thu nhập hàng tháng (VNĐ)", income),
    ("Tổng chi phí hàng tháng (VNĐ)", total_expenses),
    ("Tiền còn lại hàng tháng (VNĐ)", cash_left),
    ("Tỷ lệ chi phí (%)", round(expense_ratio, 2)),
    ("Tỷ lệ tiền còn lại (%)", round(actual_saving_ratio, 2)),
    ("Tiền tiết kiệm hiện có (VNĐ)", current_savings),
    ("Quỹ dự phòng mục tiêu (VNĐ)", emergency_target),
    ("Số tiền còn thiếu của quỹ dự phòng (VNĐ)", emergency_gap),
    ("Tên mục tiêu", goal_name),
    ("Số tiền mục tiêu (VNĐ)", goal_amount),
    ("Số tiền cần tiết kiệm mỗi tháng (VNĐ)", goal_monthly)
]

report_df = pd.DataFrame(
    report_rows,
    columns=["Thông tin", "Giá trị"]
)

csv_data = report_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="⬇️ Tải báo cáo CSV",
    data=csv_data,
    file_name="bao_cao_tai_chinh.csv",
    mime="text/csv",
    use_container_width=True
)

# =========================
# 13. KIẾN THỨC TÀI CHÍNH
# =========================
st.divider()
st.header("📚 Góc kiến thức tài chính")

with st.expander("1. Quy tắc 50/30/20"):
    st.write(
        "- 50% thu nhập: nhu cầu thiết yếu.\n"
        "- 30% thu nhập: mong muốn cá nhân.\n"
        "- 20% thu nhập: tiết kiệm và mục tiêu tài chính.\n\n"
        "Đây là quy tắc tham khảo. Nếu chi phí nhà ở hoặc "
        "sinh hoạt cao, bạn có thể điều chỉnh các tỷ lệ."
    )

with st.expander("2. Trả cho bản thân trước"):
    st.write(
        "Khi nhận thu nhập, hãy chuyển một khoản phù hợp "
        "sang tài khoản tiết kiệm trước khi chi tiêu tùy ý. "
        "Số tiền cần linh hoạt theo thu nhập và các nghĩa vụ "
        "tài chính của bạn."
    )

with st.expander("3. Xây dựng quỹ dự phòng"):
    st.write(
        "Quỹ dự phòng giúp ứng phó với mất việc, bệnh tật "
        "hoặc chi phí bất ngờ. Có thể bắt đầu từ một khoản nhỏ "
        "rồi hướng tới khoảng 3–6 tháng chi phí thiết yếu."
    )

with st.expander("4. Phân biệt nhu cầu và mong muốn"):
    st.write(
        "Nhu cầu là những khoản quan trọng như ăn uống, "
        "nhà ở và đi lại. Mong muốn là những khoản có thể "
        "cắt giảm hoặc trì hoãn, chẳng hạn mua sắm không cần thiết."
    )

with st.expander("5. Đặt mục tiêu SMART"):
    st.write(
        "Mục tiêu nên cụ thể, đo lường được, khả thi, "
        "phù hợp và có thời hạn. Ví dụ: tiết kiệm 12 triệu VNĐ "
        "trong 12 tháng, tương đương 1 triệu VNĐ mỗi tháng "
        "nếu chưa có khoản tiết kiệm dành cho mục tiêu đó."
    )

with st.expander("6. Quản lý nợ"):
    st.write(
        "Theo dõi lãi suất, số tiền tối thiểu phải trả và "
        "ngày đến hạn. Ưu tiên trả đúng hạn và xem xét xử lý "
        "các khoản nợ lãi suất cao trước khi tăng chi tiêu tùy ý."
    )

st.caption(
    "MoneyMate là công cụ giáo dục tài chính cá nhân. "
    "Kết quả dựa trên thông tin do người dùng nhập và các quy tắc "
    "tham khảo; không phải tư vấn tài chính chuyên nghiệp. "
    "Ứng dụng không kết nối tài khoản ngân hàng và không lưu hồ sơ "
    "tài chính lâu dài sau khi phiên sử dụng kết thúc."
)
