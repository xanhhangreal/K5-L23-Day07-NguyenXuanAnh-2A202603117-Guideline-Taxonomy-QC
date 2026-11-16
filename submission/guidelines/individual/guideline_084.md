# Guideline gán nhãn — v0.1 — 084

- Ngày: 16/11/2026
- Mã thành viên: 084
- Loại nhãn: bounding box trên ảnh đường phố
- Công cụ: CVAT, xuất COCO 1.0
- Phạm vi: 40 ảnh từ `img_001.jpg` đến `img_040.jpg`

## 1. Mục tiêu

Bộ nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trong ảnh đường phố. Tôi tập trung vào ba việc: không bỏ sót vật thuộc phạm vi, phân biệt đúng lớp và vẽ box sát phần nhìn thấy.

Những lỗi cần chú ý là bỏ sót người bị che, nhầm loại xe và gán nhầm tượng hoặc hình quảng cáo thành vật thật. Guideline này làm rõ những chỗ bản v0 còn ghi chung chung để khi gán không phải tự đổi cách hiểu giữa các ảnh.

## 2. Lớp và thuộc tính

### Lớp

Mỗi vật chỉ nhận một lớp. Tôi giữ các lớp của v0 và bổ sung `bus`, `tuk_tuk` để xử lý phương tiện chưa có lớp phù hợp. Hai lớp bổ sung cần được nhóm thống nhất và cập nhật vào taxonomy trước lượt gán độc lập.

| Lớp | Cách nhận biết | Ví dụ | Không tính / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con, gồm sedan, hatchback và SUV; không có thùng hàng riêng kiểu bán tải. | Sedan, SUV. | Bán tải xếp `truck`; ô tô đồ chơi không gán. |
| `truck` | Xe chở hàng có cabin và khu vực hàng riêng, gồm xe tải, đầu kéo và bán tải. | Xe tải thùng, xe chở ô tô, bán tải. | Van có khoang kín liền thân. Bán tải có nắp thùng vẫn là `truck` nếu nhận ra cấu trúc bán tải. |
| `van` | Xe dạng van, thân kín, khoang sau liền thân để chở người hoặc hàng. | Van chở hàng, minivan. | SUV thuộc `car`; xe tải có cabin tách thùng thuộc `truck`. |
| `motorcycle` | Xe hai bánh có động cơ. | Xe máy, xe tay ga, mô tô. | Xe đạp, xích lô và tuk-tuk. |
| `person` | Người thật trong cảnh, gồm người đi bộ, đứng, ngồi và người trên phương tiện. | Người đi bộ, người lái xe máy. | Tượng, ma-nơ-canh, người trong tranh, ảnh quảng cáo hoặc phản chiếu. |
| `bus` | Xe buýt hoặc xe khách có thân xe và khoang chở nhiều hành khách, nhận dạng được là loại xe này. | Xe buýt đô thị, xe khách. | Không phân loại chỉ dựa vào kích thước; xe van vẫn thuộc `van`. |
| `tuk_tuk` | Xe ba bánh có động cơ kiểu tuk-tuk, có vị trí lái và khoang chở người hoặc hàng phía sau. | Tuk-tuk. | Xích lô không động cơ; phương tiện ba bánh khác chưa rõ loại cần review. |
| `ignore_region` | Vùng có vật mục tiêu quá nhỏ hoặc quá dày để gán riêng từng vật. | Cụm người ở xa không tách được. | Không dùng để bỏ qua vật lớn chỉ vì chưa chắc lớp. |

**R-01 — Vật ngoài phạm vi:** Xe đạp và xích lô không động cơ không thuộc bộ lớp trên nên không gán box cho phương tiện. Người thật trên đó vẫn xét theo lớp `person`. Không ép vật lạ vào lớp gần giống; ghi lại để hỏi reviewer nếu chưa xác định được phạm vi.

### Thuộc tính

Mỗi box đối tượng có đủ `occluded_level`, `truncated` và `can_review`. Riêng `ignore_region` không cần các thuộc tính này.

| Thuộc tính | Giá trị | Cách dùng |
|---|---|---|
| `occluded_level` | `0` | Không bị vật khác che. |
| `occluded_level` | `1` | Bị che trên 0% đến 30%. |
| `occluded_level` | `2` | Bị che trên 30% đến 70%. |
| `occluded_level` | `3` | Bị che trên 70% nhưng vẫn nhận ra vật và lớp. |
| `truncated` | `no` / `yes` | `yes` khi vật bị cắt bởi mép ảnh; còn lại là `no`. |
| `can_review` | `false` / `true` | `true` khi còn phân vân về lớp, box hoặc thuộc tính và cần người khác kiểm lại. |

**R-02 — Che khuất khác cắt mép:** Tôi ước lượng phần bị vật khác che trên hình dạng 2D dự kiến của đối tượng trong khung ảnh. Phần nằm ngoài ảnh chỉ tính vào `truncated`, không cộng vào mức che. Một vật có thể vừa bị che vừa bị cắt mép. Nếu chưa chắc mức che thì đánh dấu `can_review`, không dùng mức `3` để thay cho “không biết”.

