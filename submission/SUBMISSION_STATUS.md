# Trạng thái bàn giao Day07 — 17/11/2026

Bài ở nhánh `main`. Đã nhận đủ bốn COCO 084/117/133/150, 40/40 ảnh và 80/80 lượt theo phân công gốc. Các gói bổ sung 7/7/6 ảnh trước đây không còn cần cho việc bù thiếu thành viên 150; chỉ giữ làm lịch sử.

## Đã có trong bản này

- Guideline cá nhân bốn mã, v1.0 khóa và v1.1 làm rõ ví dụ có hỗ trợ AI; giữ nguyên taxonomy/ngưỡng.
- Bản gốc ZIP 150 được ghi checksum, JSON gốc giữ ở `qc/imports/2026-11-17/member_150/original_150.json`. 150 thiếu hai thuộc tính ở cả 303 box; bản nhập đã bổ sung có ghi nguồn AI và giữ cờ review.
- IAA toàn lô: 463 cặp, IoU 0,9504 và cùng lớp 96,98%; 784 ca trên 39 ảnh. Đồng thuận thuộc tính không phải bằng chứng độc lập sau khi sửa schema 150 bằng dữ liệu đối chiếu.
- Nhật ký 824 dòng gồm 784 ca IAA và 40 kiểm tra toàn ảnh; tất cả ghi đúng người thực hiện là AI và chưa được nhóm xác nhận.
- COCO/CSV sau xử lý 40 ảnh, 508 annotation, batch_manifest và các vòng QC 1–3; vòng 3 là hiện hành.
- Mã reviewer 999 dành riêng cho AI, không mạo danh 084/117/133/150.

## Quyết định hiện tại: Hold

Còn 128 box cần xác nhận trên 27 ảnh; chưa có QC độc lập của người thật và ghi chú trải nghiệm cá nhân 084/150. Các file ghi chú hai mã này là bảng tổng hợp bằng chứng, không phải tự thuật giả. Nhật ký calibration là đề xuất AI, không phải xác nhận đã họp nhóm. Đủ file đầu vào không tự động làm các điều kiện này hoàn tất.

Xem [QC_REPORT.md](qc/QC_REPORT.md), [nhật ký sửa từng ảnh](automation/batch_review/review_log.json), [IAA toàn lô](qc/iaa_summary.md), [nhãn sau sửa](qc/labels_calibrated.json) và [phiếu QC hiện hành](qc/reviews/round-03/qc_review.csv).

## Kiểm lại

```powershell
python -m unittest discover -s tests -v
python scripts/validate_labels.py --all
python scripts/check_submission.py --round 3
```

Không chạy lại IAA sau khi sửa nhãn nguồn nếu chưa lưu/đổi phiên bản calibration; các mã băm hiện tại được giữ để reviewer kiểm ngược. Công cụ tái tạo bản sửa: `python tools/day07_legacy/build_assistant_batch.py` rồi `python scripts/build_final.py` (mở vòng QC mới nếu thay đổi đầu ra).

Gói ZIP có manifest riêng theo nội dung archive; submission_manifest.json trên GitHub đối chiếu toàn bộ repo và SHA-256 của ZIP. Không đưa mã băm của chính ZIP vào nội dung ZIP.
