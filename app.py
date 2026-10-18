    if remaining < 0:
        st.markdown(f'<div class="warning"><b>⚠️ Cần ưu tiên cân đối dòng tiền.</b> Hiện tại bạn đang thiếu {vnd(abs(remaining))} mỗi tháng. Hãy giảm khoản chi linh hoạt và rà soát các nghĩa vụ cố định trước khi đặt mục tiêu tiết kiệm.</div>', unsafe_allow_html=True)
    elif income > 0 and expense_ratio < 0.7:
        st.markdown('<div class="tip"><b>🌱 Có dư địa để xây dựng thói quen tốt.</b> Hãy tự động hóa tiết kiệm, theo dõi chi tiêu theo tuần và tăng quỹ dự phòng trước khi cân nhắc mục tiêu rủi ro cao.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning"><b>🔎 Nên theo dõi dòng tiền sát hơn.</b> Chi phí bắt buộc đang chiếm phần đáng kể trong thu nhập. Hãy kiểm tra ngân sách hàng tuần và tránh đặt mức tiết kiệm vượt khả năng thực tế.</div>', unsafe_allow_html=True)

    st.markdown("### 🧾 Các lời khuyên dành cho bạn")
    for i, tip in enumerate(build_advice(), 1):
        st.markdown(f"**{i}.** {tip}")

    st.markdown("### 🧩 Hồ sơ ảnh hưởng đến kế hoạch như thế nào?")
    profile_notes = []
    profile_notes.append(f"**Giai đoạn:** {age} tuổi · {occupation.lower()}.")
    profile_notes.append(f"**Nhà ở:** {housing.lower()}; khoản nhà ở bạn khai báo là {vnd(housing_cost)}/tháng.")
    profile_notes.append(f"**Gia đình:** {marital.lower()}, đang chu cấp cho {dependents} người.")
    profile_notes.append(f"**Độ ổn định thu nhập:** {income_stability.lower()}. App dùng thông tin này để gợi ý mức dự phòng, không dùng giới tính để áp đặt ngân sách.")
    st.write("\n\n".join(profile_notes))