## 3. Quy tắc vẽ box

### R-03 — Box sát phần nhìn thấy

Vẽ hình chữ nhật ôm các điểm ngoài cùng nhìn thấy của vật, không thêm khoảng đệm và không đoán phần thân bị khuất. Box không vượt khỏi ảnh.

Một vật bị che thành nhiều phần vẫn chỉ có một box nếu xác định chắc các phần đó thuộc cùng vật. Box bao hết các phần nhìn thấy, dù ở giữa có nền hoặc vật che. Không ghép các phần khi chưa đủ căn cứ.

### R-04 — Vật bị che hoặc cắt mép

Vẫn gán nếu nhận dạng được lớp và chiều cao box phần nhìn thấy đạt ít nhất 20 px. Box dừng tại phần nhìn thấy; chọn mức che theo R-02. Vật bị cắt ở mép ảnh đặt `truncated=yes`. Chỉ chạm mép mà vẫn thấy trọn vật thì không tính là bị cắt.

### R-05 — Người đi xe máy

Người và xe là hai đối tượng riêng. Một người ngồi trên một xe máy sẽ có một box `person` và một box `motorcycle` nếu cả hai đủ điều kiện gán. Nếu có người ngồi sau thì thêm box `person` riêng cho người đó.

Box xe không kéo lên để bao người; box người không kéo xuống để bao toàn bộ xe. Không suy đoán người bị che hoàn toàn. Quy tắc tách người và phương tiện cũng áp dụng cho người đi xe đạp hoặc xích lô, dù phương tiện đó ngoài phạm vi.

### R-06 — Xe chở xe

Gán riêng xe vận chuyển và từng xe thật được chở nếu nhận dạng được và đủ kích thước. Không dùng một box lớn để gộp tất cả thành một vật. Box từng xe không bao giá đỡ hoặc xe bên cạnh. Với xe vận chuyển, chỉ dùng các phần thuộc chính xe đó để xác định box.

### R-07 — Tượng, hình in, đồ chơi và phản chiếu

Không gán tượng người, tượng xe, ma-nơ-canh, đồ chơi, hình trên biển quảng cáo hoặc vật chỉ xuất hiện qua phản chiếu. Người hoặc xe thật nhìn xuyên kính vẫn được xét bình thường nếu nhận dạng được. Nếu khó phân biệt vật thật với phản chiếu, ghi rõ câu hỏi để review.

### R-08 — Xe chủ

Không gán phần xe gắn camera như nắp ca-pô hay gương khi xác định được đó là xe chủ. Không mặc định mọi xe ở sát mép dưới ảnh đều là xe chủ. Hình trong gương xử lý theo R-07.

### R-09 — Vật nhỏ và đám đông

Đo kích thước trên ảnh gốc, không theo độ phóng to khi xem. Vật có box cao **từ 20 px trở lên** được gán riêng nếu nhận dạng được. Vật mục tiêu nhỏ hơn 20 px dùng `ignore_region` bao gọn vùng cần bỏ qua.

Với đám đông, ưu tiên tách những người nhìn rõ và đủ kích thước. Chỉ dùng `ignore_region` cho phần không thể tách tin cậy. Không kéo vùng ignore phủ các vật lớn, rõ ràng để giảm số box phải vẽ.

### R-10 — Ca chưa chắc và ảnh trống

Nếu xác định được vật và có thể đặt box nhưng còn phân vân, chọn cách gán có căn cứ nhất, bật `can_review` và ghi lý do. Nếu chưa xác định được box, ghi tên ảnh, vùng và vấn đề để tập hợp vào `image_issues.csv` sau khi khóa lượt gán độc lập.

Ảnh không có vật hợp lệ vẫn giữ trong Task và file COCO, không tạo box cho đủ. Khi gán độc lập, chỉ dùng guideline v1.0 đã thống nhất; không xem nhãn của thành viên khác.

## 4. Ca khó

