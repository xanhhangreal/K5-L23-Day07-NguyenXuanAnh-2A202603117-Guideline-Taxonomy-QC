# Guideline v1.1 — bản bàn giao có hỗ trợ AI, chờ xác nhận nhóm

Bản này giữ nghĩa R-01–R-13 và taxonomy v1.0. Không ghi nhận một cuộc họp calibration hoặc chữ ký thành viên chưa diễn ra. Nhật ký quyết định là đề xuất của AI, các vùng chưa chắc giữ can_review; trạng thái bàn giao Hold.

## Làm rõ từ lần đối chiếu 40 ảnh

- Mỗi người thật có một box; không gộp hai khuôn mặt vào một box người (img_001), không gán cả đầu riêng lẫn toàn thân cho cùng người (img_016).
- Box phương tiện gồm phần kết cấu nhìn thấy; xe vận chuyển gồm rơ-moóc (img_002). Hàng hóa rời không thuộc box.
- Xe khoang kín liền thân và xe cabin/thùng riêng phân lớp theo R-01; khi ảnh chưa đủ rõ giữ can_review.
- Xe đồ chơi trong tủ img_038, tượng img_017/img_027 và hình phản chiếu img_020/img_033 không thuộc vật mục tiêu.
- Mức che khác cắt mép. Không suy mức che 0 chỉ từ box không chạm vật khác; xét phần cơ thể/kết cấu bị che trong ảnh.
- Vật nhìn thấy cao dưới 20 px dùng ignore_region theo R-09, không giữ như đối tượng chỉ để tăng số box.

Các ví dụ trên là áp dụng quy tắc cũ; chưa thay taxonomy hoặc ngưỡng. Bên dưới giữ nội dung v1.0 để tra cứu, hồ sơ khóa v1.0 gốc không sửa.

---

# Guideline gán nhãn — v1.0 — Nhóm xanh đỏ

- Ngày chuẩn bị: 16/11/2026.
- Thành viên: `084`, `117`, `133`, `150`.
- Nguồn tổng hợp: guideline cá nhân `117`, `133`, `150` trên commit `2a04969`.
- Trạng thái: **đã khóa v1.0 cho lượt gán độc lập**.
- Căn cứ khóa: người điều phối yêu cầu trong chat ngày 16/11/2026: bỏ qua guideline 084, chốt bản tổng hợp và chia task cho mọi người.
- Guideline 084 không nằm trong nguồn tổng hợp; thành viên 084 vẫn tham gia gán nhãn. Không ghi nhận thay cho xác nhận riêng của từng thành viên hoặc một cuộc họp chưa diễn ra.
- Phạm vi: 40 ảnh, `img_001.jpg` đến `img_040.jpg`; CVAT Rectangle, COCO 1.0.

Các khác biệt và cách xử lý đã chọn được ghi tại `phase2_comparison.md`. Rule ID dưới đây dùng cho bản nhóm, độc lập với mã trong từng bản cá nhân. Từ lúc bắt đầu lượt độc lập, không sửa bản này hoặc taxonomy; đề xuất thay đổi được giữ lại cho calibration v1.1.

## 1. Mục tiêu

Tạo nhãn cho mô hình phát hiện người và phương tiện trên ảnh đường phố 2D. Mỗi vật hợp lệ có một box, một lớp và các thuộc tính mô tả tình trạng quan sát. Ưu tiên không bỏ sót người/xe, không gán nhầm vật mô phỏng và giữ box sát phần nhìn thấy.

Chỉ dùng bằng chứng quan sát được; không suy đoán số ghế, động cơ đang hoạt động, danh tính, vận tốc hoặc phần vật thể bị che hoàn toàn. Bộ nhãn này không yêu cầu vật đang di chuyển: xe thật đang đỗ hay được vận chuyển vẫn được xét.

## 2. Lớp và thuộc tính

### Lớp

**R-01 — Chọn lớp theo kết cấu nhìn thấy.** Mỗi vật nhận đúng một lớp. Không ép vật ngoài phạm vi vào lớp gần giống; không thêm lớp giữa lượt gán độc lập.