elif page == "Lập ngân sách":
    st.subheader("🪙 Ngân sách tháng được cá nhân hóa")
    st.write("MoneyMate lấy chi phí bạn khai báo làm cơ sở, sau đó so sánh với nguyên tắc 50/30/20. Đây là kế hoạch tham khảo và có thể điều chỉnh.")
    if income > 0:
        budget_df = pd.DataFrame({
            "Nhóm ngân sách": ["Nhu cầu thiết yếu", "Mong muốn cá nhân", "Tiết kiệm / mục tiêu"],
            "Số tiền (VNĐ)": [recommended_needs, recommended_wants, recommended_savings]
        })
        c1, c2 = st.columns([1.05, 1])
        with c1:
            fig = px.pie(budget_df, names="Nhóm ngân sách", values="Số tiền (VNĐ)", hole=0.58,
                         title="Phân bổ thu nhập đề xuất")
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(margin=dict(t=55,b=10,l=10,r=10), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            view_df = budget_df.copy()
            view_df["Số tiền (VNĐ)"] = view_df["Số tiền (VNĐ)"].map(vnd)
            st.markdown("#### Số tiền đề xuất")
            st.dataframe(view_df, hide_index=True, use_container_width=True)
            st.caption("Phần tiết kiệm đề xuất là mục tiêu ban đầu; nếu chi phí bắt buộc quá cao, hãy ưu tiên nhu cầu thiết yếu và trả nợ đúng hạn.")
        st.markdown("#### Đối chiếu chi phí thực tế")
        comparison = pd.DataFrame({
            "Khoản mục": ["Chi phí thiết yếu bạn nhập", "Ngân sách nhu cầu đề xuất", "Trả nợ hàng tháng", "Số tiền còn lại sau chi phí và trả nợ"],
            "Số tiền (VNĐ)": [essential_actual, recommended_needs, debt_payment, remaining]
        })
        st.dataframe(comparison.assign(**{"Số tiền (VNĐ)": comparison["Số tiền (VNĐ)"].map(vnd)}), hide_index=True, use_container_width=True)
        st.markdown("#### Gợi ý hành động")
        if essential_actual > recommended_needs:
            st.warning("Chi phí thiết yếu khai báo đang cao hơn ngân sách nhu cầu tham khảo. Không nên cắt giảm các nhu cầu an toàn hoặc sức khỏe một cách cực đoan; hãy rà soát từng khoản và điều chỉnh theo thực tế.")
        if recommended_wants < income * 0.1:
            st.info("Ngân sách cho mong muốn cá nhân đang khá thấp. Hãy xem đây là tín hiệu để rà soát chi phí cố định, không phải yêu cầu phải loại bỏ hoàn toàn giải trí.")
        st.download_button(
            "⬇️ Tải ngân sách dạng CSV",
            data=budget_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="moneymate_ngan_sach.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("Nhập thu nhập lớn hơn 0 để tạo ngân sách.")

elif page == "Mục tiêu tiết kiệm":
    st.subheader("🎯 Kế hoạch đạt mục tiêu")
    gap = max(0, goal_amount - savings)
    monthly_need = gap / goal_months if goal_months else gap
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Mục tiêu", goal_name, "Mục tiêu bạn chọn")
    with c2:
        metric_card("Còn cần tích lũy", vnd(gap), "Đã trừ khoản tiết kiệm hiện có")
    with c3:
        metric_card("Cần để dành mỗi tháng", vnd(monthly_need), f"Trong {goal_months} tháng")
    st.markdown("### 🗓️ Tiến độ dự kiến")
    if goal_amount > 0:
        progress = min(1.0, savings / goal_amount)
        st.progress(progress, text=f"Đã có {progress*100:.1f}% mục tiêu")
        months = list(range(0, int(goal_months) + 1))
        balances = [min(goal_amount, savings + monthly_need * m) for m in months]
        df_goal = pd.DataFrame({"Tháng": months, "Tích lũy dự kiến (VNĐ)": balances})
        fig = px.line(df_goal, x="Tháng", y="Tích lũy dự kiến (VNĐ)", markers=True,
                      title="Lộ trình tích lũy (không tính lãi)")
        fig.update_layout(margin=dict(t=55,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)
    if monthly_need == 0:
        st.success("Bạn đã đạt hoặc vượt số tiền mục tiêu đã nhập.")
    elif remaining < monthly_need:
        st.warning(f"Với dòng tiền hiện tại, bạn chưa có đủ {vnd(monthly_need)}/tháng để đạt mục tiêu. Hãy kéo dài thời hạn, giảm số tiền mục tiêu hoặc tìm cách tăng thu nhập; tránh vay thêm chỉ để đạt mục tiêu.")
    else:
        st.success(f"Mục tiêu có vẻ khả thi theo số liệu đã nhập nếu bạn dành khoảng {vnd(monthly_need)}/tháng và duy trì kỷ luật.")
    st.caption("Mô phỏng đơn giản, chưa tính lãi tiền gửi, lạm phát, biến động thu nhập hay chi phí bất ngờ.")

else:
    st.subheader("📚 Góc học nhanh về quản lý tài chính")
    st.write("Các nguyên tắc dưới đây là khung tham khảo để hình thành thói quen, không phải quy tắc bắt buộc cho tất cả mọi người.")
    with st.expander("1. Quy tắc 50/30/20", expanded=True):
        st.write("- **50% nhu cầu:** nhà ở, ăn uống, đi lại, hóa đơn, chi phí thiết yếu.\n- **30% mong muốn:** giải trí, mua sắm không thiết yếu, sở thích.\n- **20% tiết kiệm và trả nợ:** quỹ dự phòng, mục tiêu dài hạn và nghĩa vụ nợ phù hợp.")
        st.write("Nếu tiền thuê nhà hoặc chi phí gia đình cao, tỷ lệ này có thể không phù hợp. Hãy bắt đầu từ ngân sách thực tế.")
    with st.expander("2. Pay Yourself First – trả cho bản thân trước"):
        st.write("Ngay khi nhận thu nhập, chuyển một khoản vừa sức sang tài khoản tiết kiệm riêng. Có thể bắt đầu 5–10% rồi tăng dần thay vì đặt mục tiêu quá cao và bỏ cuộc.")
    with st.expander("3. Quỹ dự phòng khẩn cấp"):
        st.write("Một mục tiêu thường dùng là tích lũy khoảng 3–6 tháng chi phí thiết yếu. Người có thu nhập thất thường hoặc nhiều người phụ thuộc có thể cần mức dự phòng cao hơn.")
    with st.expander("4. Phân biệt nhu cầu và mong muốn"):
        st.write("Nhu cầu là khoản cần để duy trì cuộc sống, sức khỏe, học tập hoặc công việc. Mong muốn có thể trì hoãn hoặc chọn phương án rẻ hơn. Một khoản chi có thể khác nhau tùy hoàn cảnh.")
    with st.expander("5. Quản lý nợ"):
        st.write("Ghi rõ dư nợ, lãi suất, ngày đến hạn và khoản trả tối thiểu. Tránh trễ hạn; sau khi đảm bảo nghĩa vụ thiết yếu, cân nhắc ưu tiên nợ lãi suất cao.")
    with st.expander("6. Mục tiêu SMART"):
        st.write("Mục tiêu nên cụ thể, đo lường được, khả thi, phù hợp và có thời hạn. Ví dụ: tiết kiệm 12 triệu đồng trong 12 tháng, tương đương 1 triệu đồng mỗi tháng nếu chưa tính lãi.")
    st.markdown("### 📖 Nguồn nguyên tắc để nhóm tham khảo")
    st.markdown("""
    - **50/30/20:** thường được phổ biến trong tài liệu giáo dục ngân sách cá nhân; nên trình bày như một quy tắc tham khảo, không phải chuẩn bắt buộc.
    - **Consumer Financial Protection Bureau (CFPB):** tài liệu giáo dục về lập ngân sách, tiết kiệm và quỹ dự phòng.
    - **FINRA Investor Education Foundation:** tài liệu về quỹ dự phòng, quản lý nợ và nền tảng tài chính.
    - **SMART goals:** khung thiết lập mục tiêu có tính cụ thể, đo lường được và có thời hạn.

    Khi làm báo cáo, nhóm nên đọc nguồn gốc, ghi tên tài liệu/ngày truy cập và trích dẫn đúng định dạng mà giảng viên yêu cầu.
    """)

st.divider()
st.markdown("""
<div style="text-align:center;color:#7b8794;font-size:.85rem">
  <b>MoneyMate</b> · Một bước nhỏ hôm nay, tài chính vững vàng hơn ngày mai.<br>
  Công cụ phục vụ học tập và lập ngân sách cơ bản; kết quả phụ thuộc vào dữ liệu người dùng nhập.
</div>
""", unsafe_allow_html=True)
