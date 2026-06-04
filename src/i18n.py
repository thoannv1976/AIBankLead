"""Internationalization (i18n) for BankLead AI — English & Vietnamese.

Pure module (no Streamlit dependency) so it can be imported anywhere,
including the scoring logic. The current language is resolved in ``ui.py``
and passed into ``t()`` and the label helpers as an explicit ``lang`` code
("en" or "vi").
"""

from __future__ import annotations

LANGUAGES = {"en": "English", "vi": "Tiếng Việt"}
DEFAULT_LANG = "vi"


# ---------------------------------------------------------------------------
# Translation table:  key -> {"en": ..., "vi": ...}
# Values may contain {named} placeholders filled via str.format(**kwargs).
# ---------------------------------------------------------------------------
TRANSLATIONS: dict[str, dict[str, str]] = {
    # ---- shared / sidebar -------------------------------------------------
    "language_label": {"en": "🌐 Language / Ngôn ngữ", "vi": "🌐 Ngôn ngữ / Language"},
    "guard.no_data": {
        "en": "No data loaded yet. Go to **Upload & Preview** to load a CSV "
              "(or load the bundled sample dataset).",
        "vi": "Chưa có dữ liệu. Vào trang **Tải & Xem trước** để nạp file CSV "
              "(hoặc dùng bộ dữ liệu mẫu có sẵn).",
    },
    "guard.no_models": {
        "en": "No trained models yet. Go to **Train & Evaluate** first.",
        "vi": "Chưa có mô hình nào được huấn luyện. Hãy vào trang "
              "**Huấn luyện & Đánh giá** trước.",
    },

    # ---- dashboard --------------------------------------------------------
    "dash.subtitle": {
        "en": "AI-driven customer analytics to identify high-potential "
              "personal-loan leads from banking profile data.",
        "vi": "Phân tích khách hàng bằng AI để xác định khách hàng tiềm năng "
              "vay cá nhân từ dữ liệu hồ sơ ngân hàng.",
    },
    "dash.about_title": {"en": "About this app", "vi": "Giới thiệu ứng dụng"},
    "dash.about_body": {
        "en": "BankLead AI helps retail-banking marketing teams move from mass "
              "marketing to **data-driven targeting**. Instead of offering "
              "personal loans to everyone, the bank can rank customers by an AI "
              "**lead score** and focus on the most promising segments.",
        "vi": "BankLead AI giúp đội marketing ngân hàng bán lẻ chuyển từ "
              "marketing đại trà sang **nhắm mục tiêu dựa trên dữ liệu**. Thay "
              "vì mời vay tất cả khách hàng, ngân hàng có thể xếp hạng khách "
              "hàng theo **điểm tiềm năng** do AI tính và tập trung vào nhóm "
              "hứa hẹn nhất.",
    },
    "dash.research_objective": {
        "en": "**Research objective** — *AI-based customer analytics for "
              "potential customer identification in banking using customer "
              "profile data.*",
        "vi": "**Mục tiêu nghiên cứu** — *Phân tích khách hàng dựa trên AI để "
              "xác định khách hàng tiềm năng trong ngân hàng bằng dữ liệu hồ sơ "
              "khách hàng.*",
    },
    "dash.workflow": {
        "en": "**Workflow**\n"
              "1. Upload customer CSV → 2. Auto preprocess → 3. Train models "
              "(Logistic Regression, Random Forest, XGBoost) → 4. Evaluate → "
              "5. Score & rank leads → 6. Export for CRM.",
        "vi": "**Quy trình**\n"
              "1. Tải CSV khách hàng → 2. Tự động tiền xử lý → 3. Huấn luyện mô "
              "hình (Logistic Regression, Random Forest, XGBoost) → 4. Đánh giá "
              "→ 5. Chấm điểm & xếp hạng → 6. Xuất sang CRM.",
    },
    "dash.pages_title": {"en": "Pages", "vi": "Các trang"},
    "dash.pages_list": {
        "en": "- 📤 **Upload & Preview**\n- 🤖 **Train & Evaluate**\n"
              "- 🎯 **Lead Scoring**\n- 📊 **Customer Insights**\n"
              "- 📥 **Export Results**",
        "vi": "- 📤 **Tải & Xem trước**\n- 🤖 **Huấn luyện & Đánh giá**\n"
              "- 🎯 **Chấm điểm tiềm năng**\n- 📊 **Phân tích khách hàng**\n"
              "- 📥 **Xuất kết quả**",
    },
    "dash.nav_caption": {
        "en": "Use the sidebar to navigate between pages.",
        "vi": "Dùng thanh bên trái để chuyển giữa các trang.",
    },
    "dash.status_title": {"en": "Current session status", "vi": "Trạng thái phiên làm việc"},
    "dash.status_need_upload": {
        "en": "👉 Start by going to **Upload & Preview** to load a customer CSV "
              "(or click *Load sample dataset* there).",
        "vi": "👉 Bắt đầu bằng cách vào **Tải & Xem trước** để nạp CSV khách "
              "hàng (hoặc bấm *Nạp dữ liệu mẫu*).",
    },
    "dash.status_need_train": {
        "en": "✅ Data loaded. Next, open **Train & Evaluate** to train the models.",
        "vi": "✅ Đã nạp dữ liệu. Tiếp theo, mở **Huấn luyện & Đánh giá** để "
              "huấn luyện mô hình.",
    },
    "dash.status_need_score": {
        "en": "✅ Models trained. Open **Lead Scoring** to rank your customers.",
        "vi": "✅ Đã huấn luyện mô hình. Mở **Chấm điểm tiềm năng** để xếp hạng "
              "khách hàng.",
    },
    "dash.status_complete": {
        "en": "✅ Pipeline complete. Visit **Lead Scoring**, **Customer "
              "Insights**, and **Export Results**.",
        "vi": "✅ Hoàn tất quy trình. Hãy xem **Chấm điểm tiềm năng**, **Phân "
              "tích khách hàng** và **Xuất kết quả**.",
    },
    "dash.priority_caption": {
        "en": "Priority bands — High: score ≥ {high:.2f} · "
              "Medium: {med:.2f}–{high_minus:.2f} · Low: < {med:.2f}",
        "vi": "Mức ưu tiên — Cao: điểm ≥ {high:.2f} · "
              "Trung bình: {med:.2f}–{high_minus:.2f} · Thấp: < {med:.2f}",
    },

    # ---- metrics (shared) -------------------------------------------------
    "metric.customers_uploaded": {"en": "Customers uploaded", "vi": "Khách hàng đã tải"},
    "metric.acceptance": {"en": "Personal-loan acceptance", "vi": "Tỷ lệ chấp nhận vay"},
    "metric.models_trained": {"en": "Models trained", "vi": "Số mô hình đã huấn luyện"},
    "metric.best_model": {"en": "Best model", "vi": "Mô hình tốt nhất"},
    "val.not_trained": {"en": "Not trained", "vi": "Chưa huấn luyện"},
    "metric.records": {"en": "Customer records", "vi": "Số bản ghi khách hàng"},
    "metric.variables": {"en": "Variables", "vi": "Số biến"},
    "metric.missing_values": {"en": "Missing values", "vi": "Giá trị thiếu"},
    "metric.acceptance_short": {"en": "Acceptance rate", "vi": "Tỷ lệ chấp nhận"},
    "val.no_target": {"en": "no target", "vi": "không có biến mục tiêu"},
    "metric.accepted": {"en": "Accepted (1)", "vi": "Chấp nhận (1)"},
    "metric.not_accepted": {"en": "Not accepted (0)", "vi": "Không chấp nhận (0)"},

    # ---- page hero titles -------------------------------------------------
    "upload.title": {"en": "Upload & Preview", "vi": "Tải & Xem trước"},
    "train.title": {"en": "Train & Evaluate", "vi": "Huấn luyện & Đánh giá"},
    "lead.title": {"en": "Lead Scoring", "vi": "Chấm điểm tiềm năng"},
    "insights.title": {"en": "Customer Insights", "vi": "Phân tích khách hàng"},
    "export.title": {"en": "Export Results", "vi": "Xuất kết quả"},

    # ---- upload page ------------------------------------------------------
    "upload.subtitle": {
        "en": "Load a customer CSV and inspect it before training.",
        "vi": "Nạp file CSV khách hàng và kiểm tra trước khi huấn luyện.",
    },
    "upload.uploader_label": {
        "en": "Upload customer profile CSV", "vi": "Tải lên CSV hồ sơ khách hàng",
    },
    "upload.uploader_help": {
        "en": "Expected columns include Age, Income, Family, CCAvg, Education, "
              "Mortgage, CD Account, Online, CreditCard and the target "
              "'Personal Loan'.",
        "vi": "Các cột kỳ vọng: Age, Income, Family, CCAvg, Education, Mortgage, "
              "CD Account, Online, CreditCard và biến mục tiêu 'Personal Loan'.",
    },
    "upload.loaded_rows": {
        "en": "Loaded **{name}** — {n:,} rows.",
        "vi": "Đã nạp **{name}** — {n:,} dòng.",
    },
    "upload.read_error": {"en": "Could not read CSV: {err}", "vi": "Không đọc được CSV: {err}"},
    "upload.load_sample_btn": {"en": "📥 Load sample dataset", "vi": "📥 Nạp dữ liệu mẫu"},
    "upload.sample_loaded": {
        "en": "Sample dataset loaded — {n:,} rows.",
        "vi": "Đã nạp dữ liệu mẫu — {n:,} dòng.",
    },
    "upload.sample_not_found": {
        "en": "Sample file not found. Run "
              "`python sample_data/generate_sample.py` first.",
        "vi": "Không tìm thấy file mẫu. Hãy chạy "
              "`python sample_data/generate_sample.py` trước.",
    },
    "upload.need_data_info": {
        "en": "Upload a CSV or load the sample dataset to continue.",
        "vi": "Tải lên một CSV hoặc nạp dữ liệu mẫu để tiếp tục.",
    },
    "upload.target_warning": {
        "en": "⚠️ Target column **'{target}'** not detected. Training requires "
              "a personal-loan label (1 = accepted, 0 = not).",
        "vi": "⚠️ Không phát hiện cột mục tiêu **'{target}'**. Việc huấn luyện "
              "cần nhãn vay cá nhân (1 = chấp nhận, 0 = không).",
    },
    "upload.preview_title": {"en": "Data preview", "vi": "Xem trước dữ liệu"},
    "upload.missing_title": {"en": "Missing values", "vi": "Giá trị thiếu"},
    "upload.no_missing": {"en": "No missing values detected. 🎉", "vi": "Không có giá trị thiếu. 🎉"},
    "upload.col_column": {"en": "column", "vi": "cột"},
    "upload.col_missing": {"en": "missing", "vi": "số thiếu"},
    "upload.target_dist_title": {
        "en": "Target distribution — Personal Loan",
        "vi": "Phân phối biến mục tiêu — Vay cá nhân",
    },
    "chart.customers": {"en": "Customers", "vi": "Số khách hàng"},
    "upload.imbalance_caption": {
        "en": "Personal-loan acceptance is typically imbalanced — the app "
              "handles this with balanced class weights / scale_pos_weight.",
        "vi": "Tỷ lệ chấp nhận vay thường mất cân bằng — ứng dụng xử lý bằng "
              "trọng số lớp cân bằng / scale_pos_weight.",
    },
    "upload.data_ready": {
        "en": "Data ready. Proceed to **Train & Evaluate**.",
        "vi": "Dữ liệu đã sẵn sàng. Chuyển sang **Huấn luyện & Đánh giá**.",
    },

    # ---- train page -------------------------------------------------------
    "train.subtitle": {
        "en": "Train Logistic Regression, Random Forest and XGBoost, then "
              "compare them on lead-targeting metrics.",
        "vi": "Huấn luyện Logistic Regression, Random Forest và XGBoost, rồi so "
              "sánh trên các thước đo nhắm khách hàng tiềm năng.",
    },
    "train.xgb_missing_caption": {
        "en": "ℹ️ XGBoost not installed — only Logistic Regression and Random "
              "Forest are available.",
        "vi": "ℹ️ Chưa cài XGBoost — chỉ có Logistic Regression và Random Forest.",
    },
    "train.models_to_train": {"en": "Models to train", "vi": "Mô hình cần huấn luyện"},
    "train.test_size": {"en": "Test size", "vi": "Tỷ lệ tập kiểm tra"},
    "train.train_btn": {"en": "🚀 Train models", "vi": "🚀 Huấn luyện mô hình"},
    "train.select_one": {"en": "Select at least one model.", "vi": "Hãy chọn ít nhất một mô hình."},
    "train.spinner": {"en": "Preprocessing and training...", "vi": "Đang tiền xử lý và huấn luyện..."},
    "train.trained_success": {
        "en": "Trained {n} model(s). Dropped columns: {dropped}.",
        "vi": "Đã huấn luyện {n} mô hình. Cột đã loại bỏ: {dropped}.",
    },
    "val.none": {"en": "none", "vi": "không có"},
    "train.need_target_error": {
        "en": "Target column '{target}' is required to train models.",
        "vi": "Cần có cột mục tiêu '{target}' để huấn luyện mô hình.",
    },
    "train.info_configure": {
        "en": "Configure and train models to see the evaluation dashboard.",
        "vi": "Cấu hình và huấn luyện mô hình để xem bảng đánh giá.",
    },
    "train.best_model_title": {"en": "🏆 Best model", "vi": "🏆 Mô hình tốt nhất"},
    "train.best_caption": {
        "en": "Selected by combined ranking on PR-AUC and top-k lead "
              "performance — the most relevant metrics for imbalanced lead "
              "identification.",
        "vi": "Được chọn theo xếp hạng kết hợp PR-AUC và hiệu suất lead top-k — "
              "các thước đo phù hợp nhất cho dữ liệu mất cân bằng.",
    },
    "train.perf_comparison": {"en": "Performance comparison", "vi": "So sánh hiệu suất"},
    "train.visual_comparison": {"en": "Visual comparison", "vi": "So sánh trực quan"},
    "tab.core_metrics": {"en": "Core metrics", "vi": "Thước đo cốt lõi"},
    "tab.topk_metrics": {"en": "Top-k lead metrics", "vi": "Thước đo lead top-k"},
    "train.topk_caption": {
        "en": "Precision@Top k% = share of real converters among the highest-"
              "scoring k% of customers — what your sales team actually calls.",
        "vi": "Precision@Top k% = tỷ lệ khách hàng thực sự chuyển đổi trong nhóm "
              "k% có điểm cao nhất — chính là nhóm đội sales sẽ gọi.",
    },
    "train.eval_complete": {
        "en": "Evaluation complete. Best model: **{best}**. Proceed to **Lead Scoring**.",
        "vi": "Hoàn tất đánh giá. Mô hình tốt nhất: **{best}**. Chuyển sang "
              "**Chấm điểm tiềm năng**.",
    },

    # ---- lead scoring page ------------------------------------------------
    "lead.subtitle": {
        "en": "Rank every customer by predicted probability of accepting a "
              "personal-loan offer.",
        "vi": "Xếp hạng từng khách hàng theo xác suất dự đoán chấp nhận đề nghị "
              "vay cá nhân.",
    },
    "lead.scoring_model": {"en": "Scoring model", "vi": "Mô hình chấm điểm"},
    "lead.best_model_caption": {"en": "Best model: **{best}**", "vi": "Mô hình tốt nhất: **{best}**"},
    "lead.priority_overview": {"en": "Lead priority overview", "vi": "Tổng quan mức ưu tiên"},
    "metric.total_leads": {"en": "Total leads", "vi": "Tổng số khách hàng"},
    "metric.high_priority": {"en": "🟢 High priority", "vi": "🟢 Ưu tiên cao"},
    "metric.medium_priority": {"en": "🟡 Medium priority", "vi": "🟡 Ưu tiên trung bình"},
    "metric.low_priority": {"en": "⚪ Low priority", "vi": "⚪ Ưu tiên thấp"},
    "lead.select_title": {"en": "Select top leads for your campaign", "vi": "Chọn nhóm khách hàng hàng đầu cho chiến dịch"},
    "lead.selection_mode": {"en": "Selection mode", "vi": "Cách chọn"},
    "mode.top5": {"en": "Top 5%", "vi": "Top 5%"},
    "mode.top10": {"en": "Top 10%", "vi": "Top 10%"},
    "mode.top20": {"en": "Top 20%", "vi": "Top 20%"},
    "mode.custom": {"en": "Custom count", "vi": "Số lượng tùy chỉnh"},
    "mode.all": {"en": "All leads", "vi": "Tất cả"},
    "lead.custom_count": {"en": "Custom count", "vi": "Số lượng tùy chỉnh"},
    "metric.selected_leads": {"en": "Selected leads", "vi": "Số KH đã chọn"},
    "metric.converters_captured": {"en": "Real converters captured", "vi": "KH thực sự chuyển đổi bắt được"},
    "metric.pct_converters": {"en": "% of all converters reached", "vi": "% trên tổng KH chuyển đổi"},
    "lead.ranked_list": {"en": "Ranked lead list", "vi": "Danh sách khách hàng xếp hạng"},
    "lead.showing_first": {
        "en": "Showing first 500 of {total:,} selected leads. Use **Export "
              "Results** to download the full list.",
        "vi": "Đang hiển thị 500 trong tổng {total:,} khách hàng đã chọn. Dùng "
              "**Xuất kết quả** để tải toàn bộ danh sách.",
    },
    "lead.success": {
        "en": "Leads scored. See **Customer Insights** for drivers, or **Export "
              "Results** to download.",
        "vi": "Đã chấm điểm. Xem **Phân tích khách hàng** để biết yếu tố ảnh "
              "hưởng, hoặc **Xuất kết quả** để tải về.",
    },

    # ---- insights page ----------------------------------------------------
    "insights.subtitle": {
        "en": "Understand the drivers of conversion and profile your "
              "highest-value leads.",
        "vi": "Hiểu các yếu tố thúc đẩy chuyển đổi và phác hoạ chân dung nhóm "
              "khách hàng giá trị nhất.",
    },
    "insights.open_scoring_info": {
        "en": "Open **Lead Scoring** first to generate the lead table.",
        "vi": "Hãy mở **Chấm điểm tiềm năng** trước để tạo bảng khách hàng.",
    },
    "insights.feature_importance": {"en": "Feature importance", "vi": "Tầm quan trọng của đặc trưng"},
    "insights.model": {"en": "Model", "vi": "Mô hình"},
    "chart.lr_title": {"en": "Coefficient direction & magnitude", "vi": "Chiều & độ lớn của hệ số"},
    "insights.lr_caption": {
        "en": "Positive (green) coefficients push a customer **toward** "
              "accepting a loan; negative (red) push away. Magnitude = relative "
              "influence (features are standardized).",
        "vi": "Hệ số dương (xanh) đẩy khách hàng **về phía** chấp nhận vay; âm "
              "(đỏ) đẩy ra xa. Độ lớn = mức ảnh hưởng tương đối (đặc trưng đã "
              "được chuẩn hóa).",
    },
    "chart.tree_title": {"en": "Relative feature importance", "vi": "Tầm quan trọng tương đối"},
    "insights.tree_caption": {
        "en": "Higher bars contribute more to the model's predictions.",
        "vi": "Cột càng cao thì đóng góp càng nhiều vào dự đoán của mô hình.",
    },
    "insights.high_profile": {"en": "High-priority lead profile", "vi": "Chân dung nhóm ưu tiên cao"},
    "insights.no_high": {
        "en": "No high-priority leads (score ≥ 0.70) in this dataset/model.",
        "vi": "Không có khách hàng ưu tiên cao (điểm ≥ 0.70) với bộ dữ liệu/mô "
              "hình này.",
    },
    "metric.high_leads": {"en": "High-priority leads", "vi": "Số KH ưu tiên cao"},
    "metric.avg_income_high": {"en": "Avg income (high)", "vi": "Thu nhập TB (cao)"},
    "metric.avg_card_high": {"en": "Avg card spend (high)", "vi": "Chi tiêu thẻ TB (cao)"},
    "metric.avg_mortgage_high": {"en": "Avg mortgage (high)", "vi": "Thế chấp TB (cao)"},
    "metric.use_online": {"en": "Use online banking", "vi": "Dùng NH trực tuyến"},
    "metric.hold_cd": {"en": "Hold a CD account", "vi": "Có TK tiền gửi (CD)"},
    "metric.own_cc": {"en": "Own a credit card", "vi": "Sở hữu thẻ tín dụng"},
    "delta.vs_base": {"en": "{v:+.0f}k vs base", "vi": "{v:+.0f}k so với nền"},
    "insights.edu_dist": {
        "en": "**Education distribution (high-priority leads)**",
        "vi": "**Phân phối học vấn (nhóm ưu tiên cao)**",
    },
    "edu.undergrad": {"en": "Undergrad", "vi": "Đại học"},
    "edu.graduate": {"en": "Graduate", "vi": "Sau đại học"},
    "edu.advanced": {"en": "Advanced/Pro", "vi": "Chuyên sâu"},
    "insights.recommendations_title": {"en": "📌 Campaign recommendations", "vi": "📌 Khuyến nghị chiến dịch"},

    # ---- recommendations (generated) -------------------------------------
    "rec.focus_high": {
        "en": "Focus first on the **{n} high-priority leads** (score ≥ "
              "{thr:.2f}) - these convert best.",
        "vi": "Ưu tiên trước **{n} khách hàng ưu tiên cao** (điểm ≥ {thr:.2f}) - "
              "nhóm này chuyển đổi tốt nhất.",
    },
    "rec.personalize": {
        "en": "Use personalized loan offers for high-income, high-card-spend "
              "customers (avg income of top leads ≈ ${income:.0f}k).",
        "vi": "Dùng đề nghị vay cá nhân hoá cho khách hàng thu nhập cao, chi "
              "tiêu thẻ cao (thu nhập TB của nhóm đầu ≈ ${income:.0f}k).",
    },
    "rec.nurture": {
        "en": "Nurture the **{n} medium-priority leads** with follow-up emails "
              "before committing sales effort.",
        "vi": "Chăm sóc **{n} khách hàng ưu tiên trung bình** bằng email theo "
              "dõi trước khi dồn nguồn lực bán hàng.",
    },
    "rec.avoid_low": {
        "en": "Avoid mass marketing to the **{n} low-priority leads** - outreach "
              "cost rarely pays off here.",
        "vi": "Tránh marketing đại trà tới **{n} khách hàng ưu tiên thấp** - chi "
              "phí tiếp cận hiếm khi xứng đáng.",
    },
    "rec.export_crm": {
        "en": "Export the top leads to your CRM and track conversion outcomes.",
        "vi": "Xuất nhóm khách hàng hàng đầu sang CRM và theo dõi kết quả "
              "chuyển đổi.",
    },
    "rec.retrain": {
        "en": "Retrain the model periodically as new campaign results arrive.",
        "vi": "Huấn luyện lại mô hình định kỳ khi có kết quả chiến dịch mới.",
    },

    # ---- export page ------------------------------------------------------
    "export.subtitle": {
        "en": "Download the scored lead list for your CRM or campaign tooling.",
        "vi": "Tải danh sách khách hàng đã chấm điểm cho CRM hoặc công cụ "
              "chiến dịch.",
    },
    "export.what_to_export": {"en": "What to export", "vi": "Nội dung cần xuất"},
    "export.lead_scope": {"en": "Lead scope", "vi": "Phạm vi"},
    "scope.selected": {"en": "Selected top leads", "vi": "Nhóm KH đã chọn"},
    "scope.all": {"en": "All scored customers", "vi": "Tất cả KH đã chấm điểm"},
    "export.exporting_caption": {
        "en": "Exporting **{n:,}** rows using model **{model}**.",
        "vi": "Đang xuất **{n:,}** dòng bằng mô hình **{model}**.",
    },
    "export.download_csv": {"en": "⬇️ Download CSV", "vi": "⬇️ Tải CSV"},
    "export.download_excel": {"en": "⬇️ Download Excel", "vi": "⬇️ Tải Excel"},
    "export.exported_columns": {
        "en": "**Exported columns:** Customer ID · Rank · Lead Score · Priority "
              "· key customer features · Recommended Action.",
        "vi": "**Các cột xuất ra:** Mã KH · Hạng · Điểm tiềm năng · Mức ưu tiên "
              "· các đặc trưng chính · Hành động đề xuất.",
    },
    "export.success": {
        "en": "Ready to download. Hand the list to your sales/CRM team and track "
              "conversions to retrain the model later.",
        "vi": "Sẵn sàng tải về. Chuyển danh sách cho đội sales/CRM và theo dõi "
              "chuyển đổi để huấn luyện lại mô hình sau này.",
    },
}


