# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **20**; số người gán: 3
- Lượt gán đủ **40/40**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 214 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 20 | 214 | 0.944 | 97.7% | 37.9% | 92.1% | 20/36 | 0 | ĐẠT |
| 084|117 | 6 | 33 | 0.923 | 93.9% | 51.5% | 100.0% | 2/0 | 0 | CHƯA ĐẠT |
| 084|133 | 9 | 131 | 0.941 | 97.7% | 38.2% | 89.3% | 13/24 | 0 | ĐẠT |
| 117|133 | 5 | 50 | 0.966 | 100.0% | 28.0% | 94.0% | 5/12 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 339 ({'bo_sot_thua': 47, 'sai_thuoc_tinh': 135, 'co_can_review': 115, 'iou_thap': 16, 'bat_dong_ignore': 21, 'sai_lop': 5}), trên 19 ảnh cần calibration.
