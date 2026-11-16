# Đối chiếu guideline cá nhân — Pha 2

- Nguồn: nhánh `guideline-ca-nhan`, commit `2a04969`.
- Đã nhận: `117`, `133`, `150`.
- Không chờ guideline `084`: người điều phối yêu cầu bỏ qua bản này để chốt v1.0; `084` vẫn tham gia gán nhãn.
- Trạng thái: đã khóa v1.0 theo chỉ đạo trong chat ngày 16/11/2026. Không ghi nhận thay cho cuộc họp hoặc phiếu duyệt ảnh chưa thực hiện.
- Giữ nguyên ba bản cá nhân để đối chiếu. Rule ID của bản nhóm theo hệ thống mới trong `guideline_v1.0_agreed.md`; không dùng lẫn với Rule ID bản cá nhân.

## 1. Những điểm đã giống nhau trong ba bản

| Chủ đề | Nội dung cùng hướng |
|---|---|
| Taxonomy | Bổ sung `bus`, `tuk_tuk`; người và phương tiện là lớp dự đoán, che khuất/cắt mép/review là thuộc tính. |
| Người trên phương tiện | Tách từng người và xe, không gom cả cụm thành một box. |
| Xe chở xe | Tách xe vận chuyển và từng xe thật được chở đủ điều kiện. |
| Phạm vi | Không gán xe đạp, xích lô không động cơ; người trên đó vẫn xét riêng. |
| Vật mô phỏng | Loại tượng, ma-nơ-canh, hình in, đồ chơi và phản chiếu; cần phân biệt với vật thật nhìn xuyên kính. |
| Box | Ôm phần nhìn thấy, không dựng phần bị khuất. |
| Che khuất | Mức 0%, nhẹ tới 30%, trung bình tới 70%, nặng trên 70% nhưng còn nhận dạng được. |
| QC | Giữ ngưỡng lab, duyệt toàn lô, báo số lượng và mẫu số, giữ IAA trước calibration. |

Bản nhóm dùng ba nguồn đã nhận. Việc khóa dựa trên chỉ đạo người điều phối, không ghi là cả bốn thành viên đã nộp hoặc đã xác nhận riêng.

## 2. Khác biệt và cách xử lý được chọn cho v1.0