# ---------------------------------------------------------------------------
# Priority bands, recommended actions, column & feature labels
# Internal canonical values stay in English ("High"/"Medium"/"Low"); these
# maps only affect what the user sees.
# ---------------------------------------------------------------------------
PRIORITY_LABELS = {
    "High": {"en": "High", "vi": "Cao"},
    "Medium": {"en": "Medium", "vi": "Trung bình"},
    "Low": {"en": "Low", "vi": "Thấp"},
}

ACTION_LABELS = {
    "High": {"en": "Contact now - personalized loan offer",
             "vi": "Liên hệ ngay - đề nghị vay cá nhân hoá"},
    "Medium": {"en": "Nurture - follow-up email / call",
               "vi": "Chăm sóc - email/gọi theo dõi"},
    "Low": {"en": "Deprioritize - no direct outreach",
            "vi": "Hạ ưu tiên - không tiếp cận trực tiếp"},
}

HEADER_LABELS = {
    "Rank": {"en": "Rank", "vi": "Hạng"},
    "Customer ID": {"en": "Customer ID", "vi": "Mã KH"},
    "Lead Score": {"en": "Lead Score", "vi": "Điểm tiềm năng"},
    "Priority": {"en": "Priority", "vi": "Mức ưu tiên"},
    "Recommended Action": {"en": "Recommended Action", "vi": "Hành động đề xuất"},
    "Age": {"en": "Age", "vi": "Tuổi"},
    "Income": {"en": "Income", "vi": "Thu nhập"},
    "Family": {"en": "Family", "vi": "Quy mô GĐ"},
    "CCAvg": {"en": "CCAvg", "vi": "Chi tiêu thẻ TB"},
    "Education": {"en": "Education", "vi": "Học vấn"},
    "Mortgage": {"en": "Mortgage", "vi": "Thế chấp"},
    "CD Account": {"en": "CD Account", "vi": "TK tiền gửi"},
    "Online": {"en": "Online", "vi": "NH trực tuyến"},
    "CreditCard": {"en": "CreditCard", "vi": "Thẻ tín dụng"},
    "Experience": {"en": "Experience", "vi": "Kinh nghiệm"},
    "Securities Account": {"en": "Securities Account", "vi": "TK chứng khoán"},
    "Actual (Personal Loan)": {"en": "Actual (Personal Loan)", "vi": "Thực tế (Vay)"},
}

