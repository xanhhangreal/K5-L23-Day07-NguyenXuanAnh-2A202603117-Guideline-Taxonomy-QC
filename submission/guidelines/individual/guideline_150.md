# Guideline gán nhãn — v0.1-individual — 150

- Phiên bản: `v0.1-individual`.
- Ngày: 16/11/2026.
- Người viết / duyệt: thành viên `150` / chờ nhóm duyệt.
- Phạm vi: 40 ảnh đường phố, từ `img_001.jpg` đến `img_040.jpg`.
- Công cụ: CVAT, bounding box chữ nhật, xuất COCO 1.0.
- Trạng thái: đề xuất cá nhân để thảo luận trước khi nhóm khóa guideline v1.0.
- Hỗ trợ AI: hỗ trợ biên soạn và rà soát ví dụ; người viết tự kiểm ảnh gốc và xác nhận quyết định. Tài liệu chưa ghi nhận kết quả gán nhãn hoặc QC thực tế.

## 1. Mục tiêu

Bộ nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố 2D. Tôi ưu tiên không bỏ sót đối tượng thuộc phạm vi, chọn đúng lớp và giữ cách vẽ box nhất quán giữa các ảnh.

Bỏ sót người hoặc xe bị che làm thiếu dữ liệu về tình huống giao thông khó. Nhầm lớp bán tải, van hoặc tuk-tuk làm sai mục tiêu phân loại. Gán tượng, đồ chơi hoặc hình quảng cáo thành người và xe thật tạo ví dụ sai cho mô hình. Box quá rộng, bao cả người ngồi trên xe hoặc hàng chở rời cũng làm sai ranh giới đối tượng.

Phạm vi là thông tin có thể nhận biết trên ảnh. Không suy đoán số chỗ ngồi, tình trạng động cơ hoặc phần thân bị khuất để quyết định nhãn.

## 2. Lớp và thuộc tính

### Lớp

Mỗi đối tượng có đúng một lớp. `ignore_region` là vùng bỏ qua, không phải lớp đối tượng. Tôi đề xuất bổ sung `bus` và `tuk_tuk`; nhóm cần chốt và cập nhật taxonomy trước lượt gán độc lập.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con có kết cấu chở người, gồm sedan, hatchback, wagon và SUV. | Ô tô trong `img_015`; ô tô thật được chở ở `img_002`. | Bán tải là `truck`; mô hình xe trong `img_038` không gán. |
| `truck` | Xe chở hàng có cabin và khu vực hàng riêng, gồm xe tải, đầu kéo và bán tải. | Xe chở ô tô ở `img_002`, xe tải nhỏ ở `img_036`. | Van có khoang sau liền thân; nắp thùng không tự đổi bán tải thành van. |
| `van` | Xe dạng van có khoang hành khách hoặc hàng hóa kín liền thân với khoang lái. | Xe van phía sau người đi xe máy ở `img_005`. | SUV thuộc `car`; xe cabin tách thùng thuộc `truck`. |
| `motorcycle` | Xe máy, xe tay ga hoặc mô tô, gồm mô tô gắn sidecar. | Xe máy ở `img_026`, mô tô sidecar ở `img_022`. | Xe đạp, xích lô; tuk-tuk có thân xe ba bánh riêng. |
| `person` | Người thật trong cảnh, gồm người đi bộ, người ngồi và người trên phương tiện. | Người bán hàng ở `img_003`, hai người trên xe ở `img_026`. | Tượng, ma-nơ-canh, hình người trên biển, người chỉ thấy qua phản chiếu. |
| `bus` (đề xuất) | Xe có kết cấu nhận dạng được là xe buýt hoặc xe khách. | Xe khách ở `img_009`, xe buýt phía sau bán tải ở `img_037`. | Không suy ra lớp chỉ từ kích thước hoặc số chỗ không nhìn thấy. |
| `tuk_tuk` (đề xuất) | Xe cơ giới ba bánh kiểu tuk-tuk hoặc auto rickshaw có vị trí lái và khoang khách hoặc hàng phía sau. | Hai tuk-tuk ở `img_004`, xe chở hàng ở `img_035`. | Xích lô đạp chân và mô tô có sidecar. |
| `ignore_region` | Vùng chứa đối tượng mục tiêu quá nhỏ hoặc cụm không thể tách từng vật tin cậy. | Phần người, xe ở xa trong `img_021`, `img_025`. | Không phủ lên vật lớn rõ chỉ vì khó chọn lớp hoặc muốn giảm số box. |