| Mã | Chủ đề / ảnh | 117 | 133 | 150 | Cách xử lý trong bản tổng hợp | Cách áp dụng khi gán |
|---|---|---|---|---|---|---|
| P2-01 | Mô tô sidecar, `img_022.jpg` | Định nghĩa motorcycle hai bánh, chưa có ngoại lệ. | Có tính sidecar vào motorcycle. | Một motorcycle gồm cả sidecar gắn liền. | R-11: bổ sung ngoại lệ sidecar, một box cho tổ hợp gắn liền. | Áp dụng R-11: một motorcycle cho mô tô và sidecar gắn liền. |
| P2-02 | Predator, `img_011.jpg` | Liệt kê trong nhóm tượng. | Person nếu là người thật hóa trang, có review. | Cần xác định người thật hay vật mô phỏng. | R-07: không kết luận bản chất chỉ từ tên ảnh; người thật hóa trang vẫn là person, tượng thì loại. | Tự xét trên ảnh; chưa chắc theo R-10, giữ để calibration. |
| P2-03 | Xe diễu hành, `img_019.jpg` | Chưa nêu riêng. | Loại xe mô hình diễu hành. | Không loại xe thật chỉ do thiết kế lạ; cần review. | R-07: xe thật hóa trang vẫn xét, mô hình thì loại; ca chưa chắc chuyển R-10. | Xe thật hóa trang vẫn xét; mô hình thì loại; chưa chắc theo R-10. |
| P2-04 | Vỏ xe trên nóc, `img_024.jpg` | Chưa nêu riêng. | Loại vỏ xe cắt rời. | Review bản chất vật trên nóc. | R-12: hàng/vỏ xe rời không là xe độc lập; xe thật nguyên chiếc được chở theo R-06. | Vỏ rời thì loại, xe thật được chở thì xét; chưa chắc theo R-10. |
| P2-05 | Hàng hóa, `img_029.jpg`, `img_035.jpg` | Chưa tách quy tắc hàng; img_029 được xếp nhóm xe không động cơ. | Không bao hàng; mô tả img_029 là bao tải. | Không bao hàng; mô tả img_029 là thanh dài. | R-12: không bao hàng rời; không đưa mô tả mâu thuẫn vào bản nhóm như sự thật. | Chọn lớp từ ảnh thật, không dựa mô tả mâu thuẫn; chưa chắc theo R-10. |
| P2-06 | Bán tải nắp cao, `img_037.jpg` | Truck nếu rõ kết cấu. | Truck hoặc van, chờ chốt. | Truck nếu rõ kết cấu. | R-01: chọn theo kết cấu bán tải, không theo riêng nắp thùng. | Theo R-01: kết cấu bán tải là truck; chưa rõ thì review. |
| P2-07 | Ranh giới mức che | (0,30], (30,70], >70%. | 1–30, 31–70; nêu trường hợp >90% không nhận dạng. | (0,30], (30,70], >70%. | R-02: dùng khoảng liên tục để không bỏ trống 0–1% và 30–31%; không đặt ngưỡng loại 90% mới. | Dùng khoảng liên tục; không gán khi không nhận dạng được bất kể tỷ lệ. |
| P2-08 | Vật nhỏ đơn lẻ | Ignore gọn vùng vật <20 px. | Không gán riêng; mô tả ignore chủ yếu cho cụm. | Ignore gọn vùng vật <20 px. | R-09: ignore cho vật mục tiêu nhỏ hoặc cụm không tách được; giữ vật lớn rõ bên ngoài. | Áp dụng R-09, ignore gọn phần không đủ điều kiện, không phủ vật lớn rõ. |
| P2-09 | Xe buýt và van | Theo kết cấu, không theo riêng kích thước. | Có ngưỡng số ghế >16. | Không suy đoán số ghế. | R-01: theo đặc điểm nhìn thấy, không suy ra số ghế không quan sát được. | Theo kết cấu nhìn thấy; không đoán số ghế. |
| P2-10 | Mờ, tọa độ và phụ kiện | Chưa nêu riêng. | Chưa nêu đầy đủ. | Có quy tắc blur, XYXY/XYWH và phụ kiện. | R-03/R-13: bổ sung để làm rõ cách thao tác, không đổi ngưỡng lab. | Áp dụng R-03/R-13; không đặt box đoán khi không xác định được ranh giới. |

## 3. Đầu ra đã chốt

- `guideline_v1.0_agreed.md`: đã khóa, nguồn 117/133/150, không chờ 084.
- `submission/taxonomy.json`: v1.0, bảy lớp đối tượng và ignore; giữ nguyên ba thuộc tính và tám ngưỡng rules của lab.
- `cvat/labels_generated.json`: cấu hình dùng để tạo Project CVAT.
- `submission/qc/assignment.csv`: 40 ảnh, mỗi ảnh hai người, tổng 80 lượt; bốn mã 084/117/133/150, mỗi người 20 ảnh.
- `submission/tasks/task_<mã>.md` và `task_board.csv`: phiếu và bảng theo dõi phân công; trạng thái sẵn sàng tạo CVAT, không phải nhãn đã hoàn thành.
- `guideline_v1.0_lock.json`: dấu thời gian và SHA-256 cho các file đã khóa.

## 4. Thực hiện pha 3

- [x] Khóa guideline và taxonomy theo chỉ đạo người điều phối; không sửa các bản cá nhân.
- [x] Chốt sidecar, hàng rời, kết cấu bán tải, mức che, vùng ignore và xe hóa trang theo R-01–R-13.
- [x] Với các ca chưa xác định được bản chất trên ảnh, chốt thủ tục R-10: tự gán có căn cứ và can_review, hoặc ghi vấn đề cấp ảnh; giữ để calibration. Chưa ghi rằng ca đã được duyệt ảnh.
- [x] Phân công bốn thành viên, mỗi người 20 ảnh; chuẩn bị ZIP riêng và phiếu task.
- [ ] Tạo Project và bốn Task thực tế trong CVAT theo `docs/PHASE3_HANDOFF.md`.
- [ ] Thành viên gán độc lập, export COCO, chạy validator và gửi riêng.
- [ ] Khi đủ bốn JSON, kiểm toàn bộ rồi chạy IAA; không điền số liệu trước khi có nhãn.

Bỏ qua guideline 084 ở bước khóa không tạo ra file cá nhân thay cho thành viên đó. Việc thiếu guideline cá nhân vẫn được ghi đúng thực tế trong hồ sơ nộp bài.
