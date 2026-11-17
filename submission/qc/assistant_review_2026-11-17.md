# Kiểm tra tiếp sau bản Hold — 17/11/2026

Người thực hiện: AI assistant. Đây là ghi nhận kiểm ảnh và đề xuất xử lý, chưa phải quyết định calibration nhóm hoặc phiếu nghiệm thu của 117/133. Không sửa COCO độc lập đã nộp.

## Ảnh đã đối chiếu trong lượt này: img_001.jpg

Đã mở ảnh gốc `data/images/img_001.jpg`, overlay hai nguồn và annotation gốc 117/133. Tham chiếu các ca C001–C009 trong `partial_2026-11-17_084_117_133/calibration_candidates.csv`.

| Phát hiện | Bằng chứng | Đề xuất xử lý |
|---|---|---|
| Box truck sai vị trí và dư ở nguồn 133 | C001, annotation 1, XYWH [234,289,488,348]. Box bao một phần người đứng và thùng xe; nguồn này còn một box truck khác cho cùng chiếc xe. | Loại box sai trong bản calibration riêng; giữ một box ôm toàn bộ phần xe nhìn thấy theo R-01/R-03. |
| Cần kiểm lại việc tách hai người bên trái | C002, nguồn 133 có thêm person [90,99,60,148]; cả hai nguồn còn person [105,113,123,288]. Ảnh gốc nhìn thấy hai khuôn mặt khác nhau tại vùng bên trái. | Không tự xóa box chỉ vì chỉ một bên vẽ. Kiểm từng người và vẽ box phần nhìn thấy riêng, tránh một box gộp hai người, theo R-03/R-04. |
| Các giá trị mức che bằng 0 cần xem lại | C003–C009. Người ngồi bị bàn, xe hoặc người khác che; xe bị người đứng phía trước che một phần. | Ước lượng theo R-02, tách che khuất khỏi phần ngoài ảnh. Không chép mức che của 117 cho mọi ca chỉ vì nguồn này đã được AI xem trước. |

Cần người thật kiểm lại các đề xuất trên rồi ghi người chốt và kết quả vào nhật ký calibration. Chưa kiểm lại 18 ảnh bị cờ còn lại trong lượt bổ sung này. Lượt AI review Task 117 trước đó là bằng chứng riêng, không được tính thành review nhóm.

## Các điều kiện còn thiếu theo checker

1. Ghi chú cá nhân 084: thành viên tự viết từ việc thực tế đã làm.
2. Nhãn 150: người điều phối đã yêu cầu bỏ qua thành viên này; chưa có nhãn để thay thế.
3. Ghi chú cá nhân 150: không tạo thay cho người đã bỏ qua.
4. Danh sách nhãn chưa khớp assignment: còn 20 lượt gán; kế hoạch thay thế giao 084 thêm 7, 117 thêm 7 và 133 thêm 6 ảnh. Chưa áp dụng bảng đề xuất khi chưa có bài bổ sung.
5. Chưa có vòng QC toàn lô để ghi số vòng thật.
6. Chưa có qc_result.json vì chưa có nhãn cuối và phiếu QC thực tế.

Sau khi có 20 lượt bổ sung độc lập: giữ bản phân công cũ trong lịch sử, áp dụng phân công mới có truy vết; chạy IAA toàn lô; chốt calibration; lưu v1.1 và nhãn sửa; build_final; duyệt QC toàn lô rồi check_submission. Không gán danh tính người thật cho quyết định do AI tạo.