**Vật ngoài taxonomy:** Xe đạp, xích lô không động cơ, động vật và đồ vật sinh hoạt không được gán box đối tượng trong đề xuất này. Người thật trên xe đạp hoặc xích lô vẫn xét theo `person`. Không dùng `ignore_region` chỉ vì một vật ngoài phạm vi. Vật chưa xác định thuộc phạm vi hay không phải ghi câu hỏi để reviewer chốt, không ép vào lớp gần giống.

### Thuộc tính

Mỗi box đối tượng có đủ ba thuộc tính dưới đây. `ignore_region` không cần thuộc tính đối tượng.

| Thuộc tính | Giá trị cố định | Ý nghĩa / ngưỡng |
|---|---|---|
| `occluded_level` | `0` | Không bị vật khác che: 0%. |
| `occluded_level` | `1` | Phần bị che trên 0% đến hết 30%. |
| `occluded_level` | `2` | Phần bị che trên 30% đến hết 70%. |
| `occluded_level` | `3` | Phần bị che trên 70%, nhưng vẫn đủ căn cứ nhận dạng. |
| `truncated` | `no`, `yes` | `yes` khi một phần đối tượng nằm ngoài khung ảnh; chỉ chạm mép nhưng thấy trọn vật thì `no`. |
| `can_review` | `false`, `true` | `true` khi cần người khác xác nhận lớp, box, thuộc tính hoặc bản chất vật thật. |

Ước lượng che khuất trên hình dạng 2D dự kiến của phần đối tượng nằm trong khung ảnh. Phần ngoài khung chỉ tính vào `truncated`, không cộng vào mức che. Một vật có thể vừa bị che vừa bị cắt mép. Không dùng mức `3` thay cho trạng thái không biết; chưa chắc thì bật `can_review`.

Dùng thuộc tính `occluded_level` của Project; cờ `occluded` có sẵn của CVAT là trường khác và không thay thế thuộc tính này.

## 3. Quy tắc vẽ box

### R-01 — Chọn đối tượng và lớp

Chỉ gán đối tượng thật thuộc phạm vi, nhận dạng được lớp và đủ kích thước. Áp dụng định nghĩa lớp ở mục 2. Nếu nhóm chưa chốt lớp bổ sung thì dừng để thống nhất trước lượt gán, không tự thay taxonomy trong khi làm độc lập.

### R-02 — Box ôm sát phần nhìn thấy

Vẽ hình chữ nhật theo trục ảnh, ôm các điểm ngoài cùng nhìn thấy của vật, không thêm đệm hoặc dựng phần bị khuất. Nếu một vật lộ thành nhiều phần và xác định được chúng thuộc cùng vật, dùng một box bao hết các phần đó; khoảng giữa có thể chứa vật che hoặc nền. Không gộp hai vật chỉ vì chúng chạm nhau.

Tính các phần gắn với đối tượng như gương, tay lái, bánh xe và mũ bảo hiểm người đang đội. Không tính bóng đổ, vật đứng cạnh hoặc hàng chở rời. Box nằm trong giới hạn ảnh.

Khi ghi tọa độ để trao đổi, dùng XYXY `[x_min, y_min, x_max, y_max]` theo pixel ảnh gốc. File COCO dùng XYWH `[x_min, y_min, width, height]`, trong đó `width = x_max - x_min` và `height = y_max - y_min`. Không ghi XYXY hoặc tọa độ YOLO chuẩn hóa vào trường `bbox` của COCO.

### R-03 — Che khuất và cắt mép

Vật bị che hoặc cắt mép vẫn gán nếu nhận dạng được lớp và box phần nhìn thấy cao ít nhất 20 px. Box chỉ bao phần nhìn thấy và dừng ở mép ảnh nếu bị cắt. Không đặt box cho vật bị che hoàn toàn; ca có dấu hiệu vật nhưng không đủ căn cứ đặt box thì ghi vấn đề cấp ảnh theo R-11.

### R-04 — Người trên phương tiện

Tách từng người và từng phương tiện thành đối tượng riêng. Một người trên xe máy có một box `person` và một box `motorcycle` nếu cả hai đủ điều kiện; hai người trên một xe có ba box cho cụm đó. Box xe không kéo lên bao người, box người không kéo xuống bao cả xe. Người trên xe đạp hoặc xích lô vẫn gán riêng dù phương tiện ngoài phạm vi.

