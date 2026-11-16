# Guideline gán nhãn — v0.1-individual — Mã 133

- Phiên bản: `v0.1-individual`
- Ngày: 2026-11-16
- Người viết: Thành viên 133 (Vai trò: Reviewer cuối bản nhãn)

---

## 1. Mục tiêu

Nhãn bounding box 2D được xây dựng nhằm mục đích huấn luyện và đánh giá mô hình học sâu phát hiện vật thể (Object Detection) trên ảnh đường phố, phục vụ các hệ thống hỗ trợ lái xe nâng cao (ADAS) và camera giám sát giao thông thông minh.

- **Yêu cầu an toàn và hệ quả sai sót:**
  - **Bỏ sót (False Negative):** Là lỗi nghiêm trọng nhất. Nếu mô hình bỏ sót người đi bộ (`person`), xe máy (`motorcycle`) hoặc ô tô phía trước (`car`, `truck`), hệ thống có thể gây ra tai nạn giao thông nghiêm trọng.
  - **Gán nhầm / Báo động giả (False Positive):** Nếu gán nhãn cho các vật thể không có thực như hình người/xe trên biển quảng cáo (`img_018.jpg`), tượng đài điêu khắc (`img_017.jpg`, `img_027.jpg`), ma-nơ-canh trong tủ kính (`img_033.jpg`) hoặc bóng phản chiếu qua gương (`img_020.jpg`), hệ thống xe tự lái sẽ có hiện tượng phanh gấp vô cớ (phantom braking), gây nguy cơ tai nạn từ phương tiện phía sau.
  - **Sai lệch kích thước / ranh giới (Poor Bbox):** Vẽ box không ôm sát phần nhìn thấy hoặc ôm trùm cả hàng hóa cồng kềnh vượt khổ (`img_035.jpg`, `img_029.jpg`) sẽ khiến mô hình ước lượng sai khoảng cách và kích thước hình học của phương tiện.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (Classes)
Áp dụng phép thử: *"Mô hình phát hiện vật 2D có phải phân biệt lớp này khi suy luận thực tế không?"*
Bản v0 chỉ có 5 lớp cơ bản (`car`, `truck`, `van`, `motorcycle`, `person`) và `ignore_region`. Dựa trên việc khảo sát 40 ảnh thực tế, tôi đề xuất mở rộng và làm rõ các lớp:

| Lớp | Định nghĩa (một câu) | Ví dụ minh họa trong 40 ảnh | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con chở người từ 4–9 chỗ, sedan, hatchback, SUV, coupe. | Ô tô con đang chạy (`img_005.jpg`, `img_015.jpg`, `img_040.jpg`), 8 ô tô trên sàn xe chuyên chở (`img_002.jpg`). | Tượng đài xe bán tải bằng đá (`img_027.jpg`), mô hình đồ chơi (`img_038.jpg`), xe diễu hành đồ chơi giả tưởng (`img_019.jpg`). |
| `truck` | Xe ô tô tải chở hàng, xe đầu kéo, có khoang lái tách biệt với sàn/thùng chở hàng. | Xe tải chở ô tô Renault (`img_002.jpg`), xe tải nhỏ trong nhà kho (`img_007.jpg`), xe tải cabin liền thùng hở CMC Veryca (`img_036.jpg`). | Xe ba bánh chở hàng (`img_035.jpg`), xe bán tải gắn nắp thùng kín cao ngang cabin (`img_037.jpg`). |
| `van` | Xe ô tô thân hộp (box-shaped), khoang lái liền khối với khoang hàng/khoang hành khách. | Xe van giao hàng, xe cứu thương cỡ nhỏ, xe minivan gia đình. | Xe tải thùng hở (`img_001.jpg`), xe khách/xe buýt lớn chở trên 16 người (`img_032.jpg`). |
| `bus` *(Đề xuất thêm)* | Xe buýt công cộng hoặc xe khách đường dài cỡ lớn chở nhiều người (> 16 chỗ ngồi). | Xe buýt công cộng ETS (`img_032.jpg`), xe buýt đường phố Bangkok (`img_040.jpg`), xe khách lớn (`img_009.jpg`, `img_031.jpg`). | Xe van nhỏ 9 chỗ, xe con 7 chỗ. |
| `tuk_tuk` *(Đề xuất thêm)* | Xe cơ giới 3 bánh có động cơ, có cabin chở khách hoặc chở hàng đặc thù. | Xe tuk-tuk tại Pattaya (`img_004.jpg`), tuk-tuk Bangkok (`img_016.jpg`), xe auto rickshaw chở hàng (`img_035.jpg`). | Xe xích lô đạp chân (`img_006.jpg`, `img_023.jpg`), xe máy 2 bánh (`img_005.jpg`). |
| `motorcycle` | Phương tiện cơ giới hai bánh có động cơ (xe máy, xe tay ga, mô tô, xe gắn máy có thùng phụ sidecar). | Xe tay ga và xe số trên đường phố TP.HCM (`img_005.jpg`, `img_008.jpg`, `img_030.jpg`), xe mô tô sidecar (`img_022.jpg`). | Xe đạp thông thường (`img_003.jpg`, `img_006.jpg`), xe xích lô đạp chân (`img_023.jpg`, `img_034.jpg`). |
| `person` | Con người thật còn sống (người đi bộ, người đứng, người ngồi, người điều khiển hoặc hành khách trên xe). | Người phụ nữ đứng cạnh xe bán tải (`img_001.jpg`), người điều khiển xe máy (`img_005.jpg`, `img_026.jpg`), người bán hàng rong (`img_003.jpg`, `img_010.jpg`), người đi bộ trên vỉa hè (`img_025.jpg`). | Tượng người cưỡi ngựa (`img_017.jpg`), ma-nơ-canh trong tủ kính (`img_033.jpg`), mặt người trên pano quảng cáo (`img_018.jpg`), búp bê đồ chơi (`img_038.jpg`). |
| `ignore_region` | Vùng không đánh giá độc lập: nơi tập trung cụm vật quá nhỏ (< 20 px) hoặc đám đông mờ nhòe cực xa không thể tách rời. | Đám đông người và xe ở cực xa phía chân trời (`img_025.jpg`, `img_040.jpg`). | Bất kỳ đối tượng đơn lẻ nào có chiều cao $\ge 20\text{ px}$ nhìn thấy rõ. |

**Quy tắc đối với vật không thuộc lớp nào:**
- Phương tiện thô sơ không động cơ (xe đạp, xe xích lô đạp chân: `img_003.jpg`, `img_006.jpg`, `img_021.jpg`, `img_023.jpg`, `img_034.jpg`, `img_039.jpg`): **KHÔNG gán nhãn cho phương tiện**. CHỈ gán nhãn `person` cho người điều khiển và hành khách ngồi trên đó.
- Động vật (ngựa, chim bồ câu: `img_017.jpg`, `img_028.jpg`): **KHÔNG gán**.

---

### 2.2. Thuộc tính (Attributes) với ngưỡng đo lường định lượng

Bản v0 dùng các từ ngữ định tính mơ hồ ("che ít", "che nhiều", "không rõ"). Để đảm bảo hai annotator độc lập chấm giống nhau, các thuộc tính được quy định với ngưỡng định lượng cụ thể:

1. **`occluded_level` (Mức độ bị che khuất bởi vật thể khác hoặc thành phần môi trường):**
   - `0`: Không bị che khuất ($0\%$ diện tích bị che). Toàn bộ biên dạng nhìn thấy trọn vẹn.
   - `1`: Bị che khuất nhẹ (từ $1\%$ đến $30\%$ diện tích đối tượng bị che). Hầu hết các đặc trưng nhận diện vẫn nhìn rõ.
   - `2`: Bị che khuất trung bình (từ $31\%$ đến $70\%$ diện tích đối tượng bị che). Chỉ nhìn thấy một phần, cần ngữ cảnh để nhận diện.
   - `3`: Bị che khuất nặng (trên $70\%$ diện tích đối tượng bị che, nhưng vẫn nhận dạng chắc chắn đối tượng nhờ phần lộ diện).
   - *Lưu ý:* Nếu đối tượng bị che khuất $> 90\%$ đến mức không thể xác định chắc chắn đặc trưng thì **KHÔNG gán box**.