| Lớp | Định nghĩa | Ví dụ tham chiếu từ bản cá nhân | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con gồm sedan, hatchback, wagon và SUV, không có thùng hàng riêng kiểu bán tải. | Ô tô ở `img_015`; xe thật được chở ở `img_002`. | Bán tải là truck; mô hình đồ chơi không gán. |
| `truck` | Xe chở hàng có cabin và khu vực hàng riêng, gồm xe tải, đầu kéo và bán tải. | Xe vận chuyển ở `img_002`, xe tải nhỏ ở `img_036`. | Van có khoang kín liền thân; không đổi bán tải thành van chỉ vì gắn nắp thùng. |
| `van` | Xe dạng van có khoang người/hàng kín liền thân với khoang lái. | Van được nêu ở `img_005`. | SUV là car; cabin tách thùng là truck. |
| `motorcycle` | Xe máy, xe tay ga hoặc mô tô, gồm mô tô gắn sidecar theo R-11. | Xe ở `img_026`, sidecar ở `img_022`. | Xe đạp, xích lô không động cơ và tuk-tuk thân ba bánh riêng. |
| `person` | Người thật trong cảnh, gồm người đi bộ, người ngồi và người trên phương tiện. | Người bán hàng ở `img_003`, người trên xe ở `img_026`. | Tượng, ma-nơ-canh, hình in và hình phản chiếu. |
| `bus` | Xe có kết cấu nhận dạng được là xe buýt hoặc xe khách. | Xe khách ở `img_009`, xe buýt ở `img_037`. | Van; không tự suy ra số ghế không nhìn thấy để phân lớp. |
| `tuk_tuk` | Xe ba bánh có động cơ kiểu tuk-tuk/auto rickshaw với vị trí lái và khoang khách hoặc hàng phía sau. | `img_004`, `img_035`. | Xích lô đạp chân; mô tô có sidecar gắn thêm. |
| `ignore_region` | Vùng kỹ thuật chứa vật mục tiêu quá nhỏ hoặc cụm không tách tin cậy. | Cụm xa được nêu ở `img_025`. | Không dùng như lớp cho mọi vật lạ hoặc để bỏ qua vật lớn rõ. |

Xe đạp, xích lô không động cơ, động vật và đồ dùng sinh hoạt ngoài phạm vi lớp đối tượng. Người thật trên phương tiện ngoài phạm vi vẫn xét riêng. Các ví dụ ảnh là dẫn chiếu từ tài liệu cá nhân, không xác nhận tổng số vật hoặc box trong ảnh.

### Thuộc tính

Mỗi box đối tượng có đủ ba thuộc tính; `ignore_region` không cần thuộc tính đối tượng.

| Thuộc tính | Giá trị | Nghĩa |
|---|---|---|
| `occluded_level` | `0` | Không bị vật khác che: 0%. |
| `occluded_level` | `1` | Bị che trên 0% đến hết 30%. |
| `occluded_level` | `2` | Bị che trên 30% đến hết 70%. |
| `occluded_level` | `3` | Bị che trên 70% nhưng vẫn nhận dạng được lớp. |
| `truncated` | `no`, `yes` | yes khi một phần vật nằm ngoài ảnh; chỉ chạm mép nhưng thấy trọn vật thì no. |
| `can_review` | `false`, `true` | true khi cần xác nhận lớp, ranh giới, thuộc tính hoặc bản chất vật. |

**R-02 — Che khuất khác cắt mép.** Ước lượng phần bị vật khác che trên hình dạng chiếu 2D dự kiến của phần đối tượng nằm trong ảnh. Phần ngoài ảnh chỉ tính vào truncated. Hai thuộc tính có thể cùng xuất hiện. Không đặt ngưỡng loại riêng 90%; chỉ gán khi nhận dạng được và đủ kích thước. Không dùng mức 3 thay nghĩa “không biết”, không dùng cờ occluded có sẵn của CVAT thay occluded_level.

## 3. Quy tắc vẽ box

### R-03 — Ôm sát phần nhìn thấy

