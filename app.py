    with z:
        st.metric("Quỹ dự phòng tham khảo", money(emergency_target))
        st.caption(f"{emergency_months} tháng chi phí thiết yếu và trả nợ")

    if cash_left < 0:
        st.markdown(f'<div class="warning"><b>⚠️ Cần cân đối dòng tiền.</b> Bạn đang thiếu {money(abs(cash_left))} mỗi tháng theo số liệu đã nhập. Hãy rà soát chi phí trước khi đặt mục tiêu tiết kiệm.</div>', unsafe_allow_html=True)
    elif expense_ratio is not None and expense_ratio < 0.70:
        st.markdown('<div class="tip"><b>🌱 Có thể xây dựng thói quen tài chính tốt.</b> Hãy theo dõi chi tiêu hàng tuần, tự động hóa tiết kiệm và xây dựng quỹ dự phòng.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning"><b>🔎 Nên theo dõi ngân sách sát hơn.</b> Chi phí bắt buộc đang chiếm phần đáng kể trong thu nhập. Hãy kiểm tra từng khoản và điều chỉnh theo thực tế.</div>', unsafe_allow_html=True)

    st.markdown("### 💡 Lời khuyên dành cho bạn")
    for number, tip in enumerate(personalized_advice(), start=1):
        st.markdown(f"**{number}.** {tip}")

    st.markdown("### 👤 Tóm tắt hồ sơ")
    st.write(f"- **Độ tuổi:** {age} · **Công việc:** {occupation}\n- **Tình trạng hôn nhân:** {marital} · **Người phụ thuộc:** {dependents}\n- **Nhà ở:** {housing} · **Độ ổn định thu nhập:** {income_stability}\n- **Giới tính:** {gender}")
    st.caption("Giới tính chỉ là thông tin mô tả, không làm thay đổi công thức phân bổ ngân sách.")

