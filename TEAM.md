# Thông tin nhóm

- Tên nhóm: xanh đỏ
- Mã thành viên trong phân công gốc: 084, 117, 133, 150
- Mã có nhãn đã nộp trong gói này: 084, 117, 133
- Thành viên không chờ trong lượt phân tích hiện tại: 150, theo yêu cầu người điều phối
- Người điều phối: 117
- Người review bản cuối theo phân công: 133; chưa ghi nhận nghiệm thu nhãn cuối toàn lô
- Commit chốt bài: xem commit chứa submission/SUBMISSION_STATUS.md trên nhánh guideline-ca-nhan

## Kết quả tóm tắt

- Lượt gán hoàn tất / được giao: 60/80 theo bảng gốc; 40/40 ảnh có ít nhất một nhãn, 20/40 ảnh đủ hai nhãn.
- IAA trước calibration trên tập con: 214 cặp box của 20 ảnh, IoU TB 0,944, đồng thuận lớp 97,7%; không phải chỉ số cho toàn bộ lô.
- Số ảnh cần calibration trong tập con: 19/20; 339 dòng cần xem, chưa phải số vật lỗi đã xác nhận.
- Vòng QC toàn lô: chưa khởi tạo, đã duyệt 0/40 ảnh theo vòng QC; riêng Task 117 đã được AI xem lại 20 ảnh và completed trên CVAT.
- Tỉ lệ lỗi theo ảnh / đối tượng: N/A vì chưa có vòng QC nhãn cuối; không báo 0%.
- **Quyết định: Hold** — thiếu 20 lượt gán và bằng chứng calibration/QC. Nộp bằng chứng hiện có theo SUBMISSION.md.

Chi tiết: submission/SUBMISSION_STATUS.md và submission/qc/QC_REPORT.md. Ghi công ảnh giữ nguyên ở data/ATTRIBUTION.csv.