### R-05 — Xe chở xe, sidecar và hàng hóa

Xe vận chuyển và từng xe thật được chở là các đối tượng riêng nếu đủ điều kiện. Box xe vận chuyển gồm cabin và khung chở thuộc chính xe; box xe được chở không bao giá đỡ.

Mô tô sidecar gắn liền là một `motorcycle`, box bao cả phần sidecar. Không gán thêm một box phương tiện cho riêng sidecar.

Không mở rộng box để bao kiện hàng, thanh dài hoặc tượng trang trí chở trên xe. Thùng xe, nắp thùng và khung gắn cố định thuộc kết cấu xe được tính vào box. Bán tải có nắp thùng vẫn là `truck` nếu nhận ra kết cấu bán tải.

### R-06 — Tượng, hình in, đồ chơi và phản chiếu

Không gán tượng, ma-nơ-canh, đồ chơi, hình in hoặc vật chỉ xuất hiện qua phản chiếu. Vật thật nhìn xuyên kính vẫn xét bình thường. Không loại một xe chỉ vì thiết kế lạ hoặc một người chỉ vì mặc trang phục hóa trang. Nếu chưa phân biệt được người thật với tượng, xe thật với mô hình hoặc hình cắt, đánh dấu cần review thay vì khẳng định khi thiếu bằng chứng.

### R-07 — Xe chủ gắn camera

Không gán phần xe chủ như nắp ca-pô hoặc gương khi xác định được đó là xe mang camera. Không mặc định mọi xe sát mép dưới đều là xe chủ. Vật trong gương xử lý theo R-06.

### R-08 — Vật nhỏ

Đo chiều cao box phần nhìn thấy trên ảnh gốc, không theo mức phóng to màn hình. Vật nhận dạng được và cao từ 20 px trở lên được gán riêng; vật mục tiêu nhỏ hơn 20 px dùng `ignore_region` bao gọn phần cần bỏ qua. Vùng ignore không được phủ các đối tượng đủ lớn, rõ ràng khác.

### R-09 — Đám đông

Ưu tiên tách từng vật đủ lớn và có ranh giới nhận biết được. Chỉ dùng `ignore_region` cho phần quá dày hoặc quá nhỏ không tách tin cậy. Không gộp tất cả người ở tiền cảnh với cụm xa thành một vùng ignore.

### R-10 — Vật bị mờ

Vật bị mờ vẫn gán nếu nhận dạng được lớp và ranh giới phần nhìn thấy đủ tin cậy. Không dùng cả vệt chuyển động làm đường bao. Nếu ranh giới không xác định được, ghi vùng và câu hỏi để review; không tự tạo box đoán.

### R-11 — Ca chưa chắc và ảnh không có đối tượng

Đặt được box nhưng còn phân vân thì bật `can_review` và ghi lý do. Chưa đặt được box thì ghi `image, annotator, region, note`; sau khi khóa nhãn độc lập, nhóm tập hợp vào `submission/qc/image_issues.csv`. Mã annotator của tôi là `150`.

Ảnh không có đối tượng hợp lệ vẫn phải có trong Task và danh sách `images` của COCO, không tạo box để đủ số lượng. Khi gán độc lập, chỉ dùng guideline v1.0 đã khóa và không xem nhãn thành viên khác.

## 4. Ca khó