Dùng hình chữ nhật theo trục ảnh, sát các điểm ngoài cùng nhìn thấy, không thêm đệm và không dựng phần khuất. Gồm các phần gắn với vật như bánh xe, gương, tay lái, mũ bảo hiểm đang đội; không bao bóng đổ hay vật bên cạnh. Một vật lộ thành nhiều phần vẫn một box nếu chắc cùng vật, khoảng giữa có thể chứa nền hoặc vật che. Không ghép khi thiếu căn cứ.

COCO dùng bbox XYWH `[x_min, y_min, width, height]` theo pixel ảnh gốc. Khi trao đổi bằng XYXY, phải đổi `width=x_max-x_min`, `height=y_max-y_min`; không ghi trực tiếp XYXY hoặc tọa độ chuẩn hóa vào bbox COCO.

### R-04 — Vật bị che hoặc cắt mép

Gán nếu nhận dạng được lớp và box phần nhìn thấy cao ít nhất 20 px. Box nằm trong ảnh, dừng ở biên khi bị cắt. Không gán vật bị che hoàn toàn; không suy đoán một vật chỉ từ ngữ cảnh. Thiếu căn cứ đặt box thì ghi vấn đề cấp ảnh.

### R-05 — Người trên phương tiện

Tách từng người và phương tiện. Một người trên một xe máy có hai box; hai người trên một xe có ba box cho cụm đó, nếu từng vật đủ điều kiện. Box xe không bao người, box người không bao cả xe. Quy tắc này áp dụng cả người trên xe đạp hoặc xích lô dù phương tiện ngoài phạm vi. Khi tự gán `img_005` hoặc `img_026`, áp dụng cùng nguyên tắc; số box cả ảnh phụ thuộc các đối tượng thực tế đủ điều kiện.

### R-06 — Xe chở xe

Xe vận chuyển và từng xe thật được chở là các đối tượng riêng nếu đủ điều kiện. Box xe vận chuyển gồm cabin và khung chở thuộc chính xe; không kéo box theo điểm ngoài cùng của xe hàng. Box từng xe được chở không bao giá đỡ hoặc xe cạnh bên. Không cố định số box theo mô tả tài liệu; kiểm từng vật trên ảnh.

### R-07 — Vật mô phỏng, hóa trang, kính và phản chiếu

Loại tượng, ma-nơ-canh, đồ chơi, hình in và vật chỉ thấy qua phản chiếu. Vật thật nhìn xuyên kính vẫn xét bình thường. Người thật hóa trang vẫn là person; xe thật có trang trí lạ không tự động bị loại. Không xác định bản chất chỉ từ ngoại hình hoặc tên ảnh. Với `img_011`, `img_019`, `img_024`, mỗi người áp dụng quy tắc này độc lập: có căn cứ đặt box nhưng chưa chắc thì bật can_review; không có căn cứ đặt box thì ghi vấn đề cấp ảnh theo R-10. Giữ ca đó để calibration, không hỏi nhãn người khác giữa lượt độc lập.

### R-08 — Xe chủ

Không gán phần xe gắn camera như ca-pô và gương khi xác định được là xe chủ. Không mặc định mọi xe sát mép dưới là xe chủ. Hình trong gương theo R-07.

### R-09 — Vật nhỏ và đám đông

Đo chiều cao box phần nhìn thấy trên ảnh gốc. Từ 20 px trở lên, nhận dạng được và tách được thì gán riêng; đúng 20 px đủ điều kiện. Dưới 20 px hoặc cụm không tách tin cậy thì dùng ignore_region bao gọn vùng cần bỏ qua. Tách trước các vật lớn rõ; không phủ vùng ignore lên chúng để giảm thao tác. Vật ngoài taxonomy không tự động trở thành ignore_region.

### R-10 — Ca chưa chắc, độc lập và ảnh trống

Đặt được box có căn cứ nhưng còn nghi ngờ thì bật can_review và ghi lý do. Chưa đặt được box thì ghi `image,annotator,region,note` để nhóm tập hợp vào `submission/qc/image_issues.csv` sau khi khóa nhãn độc lập. Ảnh không có vật vẫn có trong Task và danh sách images của COCO, không tạo box giả. Trong lượt độc lập chỉ dùng v1.0 đã khóa, không xem nhãn của nhau và không tự đổi quy tắc.

