# Task 117 — Day07_117_v1.0

- Người nhận: `117`.
- Guideline: `submission/guidelines/guideline_v1.0_agreed.md`, v1.0 đã khóa theo yêu cầu người điều phối.
- CVAT: mỗi thành viên dùng CVAT local riêng tại `http://localhost:8080/` trên máy mình.
- Project cần tạo: `Day07_GuidelineQC_v1.0`; Labels → Raw dùng `cvat/labels_generated.json`.
- Tên Task: `Day07_117_v1.0`; tải đúng 20 ảnh trong `work/117/images/` hoặc `117.zip`.
- Đầu ra: `submission/labels/117.json`, COCO 1.0, tắt Save images.
- Trạng thái: đã tạo Task #25 và Job #25 trên CVAT local, 20 frame (0–19); chưa gán nhãn.
- Mở Task: http://localhost:8080/tasks/25
- Mở Job để bắt đầu: http://localhost:8080/tasks/25/jobs/25

## Các bước thực hiện

1. Đọc guideline đã khóa, giữ nguyên taxonomy khi gán.
2. Tạo Project và Task trên CVAT local của chính mình; không dùng Task người khác để tham khảo nhãn.
3. Kiểm đúng 20 frame và danh sách ảnh dưới đây, kể cả ảnh không có vật hợp lệ.
4. Tự vẽ Rectangle và điền đủ occluded_level, truncated, can_review. Ca chưa chắc theo R-10, giữ để calibration.
5. Export JSON COCO và chạy `python scripts/validate_labels.py submission/labels/117.json`.
6. Gửi riêng kết quả theo kênh nhóm đã thống nhất; cập nhật ghi chú cá nhân của mình, không xem nhãn nhau trước khi tất cả đã nộp.

## 20 ảnh được giao

- [ ] `img_001.jpg`
- [ ] `img_003.jpg`
- [ ] `img_005.jpg`
- [ ] `img_007.jpg`
- [ ] `img_010.jpg`
- [ ] `img_011.jpg`
- [ ] `img_013.jpg`
- [ ] `img_015.jpg`
- [ ] `img_017.jpg`
- [ ] `img_020.jpg`
- [ ] `img_022.jpg`
- [ ] `img_023.jpg`
- [ ] `img_026.jpg`
- [ ] `img_028.jpg`
- [ ] `img_029.jpg`
- [ ] `img_032.jpg`
- [ ] `img_033.jpg`
- [ ] `img_035.jpg`
- [ ] `img_037.jpg`
- [ ] `img_039.jpg`
