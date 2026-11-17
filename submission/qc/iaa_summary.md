# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 463 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 463 | 0.950 | 97.0% | 69.5% | 94.2% | 29/90 | 0 | ĐẠT |
| 084|117 | 6 | 33 | 0.923 | 93.9% | 51.5% | 100.0% | 2/0 | 0 | CHƯA ĐẠT |
| 084|133 | 9 | 131 | 0.941 | 97.7% | 38.2% | 89.3% | 13/24 | 0 | ĐẠT |
| 084|150 | 5 | 78 | 0.916 | 100.0% | 100.0% | 93.6% | 3/6 | 0 | ĐẠT |
| 117|133 | 5 | 50 | 0.966 | 100.0% | 28.0% | 94.0% | 5/12 | 0 | ĐẠT |
| 117|150 | 9 | 109 | 0.962 | 99.1% | 99.1% | 100.0% | 5/14 | 0 | ĐẠT |
| 133|150 | 6 | 62 | 0.993 | 87.1% | 88.7% | 91.9% | 1/34 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 784 ({'bo_sot_thua': 106, 'sai_thuoc_tinh': 152, 'bat_dong_ignore': 29, 'co_can_review': 442, 'iou_thap': 41, 'sai_lop': 14}), trên 39 ảnh cần calibration.