elif page == "Ngân sách đề xuất":
    st.subheader("🪙 Ngân sách hàng tháng")
    st.write("Quy tắc 50/30/20 là điểm khởi đầu: khoảng 50% cho nhu cầu thiết yếu, 30% cho mong muốn và 20% cho tiết kiệm/trả nợ. MoneyMate đối chiếu nguyên tắc này với chi phí thực tế và điều chỉnh đề xuất theo hoàn cảnh.")
    if income <= 0:
        st.warning("Nhập thu nhập lớn hơn 0 để tạo ngân sách.")
    else:
        budget_df = pd.DataFrame({"Nhóm": ["Nhu cầu thiết yếu", "Mong muốn cá nhân", "Tiết kiệm đề xuất"], "Số tiền (VNĐ)": [target_needs, target_wants, target_savings]})
        budget_df["Tỷ lệ thu nhập (%)"] = budget_df["Số tiền (VNĐ)"] / income * 100
        left, right = st.columns([1.05, 1])
        with left:
            fig = px.pie(budget_df, names="Nhóm", values="Số tiền (VNĐ)", hole=0.55, title="Phân bổ thu nhập đề xuất")
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(margin=dict(t=55, b=10, l=10, r=10), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.markdown("#### Kế hoạch đề xuất")
            display_df = budget_df.copy()
            display_df["Số tiền (VNĐ)"] = display_df["Số tiền (VNĐ)"].map(money)
            display_df["Tỷ lệ thu nhập (%)"] = display_df["Tỷ lệ thu nhập (%)"].map(lambda v: f"{v:.1f}%")
            st.dataframe(display_df, hide_index=True, use_container_width=True)
            st.caption("Đây là gợi ý tham khảo, không phải yêu cầu bắt buộc. Nhu cầu thiết yếu và nghĩa vụ nợ thực tế cần được ưu tiên.")
        st.markdown("#### So sánh với tình hình hiện tại")
        comparison = pd.DataFrame({"Khoản mục": ["Chi phí thiết yếu đã khai báo", "Trả nợ hàng tháng", "Tổng chi phí và trả nợ", "Tiền còn lại sau chi phí"], "Số tiền (VNĐ)": [essential_cost, debt_payment, total_committed, cash_left]})
        comparison["Số tiền (VNĐ)"] = comparison["Số tiền (VNĐ)"].map(money)
        st.dataframe(comparison, hide_index=True, use_container_width=True)
        if essential_cost > income * 0.50:
            st.warning("Chi phí thiết yếu cao hơn mốc 50% thu nhập. Không nên cắt giảm cực đoan các khoản liên quan đến an toàn, sức khỏe hoặc công việc; hãy rà soát từng khoản.")
        if target_savings < income * 0.20:
            st.info("Mức tiết kiệm đề xuất thấp hơn mốc 20% do chi phí nhà ở, người phụ thuộc, thu nhập biến động hoặc khoản trả nợ. Khi hoàn cảnh cải thiện, bạn có thể tăng dần tỷ lệ.")
        st.download_button("⬇️ Tải ngân sách CSV", data=budget_df.to_csv(index=False).encode("utf-8-sig"), file_name="moneymate_ngan_sach.csv", mime="text/csv", use_container_width=True)

elif page == "Mục tiêu tiết kiệm":
    st.subheader("🎯 Kế hoạch đạt mục tiêu")
    amount_left = max(0, goal_amount - savings)
    monthly_needed = amount_left / goal_months if goal_months else amount_left
    a, b, c = st.columns(3)
    with a: metric_card("Mục tiêu", goal_name, "Mục tiêu đã chọn")
    with b: metric_card("Số tiền còn cần", money(amount_left), "Đã trừ tiết kiệm hiện có")
    with c: metric_card("Cần để dành mỗi tháng", money(monthly_needed), f"Trong {goal_months} tháng")
    if goal_amount > 0:
        progress = min(1.0, savings / goal_amount)
        st.progress(progress, text=f"Bạn đã có {progress*100:.1f}% mục tiêu")
        months = list(range(int(goal_months) + 1))
        amounts = [min(goal_amount, savings + monthly_needed * m) for m in months]
        df_goal = pd.DataFrame({"Tháng": months, "Số tiền tích lũy dự kiến (VNĐ)": amounts})
        fig = px.line(df_goal, x="Tháng", y="Số tiền tích lũy dự kiến (VNĐ)", markers=True, title="Lộ trình tích lũy dự kiến (chưa tính lãi)")
        fig.update_layout(margin=dict(t=55, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    if amount_left == 0:
        st.success("Bạn đã đạt hoặc vượt mục tiêu tiết kiệm đã nhập.")
    elif cash_left < monthly_needed:
        st.warning(f"Số tiền còn lại mỗi tháng chưa đủ để dành {money(monthly_needed)}. Hãy kéo dài thời hạn, giảm mục tiêu hoặc tìm cách tăng thu nhập; tránh vay thêm chỉ để đạt mục tiêu.")
    else:
        st.success(f"Mục tiêu có thể khả thi nếu bạn dành khoảng {money(monthly_needed)} mỗi tháng và duy trì kế hoạch.")
    st.caption("Mô phỏng chưa tính lãi tiền gửi, lạm phát, biến động thu nhập hoặc chi phí phát sinh.")

else:
    st.subheader("📚 Kiến thức quản lý tài chính cá nhân")
    st.write("Các nguyên tắc dưới đây là khung tham khảo để xây dựng lời khuyên trong MoneyMate.")
    with st.expander("1. Quy tắc 50/30/20", expanded=True):
        st.markdown("- **50% nhu cầu thiết yếu:** nhà ở, ăn uống, đi lại, hóa đơn, sức khỏe và chi phí cần thiết.\n- **30% mong muốn:** giải trí, mua sắm không thiết yếu và sở thích.\n- **20% tiết kiệm/trả nợ:** quỹ dự phòng, mục tiêu tương lai và nghĩa vụ nợ phù hợp.\n\nĐây là quy tắc tham khảo. Người có chi phí nhà ở cao, thu nhập thấp hoặc nhiều người phụ thuộc có thể cần tỷ lệ khác.")
    with st.expander("2. Pay Yourself First – tiết kiệm trước"):
        st.write("Khi nhận thu nhập, dành riêng một khoản tiết kiệm vừa sức trước khi chi cho mong muốn. Có thể bắt đầu từ 5–10% rồi tăng dần khi ngân sách cho phép.")
    with st.expander("3. Quỹ dự phòng khẩn cấp"):
        st.write("Một mục tiêu thường dùng là khoảng 3–6 tháng chi phí thiết yếu. Người có thu nhập không ổn định hoặc nhiều người phụ thuộc có thể cần quỹ dự phòng lớn hơn.")
    with st.expander("4. Phân biệt nhu cầu và mong muốn"):
        st.write("Nhu cầu giúp duy trì cuộc sống, sức khỏe, học tập hoặc công việc. Mong muốn có thể trì hoãn hoặc chọn phương án ít tốn kém hơn.")
    with st.expander("5. Quản lý nợ"):
        st.write("Ghi rõ dư nợ, lãi suất, ngày đến hạn và khoản thanh toán tối thiểu. Tránh trả trễ; sau khi bảo đảm nhu cầu thiết yếu, cân nhắc ưu tiên nợ có lãi suất cao.")
    with st.expander("6. Mục tiêu SMART"):
        st.write("Mục tiêu nên cụ thể, đo lường được, khả thi, phù hợp và có thời hạn. Ví dụ: tích lũy 12 triệu đồng trong 12 tháng, tương đương 1 triệu đồng mỗi tháng nếu chưa tính lãi.")
    st.markdown("### 📖 Nguồn để nhóm đọc và trích dẫn")
    st.markdown("""
    - **Consumer Financial Protection Bureau (CFPB):** tài liệu giáo dục về lập ngân sách và tiết kiệm.
    - **FINRA Investor Education Foundation:** tài liệu về quỹ dự phòng và nền tảng tài chính cá nhân.
    - **Quy tắc 50/30/20:** tra cứu tài liệu giáo dục ngân sách từ các tổ chức tài chính uy tín.

    Khi làm báo cáo, hãy đọc tài liệu gốc, ghi tên tài liệu, tác giả/tổ chức, năm xuất bản và ngày truy cập theo yêu cầu của giảng viên.
    """)

st.divider()
st.markdown('<div style="text-align:center;color:#7b8794;font-size:.85rem"><b>MoneyMate</b> · Mỗi quyết định nhỏ hôm nay góp phần tạo nên tương lai tài chính vững vàng.<br>Ứng dụng phục vụ học tập và lập ngân sách cơ bản; kết quả phụ thuộc vào dữ liệu người dùng nhập.</div>', unsafe_allow_html=True)