Các quyết định dưới đây là đề xuất để người viết tự xác nhận trên ảnh gốc. Số box nêu cho cụm được mô tả, không phải tổng box cả ảnh. Chưa xác nhận tổng số đối tượng hoặc tọa độ.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_001.jpg` | Bán tải cạnh người đứng, người phía sau bị bàn và xe che. | R-01, R-03 | Xe là `truck`; tách người đủ điều kiện, chỉ bao phần nhìn thấy. | Không nhầm che khuất với cắt mép. |
| `img_002.jpg` | Xe vận chuyển chở nhiều ô tô. | R-05 | Gán riêng xe vận chuyển và từng xe thật đủ điều kiện. | Không gộp nhiều vật thành một box. |
| `img_004.jpg`, `img_035.jpg` | Tuk-tuk; có xe chở hàng cao. | R-01, R-05 | Đề xuất `tuk_tuk`; không bao hàng chở rời. | Kết cấu xe khác mô tô hai bánh. |
| `img_005.jpg` | Người và xe máy che lẫn nhau, van phía sau. | R-02, R-03, R-04 | Tách người, xe; gán mức che theo từng đối tượng. | Không lấy mức che chung cho cả cụm. |
| `img_006.jpg`, `img_023.jpg`, `img_039.jpg` | Xe đạp hoặc xích lô cùng người trong cảnh. | R-01, R-04 | Không gán phương tiện ngoài phạm vi; vẫn gán người đủ điều kiện. | Loại phương tiện không đồng nghĩa loại người. |
| `img_009.jpg`, `img_037.jpg`, `img_040.jpg` | Xe buýt hoặc xe khách xuất hiện trong cảnh. | R-01, R-08 | Đề xuất lớp `bus`, kiểm chiều cao trước khi gán. | Không ép vào `van` hoặc `truck`. |
| `img_011.jpg` | Nhân vật Predator và xe trang trí. | R-06, R-11 | Cần review bản chất nhân vật và phương tiện chưa xác định. | Không đủ căn cứ mặc định mọi vật là tượng hoặc đều là vật thật. |
| `img_014.jpg` | Người đi bộ rõ hơn các phương tiện nhòe phía sau. | R-10 | Gán vật nhận dạng được; ghi vấn đề cho ca không xác định được box. | Không suy ra ranh giới từ vệt chuyển động. |
| `img_015.jpg`, `img_040.jpg` | Đối tượng bị cắt ở mép ảnh. | R-03 | Box dừng ở mép, đặt `truncated=yes` nếu mất một phần ngoài ảnh. | Chạm mép khác bị cắt mất phần. |
| `img_017.jpg`, `img_027.jpg` | Tượng người cưỡi ngựa và tượng bán tải. | R-06 | Không gán các tượng. | Là vật mô phỏng người hoặc xe. |
| `img_018.jpg`, `img_033.jpg`, `img_038.jpg` | Chân dung quảng cáo, ma-nơ-canh, xe đồ chơi. | R-06 | Không gán các vật mô phỏng. | Không phải người hoặc phương tiện thật trong cảnh. |
| `img_019.jpg` | Xe diễu hành màu vàng với nhân vật hoạt hình. | R-06, R-11 | Cần review xe thật hay mô hình; nếu xác nhận xe thật thì xét `car`, người thật xét riêng. | Thiết kế hóa trang chưa đủ để loại xe. |
| `img_020.jpg` | Cảnh phản chiếu qua gương xe. | R-06, R-07 | Không gán hình trong gương hoặc bộ phận xe chủ. | Tránh gán nhầm phản chiếu thành đối tượng trực tiếp. |
| `img_021.jpg`, `img_025.jpg`, `img_030.jpg`, `img_032.jpg` | Người hoặc xe dày đặc, có vật ở xa. | R-08, R-09 | Tách vật rõ, đủ lớn; ignore gọn phần không tách được. | Không che mất vật hợp lệ trong vùng ignore. |
| `img_022.jpg` | Mô tô sidecar. | R-05 | Một box `motorcycle` cho tổ hợp gắn liền; người nếu có xét riêng. | Không nhầm sidecar với tuk-tuk. |
| `img_024.jpg` | Xe bên dưới và vật hình xe trên nóc. | R-05, R-06, R-11 | Gán xe thật bên dưới; review bản chất vật trên nóc trước khi chốt. | Không tự coi vật được chở là một xe vận hành độc lập. |
| `img_026.jpg` | Hai người trên một xe máy. | R-03, R-04 | Đề xuất 2 box `person` và 1 box `motorcycle` cho cụm tiền cảnh, nếu đủ điều kiện. | Người và xe là các đối tượng riêng. |
| `img_028.jpg`, `img_029.jpg` | Bán tải chở tượng ngựa; xe máy chở thanh dài. | R-05, R-06 | Không kéo box xe để bao tượng hoặc thanh dài; người xét riêng. | Tách phương tiện khỏi hàng chở rời. |
| `img_037.jpg` | Bán tải có nắp thùng cao, cạnh xe buýt. | R-01, R-05 | Bán tải là `truck` nếu nhận ra kết cấu; xe buýt là đối tượng riêng. | Nắp thùng không tự đổi lớp xe. |

Ca chưa chốt không được ghi như quyết định đã được nhóm duyệt. Khi họp, dùng ID ảnh và Rule ID để nêu điểm khác nhau; giữ nguyên bản cá nhân sau khi đã nộp, ghi quyết định chung vào guideline nhóm riêng.

## 5. QC và phiên bản

### Kiểm tra trước khi nộp nhãn

Tự xem lại vật bỏ sót, box thừa hoặc trùng, lớp, ranh giới và thuộc tính. Xuất COCO 1.0 từ CVAT, tắt Save images; lưu JSON annotation thành `submission/labels/150.json`, rồi chạy:

```powershell
python scripts/validate_labels.py submission/labels/150.json
```

Validator kiểm định dạng, tập ảnh, lớp, thuộc tính và hình học box. Việc box có đúng vật, có ôm sát vật hoặc cả nhóm có cùng bỏ sót hay không vẫn cần người xem ảnh.

### Ngưỡng QC áp dụng

Giữ nguyên mục `rules` của `submission/taxonomy.json`; không thay ngưỡng để làm số liệu đạt.

| Tiêu chí | Cách tính / ngưỡng |
|---|---|
| Chiều cao tối thiểu box đối tượng | 20 px trên ảnh gốc. |
| Ghép box IAA | Ghép 1–1, không phân biệt lớp, IoU ít nhất 0,5. |
| IoU theo kích thước | Box cao từ 50 px: ít nhất 0,85; dưới 50 px: ít nhất 0,70. |
| IAA | IoU trung bình ít nhất 0,85; đồng thuận lớp ít nhất 95%, chỉ trên cặp ghép được. |
| Độ phủ | Hoàn thành 100% lượt gán trong `assignment.csv`. |
| Lỗi theo ảnh | Số ảnh có ít nhất một lỗi / số ảnh đã duyệt; tối đa 2%. |
| Lỗi theo đối tượng | Số annotation đối tượng bị lỗi / số annotation đối tượng đã duyệt; vật bỏ sót ghi riêng. |

Báo cáo ghi tử số và mẫu số. Không có cặp ghép thì IAA là N/A. Giữ số liệu trước calibration; đồng thuận cao chưa chứng minh nhãn đúng vì mọi người có thể cùng bỏ sót hoặc hiểu sai.

Duyệt toàn bộ 40 ảnh để xét bàn giao. Một ảnh lỗi là 1/40 = 2,5%, vượt ngưỡng 2%. Xét theo thứ tự: **Hold** khi thiếu bằng chứng hoặc còn vấn đề guideline/dữ liệu; **Rework** khi vượt ngưỡng hoặc có lỗi lặp; **Release** khi đủ bằng chứng đạt yêu cầu và reviewer xác nhận. Script chỉ gợi ý quyết định, không thay người duyệt.

### Người chốt ca mơ hồ và quản lý phiên bản

Thành viên `150` ghi câu hỏi và đề xuất, không tự thay quy tắc giữa lượt gán độc lập. Nhóm thống nhất ở pha 2 và calibration pha 5; người chốt và reviewer cuối theo phân công trong `TEAM.md`. Mỗi ca sửa phải có quyết định, Rule ID, phiên bản, người sửa và người kiểm lại; ưu tiên người kiểm khác người sửa.

Sau khi calibration, chỉ sửa câu chữ mà không đổi cách gán thì ghi `editorial`. Thay đổi cách chọn vật, lớp, box hoặc thuộc tính là `semantic`, phải ghi phạm vi `lo` và kiểm lại cả lô. Sửa nhãn sau QC phải mở vòng mới, giữ bằng chứng vòng cũ.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| `v0` | Guideline khởi đầu của lab. | Chưa rõ cách tách người và xe, mức che và xử lý vật mô phỏng. |
| `v0.1-individual` | Bản đề xuất cá nhân mã `150` theo template đủ 5 phần; làm rõ lớp, thuộc tính và 11 quy tắc. | Các ca người trên xe ở `img_026`, xe chở xe ở `img_002`, tượng ở `img_017` và `img_027`, sidecar ở `img_022`, bán tải ở `img_037`. |

Trước khi nộp bản cá nhân, thành viên `150` tự xác nhận các đề xuất trên bộ ảnh và ghi cách dùng AI, cách kiểm lại trong ghi chú cá nhân. Không điền số box, số đo IAA hoặc kết quả QC khi chưa thực hiện.
