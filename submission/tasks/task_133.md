# Task 133 — Day07_133_v1.0

- Người nhận: `133`.
- Guideline: `submission/guidelines/guideline_v1.0_agreed.md`, v1.0 đã khóa theo yêu cầu người điều phối.
- CVAT: mỗi thành viên dùng CVAT local riêng tại `http://localhost:8080/` trên máy mình.
- Project cần tạo: `Day07_GuidelineQC_v1.0`; Labels → Raw dùng `cvat/labels_generated.json`.
- Tên Task: `Day07_133_v1.0`; tải đúng 20 ảnh trong `work/133/images/` hoặc `133.zip`.
- Đầu ra: `submission/labels/133.json`, COCO 1.0, tắt Save images.
- Trạng thái: đã phân công; chưa ghi nhận hoàn thành gán nhãn.

## Các bước thực hiện

1. Đọc guideline đã khóa, giữ nguyên taxonomy khi gán.
2. Tạo Project và Task trên CVAT local của chính mình; không dùng Task người khác để tham khảo nhãn.
3. Kiểm đúng 20 frame và danh sách ảnh dưới đây, kể cả ảnh không có vật hợp lệ.
4. Tự vẽ Rectangle và điền đủ occluded_level, truncated, can_review. Ca chưa chắc theo R-10, giữ để calibration.
5. Export JSON COCO và chạy `python scripts/validate_labels.py submission/labels/133.json`.
6. Gửi riêng kết quả theo kênh nhóm đã thống nhất; cập nhật ghi chú cá nhân của mình, không xem nhãn nhau trước khi tất cả đã nộp.

## 20 ảnh được giao

- [ ] `img_001.jpg`
- [ ] `img_004.jpg`
- [ ] `img_005.jpg`
- [ ] `img_007.jpg`
- [ ] `img_009.jpg`
- [ ] `img_011.jpg`
- [ ] `img_014.jpg`
- [ ] `img_016.jpg`
- [ ] `img_018.jpg`
- [ ] `img_019.jpg`
- [ ] `img_021.jpg`
- [ ] `img_024.jpg`
- [ ] `img_025.jpg`
- [ ] `img_027.jpg`
- [ ] `img_030.jpg`
- [ ] `img_031.jpg`
- [ ] `img_034.jpg`
- [ ] `img_035.jpg`
- [ ] `img_038.jpg`
- [ ] `img_040.jpg`
