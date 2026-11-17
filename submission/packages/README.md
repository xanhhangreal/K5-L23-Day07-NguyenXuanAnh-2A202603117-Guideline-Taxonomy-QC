# Gói gán nhãn Day07 — v1.0

Guideline chính thức: [guideline_v1.0_agreed.md](../guidelines/guideline_v1.0_agreed.md). Bản v1.0 đã khóa theo chỉ đạo người điều phối, tổng hợp từ 117/133/150; không chờ guideline 084. Cả bốn thành viên vẫn tham gia gán.

Mỗi người nhận đúng 20 ảnh. Mỗi ảnh trong bộ 40 ảnh có hai người gán độc lập. Tải đúng gói của mình; mỗi người dùng CVAT local trên máy riêng.

| Mã | Gói ZIP | Phiếu task | Tên Task CVAT | JSON nộp |
|---|---|---|---|---|
| 084 | [handoff_084_v1.0.zip](handoff_084_v1.0.zip) | [Task 084](../tasks/task_084.md) | `Day07_084_v1.0` | `submission/labels/084.json` |
| 117 | [handoff_117_v1.0.zip](handoff_117_v1.0.zip) | [Task 117](../tasks/task_117.md) | `Day07_117_v1.0` | `submission/labels/117.json` |
| 133 | [handoff_133_v1.0.zip](handoff_133_v1.0.zip) | [Task 133](../tasks/task_133.md) | `Day07_133_v1.0` | `submission/labels/133.json` |
| 150 | [handoff_150_v1.0.zip](handoff_150_v1.0.zip) | [Task 150](../tasks/task_150.md) | `Day07_150_v1.0` | `submission/labels/150.json` |

## Cách dùng

1. Mở file ZIP trên GitHub rồi chọn Download raw file, hoặc tải bằng link người điều phối gửi. Giải nén vào thư mục repo của mình, giữ cấu trúc đường dẫn.
2. Đọc guideline chính thức và phiếu task. ZIP có guideline, taxonomy, bộ nhãn CVAT, hồ sơ khóa, bảng/danh sách phân công, hướng dẫn và 20 ảnh theo mã.
3. Trên CVAT local của mình, tạo Project `Day07_GuidelineQC_v1.0`. Trong Labels → Raw, dán `cvat/labels_generated.json`, Save rồi Submit.
4. Tạo Task theo tên trên bảng. Chọn 20 ảnh trong `work/<mã>/images/` sau khi giải nén. **Không tải toàn bộ handoff ZIP làm dataset**, vì gói chứa cả tài liệu và JSON.
5. Tự gán theo v1.0 đã khóa; export COCO 1.0, tắt Save images. Chạy validator trong repo rồi gửi riêng JSON theo mã. Không xem nhãn người khác trước khi tất cả đã nộp.

Chi tiết: [PHASE3_HANDOFF.md](../../docs/PHASE3_HANDOFF.md). Bảng phân công chung: [assignment.csv](../qc/assignment.csv). SHA-256 các ZIP: [SHA256SUMS.txt](SHA256SUMS.txt).

Task #25 của 117 đã được tạo trên máy 117. Các URL localhost và ID này chỉ áp dụng tại máy đó; mỗi thành viên tự tạo Task trên máy riêng, ID có thể khác.

## Bàn giao bổ sung 17/11/2026 — Hold

Đã nhận 084/117/133, không chờ 150. Toàn lô hiện 60/80 lượt; IAA chỉ tính trên 20 ảnh đủ cặp. [Trạng thái và phần còn thiếu](../SUBMISSION_STATUS.md).

- [ZIP báo cáo IAA một phần, mẫu calibration và 19 ảnh overlay](partial_IAA_084_117_133_2026-11-17.zip).
- [084: 7 ảnh bổ sung](supplement_084_2026-11-17.zip).
- [117: 7 ảnh bổ sung](supplement_117_2026-11-17.zip).
- [133: 6 ảnh bổ sung](supplement_133_2026-11-17.zip).
- [Phân công bổ sung](../qc/partial_2026-11-17_084_117_133/supplemental_assignments.csv).

Các ZIP bổ sung chỉ có ảnh được giao, cấu hình và hướng dẫn, không có nhãn người đang giữ ảnh đó. Đây là việc mới cần thực hiện, chưa tính là lượt gán hoàn thành. Giữ độc lập trước khi tập hợp.
