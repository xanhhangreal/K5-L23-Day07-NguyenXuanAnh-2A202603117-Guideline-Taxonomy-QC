# IAA một phần — bỏ qua thành viên 150

**Trạng thái toàn lô: HOLD.** Theo yêu cầu người dùng, không chờ 150 để phân tích phần đã có. Không thay bảng phân công gốc, không tạo nhãn thay người chưa nộp.

## Dữ liệu đã nhận

- 117: 20 ảnh, 203 annotation; nhãn tự động và AI đã xem lại.
- 084: 20 ảnh, 274 annotation, import nguyên byte từ ZIP mới.
- 133: 20 ảnh, 281 annotation, import nguyên byte từ ZIP mới.
- 150: chưa có nhãn, được loại khỏi lượt phân tích này.
- Validator của ba file đều chạy thành công. Bản 133 có cảnh báo vật nhỏ dưới 20 px cần đối chiếu guideline; không tự sửa nhãn độc lập đã nộp.

## Phạm vi và mẫu số

- Toàn lô có dữ liệu cho **40/40 ảnh**, nhưng mới đủ **60/80 lượt gán (75%)**.
- **20/40 ảnh** có hai người đã nộp: dùng để tính IAA bên dưới.
- **20/40 ảnh** mới có một người: không đưa vào phép đo đồng thuận.
- Con số 40/40 trong iaa_summary.md là 40 lượt của **tập con 20 ảnh**, không phải toàn lô 40 ảnh.

## Kết quả trên 20 ảnh đủ cặp

- Cặp box ghép được: **214** (ghép 1–1, không phân biệt lớp, IoU ≥ 0,5).
- IoU trung bình: **0.944**; đồng thuận lớp: **97.7%**.
- Box chưa ghép ở hai phía cộng theo từng cặp: **20/36**.
- Ca bất đồng/cần xem: **339**, trên **19/20 ảnh**.
- Kết quả này là đồng thuận của các nguồn đã nộp, không phải độ chính xác so với ground truth; 117 có sử dụng mô hình và AI.

Chi tiết: `iaa_summary.md`, `calibration_candidates.csv`, `image_scores.csv`. `consensus_draft.json` chỉ là nháp tự động của 20 ảnh trong phạm vi này, chưa là nhãn cuối.

## Làm tiếp khi không dùng bài của 150

Đã lập `supplemental_assignments.csv` cho **20 lượt gán bổ sung độc lập**, giao cho người khác người đã gán ảnh đó. Tải dự kiến sau bổ sung: 084 = 27, 117 = 27, 133 = 26 ảnh. Đây là phân công mới cần thực hiện, không phải kết quả đã có. Mỗi người không được xem nhãn hiện có của ảnh bổ sung trước khi gán.

Có thể mở overlay trong `work/partial_iaa_2026-11-17_084_117_133/work/viz` để calibration các ảnh đã đủ cặp. Giữ nguyên nhãn độc lập ban đầu. Chưa điền quyết định calibration, chưa tạo nhãn cuối hoặc báo cáo Release toàn lô.

Nguồn import và SHA-256 ZIP gốc: `../imports/2026-11-17/import_manifest.json`. Phạm vi và mã băm đầu vào: `SCOPE.json`.