### R-11 — Mô tô sidecar

Mô tô và sidecar gắn liền là một motorcycle; box bao phần nhìn thấy của cả tổ hợp. Không gán thêm box phương tiện riêng cho sidecar; người xét riêng theo R-05. Tuk-tuk có thân xe ba bánh riêng thuộc tuk_tuk.

### R-12 — Hàng hóa và bộ phận xe rời

Không bao hàng chở rời, bao tải, thanh dài hoặc tượng trang trí vào box phương tiện. Thùng xe, nắp thùng, khung cố định thuộc kết cấu xe được tính vào box. Vỏ xe cắt rời là hàng, không phải xe độc lập; xe thật được vận chuyển theo R-06. Bán tải có nắp cao vẫn truck khi nhận ra kết cấu bán tải; không đoán kết cấu nếu chưa rõ.

### R-13 — Vật bị mờ

Vẫn gán nếu nhận dạng được lớp và đặt được ranh giới phần nhìn thấy tin cậy. Không lấy cả vệt chuyển động làm đường bao. Nếu chưa xác định được ranh giới, ghi vấn đề để review thay vì tạo box đoán.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Cách xử lý trong bản tổng hợp | Lý do / việc chưa chốt |
|---|---|---|---|---|
| `img_002` | Xe chở ô tô. | R-06 | Tách xe vận chuyển và từng xe thật đủ điều kiện. | Không gộp vật; số lượng cần kiểm trên ảnh. |
| `img_004`, `img_035` | Tuk-tuk, xe chở hàng. | R-01, R-12 | Tuk_tuk; không bao hàng rời. | Ba bản đều đề nghị thêm lớp. |
| `img_005`, `img_026` | Người trên xe máy. | R-05 | Tách từng người và xe; box chỉ phần nhìn thấy. | Hai người/một xe có ba box cho cụm nếu đủ điều kiện. |
| `img_006`, `img_023`, `img_039` | Xe đạp, xích lô. | R-01, R-05 | Không gán phương tiện; xét người riêng. | Ngoài bộ lớp phương tiện nhưng không loại người. |
| `img_009`, `img_037`, `img_040` | Xe buýt/khách. | R-01 | Bus khi nhận dạng được và đủ kích thước. | Không dựa vào số ghế suy đoán. |
| `img_011` | Nhân vật Predator. | R-07, R-10 | Người thật thì person; tượng thì loại; chưa chắc thì can_review hoặc ghi vấn đề cấp ảnh. | Người gán tự quyết định theo ảnh, giữ ca mơ hồ cho calibration. |
| `img_017`, `img_027` | Tượng người hoặc xe. | R-07 | Không gán tượng. | Không phải đối tượng thật mục tiêu. |
| `img_018`, `img_033`, `img_038` | Hình quảng cáo, ma-nơ-canh, đồ chơi. | R-07 | Không gán vật mô phỏng; xét vật thật khác riêng. | Phân biệt vật thật nhìn xuyên kính. |
| `img_019` | Xe diễu hành. | R-07, R-10 | Xe thật có trang trí vẫn xét lớp theo kết cấu; mô hình thì loại; chưa chắc theo R-10. | Không loại xe chỉ do hình dáng hóa trang. |
| `img_020` | Phản chiếu và gương xe chủ. | R-07, R-08 | Loại hình phản chiếu và bộ phận xe chủ. | Không gán đối tượng gián tiếp trong gương. |
| `img_022` | Mô tô sidecar. | R-11 | Một motorcycle gồm sidecar gắn liền. | Sidecar không là một phương tiện độc lập. |
| `img_024` | Vật hình xe trên nóc. | R-06, R-12 | Vỏ rời thì loại; xe thật được chở thì xét riêng; chưa chắc theo R-10. | Không suy đoán bản chất vật chỉ từ mô tả tài liệu. |
| `img_029` | Các bản mô tả phương tiện/hàng khác nhau. | R-01, R-12 | Kiểm ảnh trước khi chọn lớp; không bao hàng rời. | Không coi mô tả mâu thuẫn là sự thật đã kiểm. |
| `img_037` | Bán tải nắp cao. | R-01, R-12 | Truck nếu nhận ra kết cấu bán tải; chưa rõ thì review. | Quy tắc theo kết cấu, không theo riêng nắp thùng. |

