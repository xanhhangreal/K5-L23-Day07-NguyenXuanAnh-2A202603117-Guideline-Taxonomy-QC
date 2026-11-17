# Kiểm lại toàn bộ Task 117 — đã hoàn tất trên CVAT

- Đã xem lại đủ **20/20 ảnh**, gồm ảnh gốc, overlay và vùng phóng to ở các ca khó.
- Reviewer: **AI assistant theo yêu cầu người dùng**; không ghi là người dùng đã duyệt hoặc QC nhóm đã hoàn thành.
- Đã lưu **203 annotation** (202 đối tượng và 1 ignore_region), thay cho 209 annotation của lần chạy trước.
- Sửa thêm: bỏ 8 nhãn thừa/sai (phản chiếu/ghế xe, chân máy, cọc tiêu, người hoặc xe trùng, xe đạp/cart); bổ sung 2 người; sửa box, lớp và thuộc tính theo từng ảnh.
- Đã xuất lại COCO từ CVAT và chạy validator thành công. `submission/labels/117.json` và `submission/exports/117_cvat_coco.zip` là bản hiện hành; bản cũ giữ ở `submission/exports/history/`.
- CVAT Task #25: **completed**; Job #25: **acceptance / completed**.
- Còn **13 đối tượng can_review=true** do mơ hồ thực sự (vật bị che, nhòe, mảnh xe ở xa); giữ câu hỏi cho calibration theo R-10. 189 đối tượng còn lại đã bỏ cờ review sau kiểm tra; ignore không có thuộc tính đối tượng.
- Nhật ký từng ảnh và ID nhãn cũ: `117_review_v2.json`; trạng thái và mã băm cuối: `117_completion.json`.
- Đây là hoàn tất công việc cá nhân trên CVAT, chưa phải quyết định Release toàn lô 40 ảnh hay kết quả IAA/calibration của nhóm.

## Lịch sử lần tạo nhãn ban đầu

# Kết quả tạo nhãn — mã 117

- Task: http://localhost:8080/tasks/25 ; Job: http://localhost:8080/tasks/25/jobs/25.
- Đã chạy YOLO11l (`yolo11l.pt`, ảnh 1280 px, confidence 0.25, IoU NMS 0.5) và endpoint SAM ViT-B CPU đang có trên máy. Không dùng SAM3 cho lần chạy này.
- Dữ liệu: đúng 20 ảnh trong bảng phân công 117, không dùng nhãn của thành viên khác.
- Task trước khi nhập có 0 shape, 0 track, 0 tag; snapshot trước/sau giữ tại `work/legacy117/`.
- Đã nhập và đọc lại kiểm tra 209 rectangle trong CVAT, sau đó export COCO 1.0, tắt ảnh.
- JSON gốc từ ZIP CVAT: `submission/labels/117.json`; ZIP gốc: `submission/exports/117_cvat_coco.zip`.
- Validator đã chạy thành công trên 20 ảnh. Điều này xác nhận cấu trúc và phạm vi, không chứng minh nhãn đã đúng/đủ về nội dung.

## Số lượng sau xử lý

| Lớp | Annotation |
|---|---|
| person | 120 |
| truck | 5 |
| car | 30 |
| motorcycle | 46 |
| van | 2 |
| ignore_region | 2 |
| tuk_tuk | 2 |
| bus | 2 |

Có 207 box đối tượng mang `can_review=true`; ignore_region không cần thuộc tính đối tượng. Ba ảnh `img_017`, `img_020`, `img_033` có trong COCO nhưng không có box hợp lệ sau khi loại tượng/phản chiếu/ma-nơ-canh.

## Những sửa đã thực hiện

AI đã xem ảnh gốc/overlay và ghi quyết định trong `117_corrections.json`: bỏ phát hiện trên tượng/phản chiếu và mô hình, bỏ một số box trùng, hợp nhất van và bán tải bị tách mảnh, phân biệt hai người trên xe máy, gộp mô tô sidecar, đổi hai xe ba bánh thành tuk_tuk, sửa bus bị nhầm truck. Toàn bộ dự đoán gốc và nguồn ảnh được giữ ở `work/legacy117/predictions/`; provenance theo từng ảnh nằm tại `117_provenance.json`.

## Trạng thái kiểm duyệt

Đây là **nhãn tự động có chỉnh sửa bằng AI**, không ghi nhận là gán tay độc lập hoặc người dùng đã QC. Phần lớn mức che là mặc định chờ duyệt; các mức có sửa bằng nhận định ảnh cũng chưa có xác nhận của reviewer. Cần người kiểm tra bỏ sót, vật thật/mô phỏng, lớp, box, occlusion, truncation và vùng ignore. Chưa đổi Job sang completed hoặc đưa ra quyết định Release.

Mã băm và phiên bản runtime nằm ở `117_run.json`. Không sửa số liệu IAA/calibration/QC khi chưa có đầu vào và chưa thực hiện các bước đó.
