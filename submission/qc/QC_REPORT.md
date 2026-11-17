# Báo cáo QC — nhóm xanh đỏ — Hold

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: bàn giao bằng chứng hiện có của Day07, chưa nghiệm thu nhãn cuối; chỉ số IAA tính trên tập con 20 ảnh đủ hai lượt gán.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh starter repo, giữ nguyên `data/ATTRIBUTION.csv` và `data/README.md`.
- Manifest và checksum nhãn cuối: chưa có batch_manifest.json hoặc nhãn calibrated cuối. Mã băm đầu vào, file bàn giao và export 117 được ghi ở submission_manifest.json; đây không phải manifest nghiệm thu nhãn cuối.
- Guideline và taxonomy khi gán / khi bàn giao: v1.0 đã khóa, giữ nguyên tám ngưỡng rules. Chưa có v1.1 calibrated hoặc quyết định đổi nghĩa quy tắc đã được nhóm xác nhận.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 60/80 lượt theo bảng gốc; 40/40 ảnh có ít nhất một file nhãn; 20/40 ảnh có đủ hai người. Đã nhận 084, 117, 133; không chờ 150 theo yêu cầu người điều phối.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 214 cặp ghép trên 20 ảnh đủ cặp; IoU TB 0,944 và cùng lớp 97,7%. Không ngoại suy sang 20 ảnh chỉ có một lượt gán. Đồng thuận mức che 37,9%; cùng truncated 92,1%.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 20/36 box chưa ghép theo hai phía tổng hợp các cặp; 0 box loại do cả hai cùng ignore; 21 ca bất đồng vùng ignore. Có 339 dòng cần xem trên 19 ảnh, không phải 339 vật lỗi đã được xác nhận.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: chưa có bằng chứng đối chiếu ca tham chiếu của coach. Nguồn 117 dùng YOLO + SAM ViT-B và AI; ghi chú 133 cũng nêu dùng pipeline này, nên đồng thuận cao không chứng minh nhãn đúng thực tế.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: chưa chốt calibration nhóm. File partial_2026-11-17_084_117_133/calibration_decisions_TEMPLATE.csv có 339 case_id và các cột quyết định để trống; không phải nhật ký quyết định đã duyệt. Việc AI kiểm Task 117 riêng được ghi ở ../automation/117_review_v2.json, không thay cho calibration nhóm.
- Tác động v1.1 lên nhãn và ảnh: chưa thực hiện, không tạo giả guideline_v1.1_calibrated.md hay guideline_change.json.
- Tham chiếu bằng chứng khi Rework: chưa có vòng QC toàn lô hoặc quyết định Rework. Có kế hoạch 20 lượt bổ sung độc lập tại partial_2026-11-17_084_117_133/supplemental_assignments.csv, gồm 084: 7, 117: 7, 133: 6 ảnh.

## 4. Kết quả duyệt

- Vòng QC: chưa khởi tạo vì chưa đủ lượt gán, calibration và nhãn cuối toàn lô.
- Người review và ngày: AI assistant tổng hợp hồ sơ ngày 17/11/2026 theo yêu cầu người điều phối; chưa ghi nhận reviewer người thật nghiệm thu toàn lô.
- Đã duyệt / cả lô: 0/40 ảnh trong vòng QC toàn lô. Riêng Task 117 đã được AI xem lại 20/20 ảnh và completed trên CVAT; không tính thành nghiệm thu cả nhóm.
- Ảnh lỗi / ảnh đã duyệt: N/A vì chưa có mẫu số ảnh đã duyệt trong vòng QC toàn lô; không kết luận 0% lỗi.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: N/A, chưa có phiếu QC toàn lô.
- Vật bỏ sót, ảnh và vùng: chưa có xác nhận QC. Các ca chỉ một phía gán nằm trong calibration_candidates.csv; cần xem ảnh mới kết luận bỏ sót hay gán thừa.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: ưu tiên img_021, img_030, img_025, img_011, img_005 theo image_scores.csv. Chưa khẳng định lỗi hệ thống đã được nhóm chốt.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: script chặn thiếu 20 lượt gán của 150; box trên tượng/phản chiếu hoặc vật cả hai cùng bỏ sót cần đối chiếu ảnh và guideline.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: thiếu 20 lượt gán độc lập, chưa có calibration và QC nhãn cuối. Bàn giao cho coach/nhóm xem bằng chứng và tiếp tục xử lý; không dùng gói này như nhãn đã Release cho huấn luyện.
- Nếu còn việc: 084/117/133 thực hiện lượt bổ sung theo gói task mới, người điều phối cập nhật phân công có truy vết và chạy lại IAA toàn lô. Nhóm chốt calibration, xuất nhãn cuối, reviewer duyệt đủ 40 ảnh và chạy lại check_submission.py. Mỗi người bổ sung guideline/ghi chú cá nhân còn thiếu bằng nội dung thực tế của mình.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: case C001 trong partial_2026-11-17_084_117_133/calibration_candidates.csv trỏ img_001.jpg và cặp 117–133, nhãn nguồn trong input_subset/labels/. Đối chiếu ảnh data/images/img_001.jpg, R-01/R-03 trong guideline v1.0 và overlay trong gói IAA; chưa ghi nhận người ngoài nhóm đã kiểm ngược.