FEATURE_LABELS_VI = {
    "Age": "Tuổi",
    "Experience": "Kinh nghiệm (năm)",
    "Income": "Thu nhập (k$)",
    "Family": "Quy mô gia đình",
    "CCAvg": "Chi tiêu thẻ TB (k$)",
    "Education": "Trình độ học vấn",
    "Mortgage": "Giá trị thế chấp (k$)",
    "Securities Account": "TK chứng khoán",
    "CD Account": "TK tiền gửi (CD)",
    "Online": "Ngân hàng trực tuyến",
    "CreditCard": "Sở hữu thẻ tín dụng",
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Translate ``key`` into ``lang``; falls back to English then the key."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def priority_label(band: str, lang: str = DEFAULT_LANG) -> str:
    return PRIORITY_LABELS.get(band, {}).get(lang, band)


def action_label(band: str, lang: str = DEFAULT_LANG) -> str:
    return ACTION_LABELS.get(band, {}).get(lang, band)


def header_label(col: str, lang: str = DEFAULT_LANG) -> str:
    return HEADER_LABELS.get(col, {}).get(lang, col)


def feature_label(col: str, lang: str = DEFAULT_LANG) -> str:
    """Human-friendly feature label for charts."""
    if lang == "vi":
        return FEATURE_LABELS_VI.get(col, col)
    from .config import FEATURE_LABELS  # local import to avoid cycle at import time
    return FEATURE_LABELS.get(col, col)


def priority_color_map(lang: str, colors: dict) -> dict:
    """Return {localized priority label: color} for table styling/charts."""
    from .config import PRIORITY_COLORS
    return {priority_label(band, lang): PRIORITY_COLORS[band]
            for band in PRIORITY_COLORS}