## 5. QC và phiên bản

### Kiểm tra và ngưỡng

Trước export: kiểm bỏ sót, box thừa/trùng, lớp, ranh giới và ba thuộc tính. Export COCO 1.0, tắt Save images; lưu JSON annotation vào `submission/labels/<mã>.json`. Kiểm bằng `python scripts/validate_labels.py submission/labels/<mã>.json`; validator không xác minh được vật thật hoặc phần cả nhóm cùng bỏ sót.

| Tiêu chí | Ngưỡng / cách tính |
|---|---|
| Chiều cao tối thiểu | 20 px. |
| Ghép IAA | 1–1 không phân biệt lớp, IoU ≥ 0,5. |
| IoU theo kích thước | Cao ≥ 50 px: 0,85; nhỏ hơn: 0,70. |
| IAA | IoU trung bình ≥ 0,85; đồng thuận lớp ≥ 95%, trên cặp ghép được. |
| Độ phủ | 100% lượt trong assignment.csv. |
| Lỗi theo ảnh | Ảnh có ít nhất một lỗi / ảnh đã duyệt; ≤ 2% để xét Release. |
| Lỗi theo đối tượng | Annotation đối tượng lỗi / annotation đối tượng đã duyệt; bỏ sót ghi riêng. |

Giữ nguyên tám giá trị rules của lab. Báo số lượng và mẫu số; không có cặp thì IAA N/A. Giữ IAA trước calibration. Duyệt toàn bộ 40 ảnh để bàn giao: 1/40 lỗi = 2,5%, vượt ngưỡng. Hold khi thiếu bằng chứng hoặc còn vấn đề guideline/dữ liệu; Rework khi lỗi vượt ngưỡng hoặc lặp; Release khi bằng chứng đạt và reviewer xác nhận.

### Người chốt và phiên bản

Điều phối theo TEAM.md; 133 ghi vai trò reviewer cuối trong bản cá nhân, phân công reviewer chính thức thực hiện theo TEAM.md. Ca calibration phải có người chốt bằng mã ba chữ số, quy tắc, chỗ sửa và người kiểm lại. Không ghi đã họp hoặc đã review khi chưa làm. Việc khóa v1.0 căn cứ chỉ đạo của người điều phối trong chat, không phải kết quả QC.

Sau lượt độc lập: câu chữ đổi nhưng nghĩa giữ nguyên là editorial; cách chọn vật/lớp/box/thuộc tính đổi là semantic, ghi phạm vi lo và rà cả lô. Lưu bản v1.1 riêng, giữ nguyên bản cá nhân và v1.0. Nhãn cuối đổi sau QC phải mở vòng mới, giữ bằng chứng vòng cũ.

| Phiên bản | Thay đổi | Lý do / trạng thái |
|---|---|---|
| v0 | Năm lớp đối tượng và ignore; quy tắc sơ lược. | Bản starter giữ nguyên. |
| Cá nhân 117, 133, 150 | Các cách làm rõ v0 độc lập. | Giữ nguyên file đã nộp; bỏ qua bản 084 khi tổng hợp theo yêu cầu người điều phối. |
| v1.0 — đã khóa | Bổ sung bus/tuk_tuk; chốt định nghĩa lớp, khoảng che và R-01–R-13, gồm cách chuyển ca mơ hồ sang calibration. | Khóa theo yêu cầu người điều phối ngày 16/11/2026 để bắt đầu lượt độc lập cho bốn thành viên. |

Mã băm của guideline, taxonomy, cấu hình CVAT và bảng phân công được ghi tại `guideline_v1.0_lock.json`. Dùng đúng cấu hình và phân công này để tạo Task. Không sửa v1.0 trong lượt độc lập; sau khi mọi người nộp riêng, xử lý ca mơ hồ và thay đổi quy tắc ở pha calibration.
