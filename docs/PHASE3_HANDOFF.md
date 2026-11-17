# Pha 3 — Phân công ảnh và thao tác CVAT

## Phần đã chuẩn bị

Nhóm có bốn mã `084`, `117`, `133`, `150`. Bảng chung nằm ở `submission/qc/assignment.csv`, sinh bằng seed 42. Mỗi người nhận 20 ảnh; toàn bộ 40 ảnh đều có đúng hai người gán, tổng cộng 80 lượt. Không chia lại ảnh riêng trên từng máy bằng danh sách mã hoặc seed khác.

| Mã | Tên Task gợi ý | Thư mục ảnh | Gói tải lên CVAT | JSON phải nộp |
|---|---|---|---|---|
| 084 | `Day07_084_v1.0` | `work/084/images/` | `work/cvat_upload/084.zip` | `submission/labels/084.json` |
| 117 | `Day07_117_v1.0` | `work/117/images/` | `work/cvat_upload/117.zip` | `submission/labels/117.json` |
| 133 | `Day07_133_v1.0` | `work/133/images/` | `work/cvat_upload/133.zip` | `submission/labels/133.json` |
| 150 | `Day07_150_v1.0` | `work/150/images/` | `work/cvat_upload/150.zip` | `submission/labels/150.json` |

Danh sách tên ảnh từng người: `submission/qc/assignments/<mã>.txt`. Gói ZIP chỉ chứa ảnh được giao, tên ảnh giữ nguyên. `work/` là dữ liệu cục bộ đã bị Git ignore; thành viên ở máy khác có thể tạo lại bằng cùng lệnh:

```powershell
python scripts/split_assign.py --members 117,133,084,150 --seed 42 --copy-images
```

## Bắt đầu gán theo v1.0 đã khóa

Người điều phối đã yêu cầu bỏ qua guideline `084`, khóa bản tổng hợp từ `117`, `133`, `150` và bắt đầu phân công cho cả bốn thành viên. Dùng `submission/guidelines/guideline_v1.0_agreed.md` và taxonomy v1.0 đã khóa; không chờ bản 084 để bắt đầu. Hồ sơ khóa nằm tại `submission/guidelines/guideline_v1.0_lock.json`.

Mỗi người đọc phiếu riêng tại `submission/tasks/task_<mã>.md`, dùng ZIP của mình và điền đủ thuộc tính. Một người/một xe tách hai box, hai người/một xe tách ba box nếu từng vật đủ điều kiện. Các ca chưa chắc theo R-10, giữ để calibration. Không đổi taxonomy giữa lượt độc lập. Nếu danh sách thành viên thay đổi, người điều phối phải phát lại một bảng phân công duy nhất.

## Tạo Project và Task

1. Mỗi người mở CVAT local `http://localhost:8080/` trên máy mình, chọn **Projects → Create new project**. Tên Project `Day07_GuidelineQC_v1.0`. URL localhost trỏ tới máy đang dùng, không phải CVAT chung của nhóm.
2. Trong **Labels → Raw**, dán nội dung `cvat/labels_generated.json` đã sinh từ taxonomy cuối cùng của pha 2. Có tám nhãn: `car`, `truck`, `van`, `motorcycle`, `person`, `bus`, `tuk_tuk`, `ignore_region`.
3. Kiểm ba thuộc tính của các lớp đối tượng: `occluded_level`, `truncated`, `can_review`. Ignore không cần thuộc tính đối tượng.
4. Mỗi người tạo Task riêng trong Project, dùng tên theo bảng trên. Tải ZIP của đúng mã hoặc chọn 20 ảnh trong thư mục tương ứng; dùng một trong hai cách, tránh tải trùng ảnh.
5. Kiểm Task có 20 frame, tên ảnh khớp danh sách được giao. Không đổi tên ảnh, không bỏ ảnh trống và không chia sẻ nhãn giữa các Task trước khi mọi người nộp riêng.

Đã tạo trên máy thành viên 117: Project #3 (`http://localhost:8080/projects/3`) và Task #25 (`http://localhost:8080/tasks/25`), Job #25, 20 frame (0–19). Các thành viên khác tự tạo trên CVAT local của mình; không dùng các ID này như ID chung.

Gói bàn giao được đưa lên Git tại `submission/packages/handoff_<mã>_v1.0.zip`, kèm bảng tải trong `submission/packages/README.md`; bản cục bộ nằm ở `work/cvat_upload/`. Gói chứa guideline khóa, taxonomy, cấu hình nhãn, danh sách và 20 ảnh theo mã. Giải nén vào repo của mình để dùng đường dẫn trong tài liệu. Nếu dùng gói handoff, chọn 20 ảnh trong thư mục images, không tải toàn bộ handoff ZIP làm dataset. File `<mã>.zip` chỉ chứa ảnh là bản tiện dụng cục bộ, không cần tải để dùng gói handoff.

Cấu hình đã được kiểm trên CVAT local: từng label có `type=rectangle`; checkbox can_review xuất sang CVAT với `values=["false"]`. Trong taxonomy của bài, checkbox vẫn giữ `values=[]` đúng schema. Đây là chuyển đổi định dạng tại `make_cvat_labels.py`, không thay ngưỡng hoặc nghĩa thuộc tính.

## Khi gán

- Dùng Rectangle theo guideline v1.0 đã khóa. Phần quyết định và vẽ box do người thực hiện.
- Cờ `occluded` mặc định của CVAT khác thuộc tính `occluded_level`; điền thuộc tính của Project.
- Đặt được box nhưng còn phân vân thì dùng `can_review`; chưa có căn cứ đặt box thì ghi ảnh, vùng và câu hỏi riêng.
- Sau khi khóa lượt độc lập, tập hợp ca chưa có box vào `submission/qc/image_issues.csv` với header `image,annotator,region,note`. Không điền trước các vấn đề hoặc quyết định chưa thực hiện.
- Lưu thường xuyên; chưa xem nhãn người khác và chưa sửa guideline giữa lượt độc lập.

## Export và gửi riêng

1. **Actions → Export task dataset → COCO 1.0**, tắt **Save images**.
2. Tải ở **Requests**, giải nén, lấy `annotations/instances_default.json` hoặc file subset tương ứng. Không đổi đuôi ZIP thành JSON.
3. Lưu JSON theo mã trong bảng; ảnh trống vẫn phải xuất hiện trong trường `images`.
4. Chạy validator riêng của mình, ví dụ mã 117:

```powershell
python scripts/validate_labels.py submission/labels/117.json
```

5. Gửi riêng theo kênh của coach/người điều phối. Mỗi người có guideline cá nhân, JSON COCO và ghi chú `submission/individual_notes/<mã>.md` của chính mình.

## Sau khi cả bốn người nộp

Người điều phối mới tập hợp bốn JSON và chạy Pha 4:

```powershell
python scripts/validate_labels.py --all
python scripts/qc_compare.py
python scripts/viz_disagreement.py --images flagged
```

Chỉ đo IAA khi đủ 80 lượt hợp lệ. Hiện chưa có nhãn cá nhân nên chưa chạy các lệnh này để lấy số liệu hoặc kết luận chất lượng.
