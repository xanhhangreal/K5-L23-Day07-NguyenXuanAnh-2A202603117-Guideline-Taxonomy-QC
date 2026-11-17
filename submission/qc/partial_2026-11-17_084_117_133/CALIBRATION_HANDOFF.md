# Chuẩn bị calibration — phạm vi 20 ảnh đủ cặp

Toàn lô vẫn **HOLD vì mới có 60/80 lượt gán**. Chỉ số dưới đây chỉ thuộc 20 ảnh có đủ hai người đã nộp; không dùng để quyết định Release toàn lô.

## So sánh từng cặp

| Cặp thành viên | Ảnh chung | Box ghép được | IoU TB | Cùng lớp | Cùng mức che |
|---|---|---|---|---|---|
| 084–117 | 6 | 33 | 0.923 | 93.9% | 51.5% |
| 084–133 | 9 | 131 | 0.941 | 97.7% | 38.2% |
| 117–133 | 5 | 50 | 0.966 | 100.0% | 28.0% |

Tổng IoU/lớp đạt ngưỡng không có nghĩa mọi cặp đều đạt: cặp 084–117 chỉ cùng lớp 93,9%, dưới ngưỡng 95%. Đồng thuận mức che thấp ở cả ba cặp là điểm cần bàn thống nhất trước khi sửa hàng loạt.

## Thứ tự xem đề nghị

| Ảnh | Ca cần xem | Điểm ưu tiên của script |
|---|---|---|
| img_021.jpg | 121 | 122 |
| img_030.jpg | 32 | 46 |
| img_025.jpg | 29 | 32 |
| img_011.jpg | 25 | 31 |
| img_005.jpg | 19 | 24 |
| img_035.jpg | 17 | 21 |
| img_039.jpg | 18 | 20 |
| img_031.jpg | 16 | 16 |

Có 135 ca sai thuộc tính, 115 cờ can_review, 47 ca chỉ một phía gán, 21 bất đồng ignore, 16 ca IoU thấp, 5 ca sai lớp. Một vật có thể tạo nhiều ca; 339 dòng không có nghĩa là 339 vật lỗi đã được xác nhận.

## Cách xử lý

1. Mở overlay tương ứng trong `work/partial_iaa_2026-11-17_084_117_133/work/viz`; màu nhãn theo mã thành viên. Đối chiếu ảnh gốc và R-01–R-13.
2. Với sai thuộc tính: tách che khuất do vật khác khỏi cắt mép, dùng các khoảng 0%, (0,30%], (30,70%], >70%. Không coi vật bị cắt mép là bị che.
3. Với sai lớp/vùng ignore/box một phía: kiểm vật thật hay mô phỏng, vật quá nhỏ và việc gộp/tách vật. Không tự kết luận người nào đúng chỉ vì confidence hoặc số đông.
4. Điền `calibration_decisions_TEMPLATE.csv` cho từng case_id sau khi thực sự chốt. File đang là mẫu rỗng ở các cột quyết định, người chốt, bản sửa và kiểm lại; không phải biên bản đã duyệt.
5. Giữ nguyên ba COCO độc lập. Chỉ sửa bản calibration riêng, lưu guideline v1.1 và guideline_change.json sau khi có quyết định thực tế.
6. Những ảnh mới có một lượt gán không dùng để đo IAA; thực hiện gán bổ sung độc lập trước, rồi cập nhật phân công có truy vết và chạy lại toàn lô bằng một bộ đầu vào mới.

Phiên IAA này dùng nhãn 117 đã được mô hình và AI hỗ trợ; không mô tả phép đo là đồng thuận giữa ba người hoàn toàn gán tay độc lập.