2. **`truncated` (Cắt mép bởi khung hình ảnh):**
   - `no`: Toàn bộ đối tượng nằm trọn vẹn bên trong khung hình ảnh.
   - `yes`: Đối tượng bị cắt một phần do chạm vào ít nhất một mép ảnh (trên, dưới, trái, phải).

3. **`can_review` (Đánh dấu ca nghi vấn / cần thảo luận):**
   - `false` (mặc định): Tự tin về nhãn và ranh giới box theo guideline.
   - `true`: Gặp tình huống biên mơ hồ hoặc chưa chắc chắn, cần đưa ra thảo luận tại buổi họp calibration Pha 2 / Pha 5.

---

## 3. Quy tắc vẽ Bounding Box

- **R-01 — Ôm sát phần nhìn thấy (Tight to visible bounding box):**
  - Bounding box phải là hình chữ nhật đứng (axis-aligned bounding box), ôm khít phần nhìn thấy thực tế của vật thể. Không mở rộng box để bao trùm không gian trống hoặc phần suy đoán bị che khuất.
- **R-02 — Người đi xe máy (Motorcycle Rider):**
  - Tách thành 2 box riêng biệt có chồng lấn (overlap):
    - 1 box `person` ôm từ đỉnh đầu/mũ bảo hiểm đến chân/vị trí đặt chân nhìn thấy của người lái.
    - 1 box `motorcycle` ôm toàn bộ chiếc xe máy (bánh xe, ống xả, thân xe, đầu xe).
    - Nếu có hành khách ngồi sau: vẽ thêm 1 box `person` riêng cho hành khách đó.
- **R-03 — Xe chở ô tô (Car Carrier - `img_002.jpg`):**
  - Gán 1 box `truck` bao toàn bộ xe chuyên chở (cabin + khung giá chở hàng).
  - Gán các box `car` riêng lẻ cho từng chiếc ô tô con nằm trên giá đỡ nếu nhận diện rõ đặc trưng xe con và không bị che khuất hoàn toàn.
- **R-04 — Hàng hóa cồng kềnh chở trên phương tiện (`img_012.jpg`, `img_029.jpg`, `img_035.jpg`):**
  - Box phương tiện CHỈ ôm sát khung thân vật lý của xe (bánh xe, cabin, sườn xe), **KHÔNG kéo dãn box để bao trùm khối hàng hóa cồng kềnh vượt khổ** trên nóc hoặc phía sau.
  - Ngoại lệ: Thùng hàng tiêu chuẩn hoặc thùng xe bán tải/xe tải thì tính là một phần cấu trúc xe.
- **R-05 — Loại trừ vật thể phi thực tế / mô hình / phản chiếu:**
  - Tuyệt đối **KHÔNG gán** tượng điêu khắc đá, đồng (`img_017.jpg`, `img_027.jpg`).
  - Tuyệt đối **KHÔNG gán** tranh ảnh, pano quảng cáo (`img_018.jpg`).
  - Tuyệt đối **KHÔNG gán** bóng phản chiếu trong gương chiếu hậu hoặc mặt kính (`img_020.jpg`).
  - Tuyệt đối **KHÔNG gán** ma-nơ-canh (`img_033.jpg`), xe đồ chơi / búp bê trong tủ kính (`img_038.jpg`), hoặc xe mô hình diễu hành giả tưởng (`img_019.jpg`).
- **R-06 — Phương tiện thô sơ không động cơ:**
  - Xe đạp, xe xích lô đạp chân: KHÔNG gán box cho phương tiện. CHỈ gán box `person` cho người điều khiển và hành khách.
- **R-07 — Ngưỡng vật thể nhỏ và cụm đám đông:**
  - Vật thể đơn lẻ có chiều cao $h < 20\text{ px}$: **KHÔNG gán box đơn lẻ**.
  - Khu vực có nhiều người/xe ở rất xa tạo thành đám đông đan xen dày đặc không thể phân định biên: Gán 1 box `ignore_region` bao trùm cụm đó (`img_025.jpg`, `img_040.jpg`).
