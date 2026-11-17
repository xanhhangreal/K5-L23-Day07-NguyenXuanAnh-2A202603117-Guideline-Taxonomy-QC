# Bàn giao Day07 — Hold — 17/11/2026

Gói này nộp bằng chứng đã có theo nhánh Hold của `SUBMISSION.md`. Chưa đạt điều kiện bàn giao nhãn cuối và chưa có kết quả checker 0 lỗi. Không thay ngưỡng hay tạo nhãn/biên bản thay người chưa thực hiện.

## Đã có

- Guideline cá nhân 117/133/150 và guideline nhóm v1.0 đã khóa. Bỏ qua guideline 084 tại bước chốt theo yêu cầu người điều phối, không tạo bản cá nhân thay người đó.
- COCO 084: 20 ảnh/274 annotation; 117: 20 ảnh/203 annotation; 133: 20 ảnh/281 annotation. Giữ nguyên JSON đã nộp, cả ảnh không có annotation.
- Task 117 đã chạy công cụ, được AI xem lại toàn bộ, export/validate và completed trên CVAT. Nguồn và lịch sử sửa được giữ ở `automation/` và `exports/history/`.
- IAA một phần: 20 ảnh đủ hai lượt, 214 cặp box, IoU TB 0,944, cùng lớp 97,7%; 339 ca cần xem trên 19 ảnh.
- Bảng coverage toàn lô, mẫu calibration chín cột, ảnh overlay và ba gói bổ sung; không dùng bài 150 cho lượt phân tích hiện tại.

## Chưa có và người xử lý

| Phần thiếu | Trạng thái thực tế | Việc tiếp theo |
|---|---|---|
| Đủ lượt gán | 60/80, 20 ảnh chỉ có một người | Ba thành viên làm 20 lượt bổ sung độc lập: 084: 7, 117: 7, 133: 6. |
| Guideline/ghi chú cá nhân | 084 thiếu guideline và ghi chú; 150 chưa nộp nhãn/ghi chú | Người học tự viết hoặc coach ghi nhận phạm vi loại trừ; không tạo hồ sơ thay. |
| Calibration | Chưa có quyết định nhóm cho 339 ca trong tập con | Xem overlay, chốt theo rule ID, ghi người chốt/bản sửa/kiểm lại. |
| v1.1 và nhãn cuối | Chưa có vì calibration chưa xong | Thực hiện pha 5 với bộ đầu vào toàn lô sau bổ sung. |
| QC toàn lô | Chưa có vòng QC, phiếu hay kết quả | Reviewer duyệt 40 ảnh sau khi có nhãn cuối, ghi đúng vòng và quyết định. |

## Đọc kết quả

- [QC_REPORT.md](qc/QC_REPORT.md) ghi Hold và các giới hạn.
- [PARTIAL_IAA_REPORT.md](qc/partial_2026-11-17_084_117_133/PARTIAL_IAA_REPORT.md) ghi rõ mẫu số. Con số 40/40 trong summary bên trong chỉ là lượt của tập con 20 ảnh, không phải toàn lô.
- [CALIBRATION_HANDOFF.md](qc/partial_2026-11-17_084_117_133/CALIBRATION_HANDOFF.md) và `calibration_decisions_TEMPLATE.csv` chuẩn bị cho buổi chốt thực tế.
- [Gói tải và task bổ sung](packages/README.md).
- `submission_manifest.json` ghi SHA-256 các file đầu vào, gói và báo cáo; không phải batch_manifest nhãn cuối.
- `qc/validation/` lưu kết quả lệnh đã chạy, gồm cả kiểm tra thất bại do thiếu bằng chứng.

## Chạy lại

```powershell
python -m unittest discover -s tests -v
python scripts/validate_labels.py --all
python scripts/qc_compare.py
python scripts/check_submission.py --round 1
```

Hai lệnh cuối hiện được giữ nguyên để báo thiếu lượt và bằng chứng; không sửa code để biến Hold thành pass.

Để tái hiện phép so sánh tập con mà không ghi đè bằng chứng đã nộp:

```powershell
python tools/day07_legacy/partial_compare.py --run-tag reviewer_replay_01
```

Lệnh tạo workspace tạm trong `work/` và báo cáo mới dưới `submission/qc/partial_reviewer_replay_01/`; tuyệt đối không tính ảnh chỉ có một lượt vào IAA. Không đưa `work/`, trọng số model hoặc thông tin đăng nhập vào gói nộp.
