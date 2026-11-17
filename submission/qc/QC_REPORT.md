# Báo cáo bàn giao Day07 — đủ dữ liệu, còn xác nhận người thật

- Mục đích và giới hạn sử dụng: bài thực hành 40 ảnh đường phố 2D. Bản sửa và lần kiểm này do AI thực hiện; chưa có xác nhận calibration/QC độc lập của nhóm. Không coi là nhãn đã nghiệm thu cho huấn luyện.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json đối chiếu labels_calibrated.json và labels_calibrated.csv; submission/submission_manifest.json ghi checksum gói bàn giao. Có snapshot riêng cho từng vòng QC.
- Guideline và taxonomy khi gán / khi bàn giao: guideline_v1.0_agreed.md và taxonomy v1.0 đã khóa; bản bàn giao guideline_v1.1_calibrated.md làm rõ ví dụ, không đổi nghĩa quy tắc hay taxonomy. v1.1 là bản AI biên soạn chờ nhóm xác nhận.
- Lượt hoàn thành / được giao: 80/80 theo bảng phân công gốc; mỗi ảnh đủ hai nguồn nộp. 084: 274, 117: 203, 133: 281, 150: 303 annotation. Đây là độ phủ file đã nhận, không chứng nhận độc lập của quá trình gán.
- Vòng QC: 3
- Người review và ngày: AI assistant, mã kỹ thuật 999 dành riêng cho AI, ngày 17/11/2026. 999 không phải thành viên; người sửa và người kiểm là cùng AI. Chưa có người thật ký nghiệm thu.
- Đã duyệt / cả lô: AI đã mở overlay và rà 40/40 ảnh sau sửa; 0/40 được reviewer người thật xác nhận trong phiên hỗ trợ này.
- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: bàn giao cho nhóm/coach xem và xác nhận; còn 128 box can_review trên 27 ảnh, ghi chú trải nghiệm 084/150 chưa có, calibration mới là đề xuất AI. Không xóa cờ để chuyển thành Release.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: C001 của IAA toàn lô ở img_001, đối chiếu R-01/R-03, review_log.json và nhãn cuối. Ở vòng 1, box person #4 dừng y405, AI đã mở xuống y432 và giữ cờ tách người; vòng 3 trỏ bản đã sửa. Chưa có người ngoài nhóm kiểm ngược.

## IAA trước sửa

463 cặp box trên 40 ảnh; IoU trung bình 0,9504, đồng thuận lớp 96,98%. Có 784 ca trên 39 ảnh: 106 chỉ một bên gán, 152 bất đồng thuộc tính, 29 bất đồng ignore, 442 cờ review, 41 IoU thấp và 14 sai lớp. Cặp 084–117 chỉ cùng lớp 93,94%; cặp 133–150 chỉ 87,10%, dưới ngưỡng 95% dù trung bình tổng đạt.

Bản gốc 150 thiếu occluded_level và truncated ở cả 303 annotation. Bản gốc được giữ nguyên byte tại imports/2026-11-17/member_150/original_150.json. labels/150.json giữ geometry/lớp và bổ sung thuộc tính có nguồn AI; mức che có sử dụng nhãn đối chiếu khi ghép được box, truncated dùng biên ảnh. Vì vậy đồng thuận thuộc tính có phần phụ thuộc, không dùng nó chứng minh hai người đã gán độc lập. Tất cả box 150 giữ can_review.

## Bản sửa và calibration

Nhãn sau xử lý có 40 ảnh, 508 annotation, gồm 495 box đối tượng và 13 ignore_region. Mỗi ảnh chỉ có một bản kết quả. Nhật ký calibration có đủ 784 case_id của IAA và thêm 40 dòng kiểm toàn ảnh. Mỗi dòng ghi rõ đề xuất AI, rule, ảnh/object IDs, dấu phiên bản sửa và trạng thái chưa được nhóm xác nhận; không phải biên bản họp đã diễn ra.

Đã xử lý: tách hai người ở img_001; mở phần rơ-moóc ở img_002; sửa lớp van/truck ở img_018/img_025; loại box đầu người trùng ở img_016; giữ rỗng các ảnh tượng/phản chiếu/đồ chơi img_017/020/027/033/038; đổi tuk-tuk ở img_040; chuyển vật dưới 20 px sang ignore. Phần xe vàng img_024, đám đông img_019/021, xe máy chồng nhau img_030 và các mảnh xe tối vẫn có cờ.

Hai bên có thể cùng sai: img_001 hai nguồn cùng giữ box không tách đúng hai người trái. Trong nguồn 150, 23 ô tô đồ chơi img_038 không được chuyển sang bản sửa. Chưa có ca tham chiếu do coach cung cấp để kết luận phần đối chiếu đó đã hoàn tất.

## Ý nghĩa phiếu QC

Vòng 1 ghi lỗi box #4 img_001 và được giữ nguyên snapshot. Vòng 2 mở trước khi hoàn thiện mã phiên bản, chưa dùng để kết luận. Vòng 3 là vòng hiện hành. Script ghi 0 lỗi mới được khẳng định / 40 ảnh và 0 / 495 đối tượng từ lượt AI rà; đây không phải ước lượng lỗi thực tế 0%, vì còn 128 câu hỏi mở. Những câu hỏi này được lưu bằng can_review và giữ quyết định Hold.

Hai mục guideline-gap của lệnh QC là hai nhóm việc chưa chốt: (1) xác nhận các ca hình ảnh còn cờ; (2) xác nhận quy trình calibration/QC và ghi chú của người học. Đây không phải hai annotation lỗi. Không thay ngưỡng taxonomy.

## Cần xác nhận để đổi quyết định

Nhóm kiểm các box còn cờ, bổ sung phần tự thuật 084/150 bằng việc thực tế đã làm, và reviewer người thật duyệt bản nhãn có mã băm. Nếu sửa nhãn, cập nhật quyết định và mở vòng mới; giữ các vòng 1–3. Checker 0 lỗi chỉ xác nhận cấu trúc/hồ sơ khớp, không thay quyết định người thật.