- **R-08 — Nửa thân vỏ xe gắn trang trí trên nóc (`img_024.jpg`):**
  - Gán 1 box `car` cho xe chính bên dưới. KHÔNG gán phần thân vỏ cắt rời gắn trên giá nóc vì đây chỉ là phụ kiện chở theo, không phải phương tiện vận hành độc lập.

---

## 4. Bảng ca khó (Hard Cases) khảo sát từ 40 ảnh

| Ảnh | Tình huống thực tế | Rule ID | Quyết định đề xuất | Lý do kỹ thuật |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở 8 ô tô con trên 2 tầng sàn. | `R-03` | 1 box `truck` cho xe tải; gán thêm 8 box `car` cho 8 ô tô con trên sàn. | Mô hình cần phát hiện được cả phương tiện vận chuyển và các ô tô đang được chở. |
| `img_004.jpg` | Hai xe tuk-tuk 3 bánh sơn xanh đỗ bên đường. | `R-01` | Gán lớp `tuk_tuk` (nếu có) hoặc thống nhất quy tắc phân loại tại Pha 2. | Không thể ép tuk-tuk vào `car` hay `motorcycle` vì hình học và động học khác biệt. |
| `img_005.jpg` | Đám đông xe máy và người lái trên đường phố TP.HCM. | `R-02` | Tách riêng box `person` và box `motorcycle` cho từng người/xe. Gán `occluded_level=2` hoặc `3` cho các xe phía sau. | Đảm bảo tính nhất quán trong bài toán phát hiện người điều khiển phương tiện 2 bánh. |
| `img_006.jpg` | Đoàn xích lô du lịch tại Huế và xe đạp. | `R-06` | KHÔNG gán box cho xe xích lô / xe đạp. CHỈ gán `person` cho người đạp và khách ngồi. | Xích lô và xe đạp là phương tiện thô sơ, nằm ngoài taxonomy phương tiện cơ giới đường bộ. |
| `img_011.jpg` | Nhân vật cosplay Predator đứng cạnh dãy xe máy độ. | `R-05` | Gán `person` cho nhân vật cosplay nếu xác định là người thật mặc trang phục; gán từng xe máy; tick `can_review=true`. | Người cosplay chiếm không gian như người thật nhưng có hình dạng dị thường cần thảo luận nhóm. |
| `img_017.jpg` | Tượng công tước Wellington cưỡi ngựa bằng đồng. | `R-05` | KHÔNG gán `person` cho tượng người cưỡi ngựa. | Tượng bất động, không tham gia giao thông. Nếu gán sẽ gây lỗi phanh gấp vô cớ. |
| `img_018.jpg` | Biển quảng cáo bầu cử có hình chân dung người. | `R-05` | KHÔNG gán `person` cho mặt người trên biển quảng cáo. | Hình ảnh 2D trên biển bảng phẳng, không phải thực thể trong không gian 3D. |
| `img_019.jpg` | Xe diễu hành mô hình hoạt hình Dangermouse. | `R-05` | KHÔNG gán `car`. Nếu nhìn thấy người điều khiển bên trong thì gán `person`. Tick `can_review=true`. | Phương tiện diễu hành mô hình hoạt hình dị biệt, không đại diện cho phương tiện giao thông chuẩn. |
| `img_020.jpg` | Hình ảnh cầu vồng và xe phản chiếu qua gương chiếu hậu. | `R-05` | KHÔNG gán bất kỳ box nào cho ảnh phản chiếu trong gương. | Hình ảnh phản chiếu qua gương là ảnh ảo, không tồn tại ở vị trí thực tế trước đầu xe. |
| `img_024.jpg` | Xe AMC Pacer chở nửa vỏ xe hơi cắt rời trên giá nóc. | `R-08` | Gán 1 box `car` cho xe chính bên dưới. KHÔNG gán box `car` cho vỏ xe gắn trên nóc. | Vỏ xe trên nóc là hành lý/vật thể chở theo, không có động cơ hay người điều khiển. |
| `img_026.jpg` | Cặp đôi đi xe máy trong hầm Thủ Thiêm ngược sáng, bóng tối. | `R-02` | Gán 1 box `person` cho người lái, 1 box `person` cho người ngồi sau, 1 box `motorcycle` cho xe máy. | Dù bị ngược sáng và bóng đen, hình dạng đặc trưng người và xe máy vẫn phân biệt rõ. |
| `img_027.jpg` | Tượng đài xe bán tải bằng đá granite trong nghĩa trang. | `R-05` | KHÔNG gán `car` hay `truck` cho tượng đá. | Khối đá điêu khắc trong công viên nghĩa trang, không phải phương tiện giao thông. |
| `img_029.jpg` | Xe máy chở khối bao tải hàng hóa khổng lồ phía sau. | `R-04` | Box `motorcycle` chỉ ôm sát khung xe và bánh xe máy, KHÔNG bao khối hàng cồng kềnh. Gán 1 box `person` cho người lái. | Tránh làm biến dạng kích thước xe máy chuẩn trong dữ liệu huấn luyện. |
| `img_033.jpg` | Ma-nơ-canh mặc quần áo đứng trong tủ kính cửa hàng. | `R-05` | KHÔNG gán `person` cho ma-nơ-canh. | Ma-nơ-canh bằng nhựa/sáp trong tủ kính, không tham gia giao thông. |
| `img_035.jpg` | Xe auto rickshaw chở hàng chất cao ngất ngưởng. | `R-04` | Box phương tiện chỉ ôm khung cabin và bánh xe; KHÔNG bao trùm khối hàng bao tải trên nóc. | Box ôm trọn khối hàng sẽ khiến mô hình nhận diện sai lệch hoàn toàn kích thước xe ba bánh. |
| `img_037.jpg` | Xe bán tải GO Transit gắn nắp thùng cao ngang cabin (`Master 75`). | `R-01` | Phân loại tạm thời là `truck` (hoặc `van`), tick `can_review=true` để thảo luận nhóm tại Pha 2. | Bán tải có nắp thùng cao nằm ở ranh giới giữa `truck` (pickup chassis) và `van` (thân hộp kín). |
| `img_038.jpg` | Tủ kính trưng bày sưu tập đồ chơi, xe mô hình và búp bê. | `R-05` | KHÔNG gán box cho bất kỳ xe đồ chơi hay búp bê nào. | Đồ chơi thu nhỏ sau tủ kính không thuộc miền dữ liệu phát hiện phương tiện/người giao thông. |