Các tên ảnh dưới đây theo tình huống được nêu trong tài liệu lab. Bảng ghi cách xử lý theo guideline; số vật và vị trí box cần đối chiếu trực tiếp trên ảnh khi thực hiện.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe chở nhiều ô tô. | R-06 | Tách box xe vận chuyển và từng ô tô đủ điều kiện. | Mỗi xe là một vật riêng; không gộp cả cụm. |
| `img_004.jpg`, `img_035.jpg` | Tuk-tuk. | R-01 | Dùng lớp `tuk_tuk` sau khi nhóm cập nhật taxonomy. | Không phù hợp với định nghĩa xe máy hai bánh. |
| `img_009.jpg`, `img_037.jpg` | Xe buýt. | R-01 | Dùng lớp `bus` sau khi nhóm cập nhật taxonomy. | Không ép xe buýt vào `van` hoặc `truck`. |
| `img_011.jpg`, `img_017.jpg`, `img_027.jpg` | Tượng có hình người hoặc xe. | R-07 | Không gán box cho tượng. | Không phải người hoặc phương tiện thật. |
| `img_018.jpg` | Chân dung trên biển quảng cáo. | R-07 | Không gán hình in; người thật khác trong cảnh vẫn xét riêng. | Tránh học nhầm hình quảng cáo thành người thật. |
| `img_020.jpg` | Phản chiếu trong gương. | R-07, R-08 | Không gán hình phản chiếu; không gán gương xe chủ. | Phân biệt vật trong cảnh với ảnh phản chiếu. |
| `img_033.jpg`, `img_038.jpg` | Ma-nơ-canh hoặc đồ chơi sau kính. | R-07 | Không gán vật mô phỏng. | Việc nằm sau kính không làm thay đổi bản chất vật. |
| `img_037.jpg` | Bán tải có nắp thùng cao, dễ nhầm van. | R-01 | Chọn `truck` khi nhận ra cấu trúc bán tải; chưa đủ căn cứ thì review. | Nắp thùng không tự làm bán tải thành van. |
| `img_006.jpg`, `img_029.jpg`, `img_039.jpg` | Xe đạp hoặc xích lô không động cơ. | R-01, R-05 | Không gán phương tiện; người trên xe xét riêng. | Phương tiện ngoài taxonomy, người vẫn trong phạm vi. |

Với ca người đi xe máy, che khuất và sát ngưỡng 20 px, tôi dùng R-02, R-04, R-05 và R-09. Cần bổ sung tên ảnh cụ thể sau khi tự kiểm bộ ảnh, không tự đặt ví dụ hoặc số box khi chưa xem.

## 5. QC và phiên bản

### Kiểm nhãn trước khi xuất

Tự rà lại lớp, box, thuộc tính, box trùng và vật bỏ sót ngoài vùng ignore. Lưu CVAT rồi xuất COCO 1.0, tắt Save images, lấy JSON annotation lưu thành `submission/labels/117.json`.

```powershell
python scripts/validate_labels.py submission/labels/117.json
```

Cờ `occluded` có sẵn của CVAT không thay cho `occluded_level`. Validator kiểm cấu trúc và tập ảnh; box có đúng vật hay không vẫn phải xem trực tiếp.

### Ngưỡng QC

Giữ nguyên mục `rules` trong taxonomy.

| Tiêu chí | Ngưỡng / cách tính |
|---|---|
| Chiều cao tối thiểu box đối tượng | 20 px. |
| Ghép box đo IAA | Ghép 1–1, không phân biệt lớp, IoU ≥ 0,5. |
| IoU theo kích thước | Box cao ≥ 50 px: 0,85; dưới 50 px: 0,70. |
| IAA | IoU trung bình ≥ 0,85; đồng thuận lớp ≥ 95%, tính trên các cặp ghép được. |
| Độ phủ | Đủ 100% lượt gán trong `assignment.csv`. |
| Lỗi theo ảnh | Số ảnh có ít nhất một lỗi / số ảnh đã duyệt; tối đa 2% để xét Release. |
| Lỗi theo đối tượng | Số annotation lỗi / số annotation đã duyệt; báo kèm số lượng. Bỏ sót ghi riêng trong phiếu QC. |

Báo cáo luôn ghi tử số và mẫu số. Không có cặp ghép thì ghi IAA là N/A. Đồng thuận cao chưa chắc đúng vì cả hai người có thể cùng bỏ sót hoặc hiểu sai.

QC duyệt cả 40 ảnh. Một ảnh lỗi là 2,5%, đã vượt ngưỡng 2%. Thiếu bằng chứng hoặc còn vấn đề chưa chốt thì **Hold**; vượt ngưỡng lỗi hoặc có lỗi lặp thì **Rework**; chỉ **Release** khi đủ bằng chứng và reviewer xác nhận.

### Người chốt và lịch sử thay đổi

Ca mơ hồ được nhóm thống nhất ở pha 2 hoặc calibration pha 5. Nhật ký ghi mã người chốt, quy tắc áp dụng, chỗ sửa và người kiểm lại. Reviewer bản cuối theo `TEAM.md`, dùng mã ba chữ số trên phiếu. Ưu tiên người kiểm khác người sửa.

Thay đổi cách chọn vật, lớp, box hoặc thuộc tính là thay đổi `semantic`: ghi phạm vi `lo` và kiểm lại cả lô. Chỉ sửa câu chữ mà giữ nguyên cách gán thì ghi `editorial`. Sau khi sửa nhãn cuối, mở vòng QC mới và giữ vòng cũ.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0` | Bản khởi đầu của lab. | Định nghĩa lớp và cách gán còn chung chung. |
| `v0.1` | Làm rõ lớp, mức che, quy tắc box và ca khó; bổ sung phương án cho bus và tuk-tuk. | Chuẩn bị bản cá nhân để thảo luận, chưa thay thế guideline v1.0 của nhóm. |