---

## 5. QC và phiên bản

### 5.1. Ngưỡng kiểm soát chất lượng đề xuất
- **IoU đối tượng:**
  - $\ge 0.85$ cho đối tượng kích thước lớn ($h \ge 50\text{ px}$).
  - $\ge 0.70$ cho đối tượng kích thước nhỏ ($20 \le h < 50\text{ px}$).
- **Độ đồng thuận nhóm (IAA):**
  - IoU trung bình $\ge 0.85$.
  - Đồng thuận lớp $\ge 95\%$.
- **Nghiệm thu toàn lô:** Tỉ lệ ảnh có lỗi $\le 2.0\%$ (trên 40 ảnh: tối đa 0 ảnh lỗi để được `Release`).

### 5.2. Lịch sử thay đổi
| Phiên bản | Thay đổi chính | Lý do / Căn cứ |
|---|---|---|
| `v0` | Bản khởi đầu do giảng viên cung cấp. Định nghĩa sơ sài 5 lớp, thuộc tính định tính, chưa có quy tắc ca biên. | Nền tảng ban đầu của bài lab. |
| `v0.1-individual` | - Bổ sung đề xuất lớp `bus`, `tuk_tuk`.<br>- Định lượng cụ thể ngưỡng % cho `occluded_level` ($0\%$, $1\text{–}30\%$, $31\text{–}70\%$, $>70\%$).<br>- Ban hành 8 quy tắc trọng tâm (`R-01` đến `R-08`).<br>- Xây dựng bảng xử lý 17 ca khó cụ thể trích xuất từ 40 ảnh thực tế. | Khắc phục hoàn toàn các điểm mơ hồ của v0 sau khi khảo sát độc lập 40 ảnh. |
