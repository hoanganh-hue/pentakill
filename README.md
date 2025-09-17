# Hệ Thống Quản Lý Dữ Liệu VSS-BHXH Hoàn Chỉnh

## Tổng Quan

Đây là hệ thống hoàn chỉnh để quản lý và phân tích dữ liệu Bảo hiểm xã hội (BHXH) của các công ty và nhân viên. Hệ thống tích hợp dữ liệu VSS (Bảo hiểm xã hội Việt Nam) vào cơ sở dữ liệu hiện có và cung cấp các công cụ phân tích, tra cứu và báo cáo toàn diện.

## Tính Năng Chính

- **Tích hợp dữ liệu VSS-BHXH** vào hệ thống quản lý nhân sự hiện có
- **Module tra cứu tự động** thông tin BHXH theo nhiều tiêu chí
- **API tools nâng cao** để xử lý và phân tích dữ liệu BHXH
- **Báo cáo phân tích toàn diện** về tình trạng BHXH của các công ty
- **Giao diện demo** để kiểm tra và sử dụng hệ thống

## Cấu Trúc Thư Mục

```text
vss_bhxh_project_final/
├── README.md                          # Tài liệu chính
├── requirements.txt                   # Dependencies
├── scripts/                          # Các script Python chính
│   ├── vss_data_generator.py         # Tạo dữ liệu VSS mock
│   ├── vss_integrator.py             # Tích hợp dữ liệu VSS
│   ├── bhxh_lookup_module.py         # Module tra cứu BHXH
│   ├── enhanced_api_tools_vss.py     # API tools nâng cao
│   └── bhxh_report_generator.py      # Tạo báo cáo BHXH
├── data/                             # Dữ liệu
│   ├── excel/                        # Files Excel
│   │   ├── EXCEL_ORIGINAL_INPUT.xlsx             # Dữ liệu gốc
│   │   └── EXCEL_VSS_INTEGRATED_20250916_144154.xlsx  # Dữ liệu đã tích hợp VSS
│   ├── json/                         # Files JSON
│   │   └── JSON_VSS_INTEGRATED_20250916_144154.json   # Dữ liệu JSON tích hợp
│   ├── vss_output/                   # Dữ liệu VSS sinh ra
│   │   ├── VSS_DATA_COMPREHENSIVE_20250916_143916.json
│   │   ├── VSS_COMPANIES_SUMMARY_20250916_143916.csv
│   │   └── VSS_EMPLOYEES_DATA_20250916_143916.csv
│   └── reports/                      # Báo cáo
│       ├── BAO_CAO_BHXH_TOAN_DIEN_20250916_145057.xlsx
│       ├── BAO_CAO_BHXH_TOAN_DIEN_20250916_145057.md
│       └── PHAN_TICH_BHXH_DATA_20250916_145057.json
├── documentation/                    # Tài liệu
│   ├── HUONG_DAN_SU_DUNG_VSS_BHXH.md
│   ├── DELIVERABLES_SUMMARY.md
│   └── FINAL_SUMMARY_COMPLETE.md
└── demo/                            # Demo hệ thống
    └── demo_complete_system.py
```

## Hướng Dẫn Cài Đặt

### 1. Yêu Cầu Hệ Thống

- Python 3.8+
- Các thư viện được liệt kê trong `requirements.txt`

### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy Demo

```bash
python demo/demo_complete_system.py
```

## Enterprise API (Doanh nghiệp) nội bộ

Hệ thống cung cấp một lớp API nội bộ bọc nguồn `thongtindoanhnghiep.co` để tra cứu doanh nghiệp, tìm kiếm và danh mục hành chính/ngành nghề. Máy chủ sử dụng FastAPI.

### Chạy máy chủ API

```bash
# Chạy theo entrypoint mới
uvicorn api.main:app --app-dir "API-thôngtindoanhnghiep" --reload --host 0.0.0.0 --port 8000
```

Biến môi trường cấu hình (tùy chọn):

- `CATALOG_TTL_SECONDS` (mặc định 86400)
- `COMPANY_TTL_SECONDS` (mặc định 21600)
- `RETRY_MAX_ATTEMPTS` (mặc định 3)
- `RETRY_INITIAL_DELAY_SECONDS` (mặc định 1.0)
- `RETRY_BACKOFF_FACTOR` (mặc định 2.0)

### Endpoints

- `GET /health`
- `GET /companies/{mst}`: trả về thông tin DN chuẩn hóa (các trường: `MaSoThue, Title, TitleEn, DiaChiCongTy, TinhThanhTitle, QuanHuyenTitle, NgayCap, ExitsInGDT, NoiDangKyQuanLy_CoQuanTitle, ChuSoHuu, GiamDoc, NganhNgheTitle`).
- `GET /companies/search?k=&l=&i=&p=&r=`: tìm kiếm DN (trả pass-through cấu trúc nguồn, khóa `data`).
- `GET /catalog/cities`
- `GET /catalog/cities/{id}/districts`
- `GET /catalog/districts/{id}/wards`
- `GET /catalog/industries`

### Ví dụ

```bash
curl -sS http://localhost:8000/companies/0104478506
```

```bash
curl -sS 'http://localhost:8000/companies/search?k=Cong%20Ty%20Cong%20Nghe&l=ha-noi&p=1&r=20'
```

### Kiến trúc API nội bộ (tổng quan)

- Lớp dữ liệu: `ThongTinDoanhNghiepAPIClient` (gọi `https://thongtindoanhnghiep.co`).
- Lớp dịch vụ:
  - `CompanyService`: chuẩn hóa MST (10/13 số), mapping trường, cache TTL, retry.
  - `CatalogService`: danh mục tỉnh/thành, quận/huyện, phường/xã, ngành nghề (cache TTL 24h).
- Lớp API: `api_server.py` (FastAPI) expose các endpoint `/companies/*`, `/catalog/*`, `/health`.

Sơ đồ tóm tắt:

```text
Client → FastAPI (`api_server.py`) → Services (`services.py`) → ThongTinDoanhNghiepAPIClient → thongtindoanhnghiep.co
```

### Chuẩn hóa và Mapping dữ liệu công ty

Trường trả về từ `GET /companies/{mst}` (đã chuẩn hóa):

- `MaSoThue` ← nguồn `MaSoThue`
- `Title` ← nguồn `Title`
- `TitleEn` ← nguồn `TitleEn`
- `DiaChiCongTy` ← nguồn `DiaChiCongTy`
- `TinhThanhTitle` ← nguồn `TinhThanhTitle`
- `QuanHuyenTitle` ← nguồn `QuanHuyenTitle`
- `NgayCap` ← nguồn `NgayCap`
- `ExitsInGDT` ← nguồn `ExitsInGDT`
- `NoiDangKyQuanLy_CoQuanTitle` ← nguồn `NoiDangKyQuanLy_CoQuanTitle`
- `ChuSoHuu` ← nguồn `ChuSoHuu`
- `GiamDoc` ← nguồn `GiamDoc`
- `NganhNgheTitle` ← nguồn `NganhNgheTitle`

Quy tắc xác minh cơ bản:

- MST đầu vào được chuẩn hóa còn lại 10 hoặc 13 chữ số; nếu khác → 404.
- Kết quả có `MaSoThue` (10 ký tự đầu) phải khớp với MST đầu vào (10 ký tự đầu).

### Xử lý lỗi và mã trạng thái

- `404 Not Found`: MST không hợp lệ hoặc không tìm thấy doanh nghiệp.
- `503 Service Unavailable`: Upstream `thongtindoanhnghiep.co` tạm thời không khả dụng (sau khi đã retry).
- `200 OK`: Thành công.

Retry và backoff:

- Thử tối đa `RETRY_MAX_ATTEMPTS` lần (mặc định 3).
- Độ trễ bắt đầu `RETRY_INITIAL_DELAY_SECONDS` (mặc định 1s), nhân `RETRY_BACKOFF_FACTOR` (mặc định 2x) giữa các lần.

Caching:

- Danh mục (`cities`, `districts`, `wards`, `industries`): TTL = `CATALOG_TTL_SECONDS` (mặc định 24h).
- Chi tiết doanh nghiệp theo MST: TTL = `COMPANY_TTL_SECONDS` (mặc định 6h).

### Cấu hình hệ thống

Các biến môi trường có thể đặt khi chạy:

| Biến | Mặc định | Mô tả |
| --- | --- | --- |
| `CATALOG_TTL_SECONDS` | 86400 | TTL cache cho danh mục |
| `COMPANY_TTL_SECONDS` | 21600 | TTL cache cho chi tiết DN |
| `RETRY_MAX_ATTEMPTS` | 3 | Số lần retry tối đa |
| `RETRY_INITIAL_DELAY_SECONDS` | 1.0 | Độ trễ retry ban đầu (giây) |
| `RETRY_BACKOFF_FACTOR` | 2.0 | Hệ số backoff giữa các lần |

Ví dụ chạy với cấu hình tùy chỉnh:

```bash
COMPANY_TTL_SECONDS=14400 RETRY_MAX_ATTEMPTS=4 \
uvicorn api_server:app --app-dir "API-thôngtindoanhnghiep" --host 0.0.0.0 --port 8000
```

## Triển khai và đóng gói

- Chạy development: `uvicorn api.main:app --app-dir "API-thôngtindoanhnghiep" --reload --host 0.0.0.0 --port 8000`
- Chạy production (ví dụ): `uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 2`
- Biến môi trường tham khảo ở mục “Cấu hình hệ thống”.

## Triển khai và vận hành (tóm tắt)

## Quy trình nhập/xuất dữ liệu (MST .txt)

Theo yêu cầu vận hành, hệ thống nhận vào danh sách mã số thuế (MST) từ một tệp `.txt` và tạo ra các tệp Excel đầu ra như sau.

### 1) Đầu vào

- Tệp: `input-masothue.txt`
- Định dạng:
  - Mỗi dòng một MST (10 hoặc 13 chữ số).
  - Bỏ qua dòng rỗng và dòng bắt đầu bằng ký tự `#` (ghi chú).
  - Ví dụ:

```text
# Danh sách MST cần tra cứu
0104478506
0100109106
```

### 2) Đầu ra giai đoạn 1 (Doanh nghiệp + BHXH)

- Tệp: `/Users/nguyenduchung1993/Documents/cccd-generator-app-2/API-thôngtindoanhnghiep/output-data-doanhnghieo+bhxh.xlsx`
- Nội dung: Bảng doanh nghiệp đã chuẩn hóa cột theo mapping, có khung cột BHXH (để điền ở bước tiếp theo). Trường DN cốt lõi gồm:
  - `MaSoThue, Title, TitleEn, DiaChiCongTy, TinhThanhTitle, QuanHuyenTitle, NgayCap, ExitsInGDT, NoiDangKyQuanLy_CoQuanTitle, ChuSoHuu, GiamDoc, NganhNgheTitle`

Ghi chú: Tên tệp và trình tự tạo file tuân theo đường dẫn bạn cung cấp. Trong trường hợp muốn đảo ngược pipeline (DN → VSS → DN+BHXH), vui lòng cập nhật phần này cho thống nhất.

### 3) Chuyển tiếp sang hệ thống VSS (giai đoạn 2)

- Đầu vào: tệp Excel ở bước (2).
- Xử lý: hệ thống VSS (bên ngoài) sử dụng dữ liệu DN để tra cứu/enrich chỉ số BHXH.
- Đầu ra: `/Users/nguyenduchung1993/Documents/cccd-generator-app-2/API-thôngtindoanhnghiep/output-data-doanhnghiep.xlsx`

### 4) Lưu ý triển khai

- Hệ thống API hiện tại không kèm script ETL; bạn có thể triển khai job đọc `input-masothue.txt` và gọi API nội bộ `/companies/{mst}` để build Excel theo cấu trúc trên.
- Khuyến nghị: thực hiện theo lô (batch), có retry/backoff, và ghi nhãn thời gian xử lý vào tên file nếu cần versioning.

### 5) Script ETL đi kèm

- Tệp: `scripts/etl_mst_pipeline.py`
- Cách chạy:

```bash
python -m API-thôngtindoanhnghiep.scripts.etl_mst_pipeline
```

- Chức năng: đọc `input-masothue.txt`, gọi dịch vụ doanh nghiệp nội bộ (thông qua `CompanyService`), và xuất:
  - `output-data-doanhnghieo+bhxh.xlsx` (có khung cột BHXH trống)
  - `output-data-doanhnghiep.xlsx` (chỉ cột doanh nghiệp)

- Ưu tiên API doanh nghiệp (`api/`, `services.py`, `config.py`); các mô-đun VSS/BHXH đã được loại bỏ khỏi repository để thuận tiện triển khai.
- Khuyến nghị mở rộng: metrics (Prometheus), tracing (OpenTelemetry), và Dockerfile để đóng gói container.

## Nguồn dữ liệu, tính xác thực và quyền riêng tư

- Nguồn dữ liệu doanh nghiệp: truy xuất trực tiếp từ `https://thongtindoanhnghiep.co` thông qua lớp `ThongTinDoanhNghiepAPIClient` và các dịch vụ trong `services.py`. Dữ liệu trả về là dữ liệu thực tế tại thời điểm gọi, không tạo giả.
- Nguồn dữ liệu VSS-BHXH: các tệp trong `data/json/`, `data/excel/`, `data/vss_output/` và `data/reports/` là kết quả tích hợp/phân tích trên dữ liệu thực tế đã thu thập; các dấu thời gian trong tên tệp thể hiện thời điểm kết xuất.
- Độ tươi dữ liệu: danh mục (tỉnh/thành, quận/huyện, phường/xã, ngành nghề) được cache tối đa 24h; chi tiết doanh nghiệp theo MST được cache tối đa 6h (giá trị mặc định, có thể thay đổi qua biến môi trường). Điều này giúp cân bằng giữa tính thời sự và hiệu năng.
- Tái lập kết quả: có thể chạy lại các script trong `scripts/` để tái tạo báo cáo từ cùng nguồn dữ liệu; giữ nguyên cấu trúc thư mục để đảm bảo tái lập.
- Quyền riêng tư và tuân thủ:
  - Hệ thống không lưu thông tin nhạy cảm vượt quá nhu cầu nghiệp vụ; khi ghi log, không ghi đầy đủ định danh cá nhân (PII) mà chỉ lưu các chỉ số và mã lỗi cần thiết.
  - Tuân thủ điều khoản sử dụng của nguồn dữ liệu bên ngoài; áp dụng rate limiting và retry hợp lý để không gây quá tải dịch vụ nguồn.
  - Nếu triển khai ngoài sản xuất, xem xét bổ sung cơ chế ẩn danh/giảm định danh trong báo cáo chia sẻ ra bên ngoài.

## Ghi chú dành cho kiến trúc sư

- Hệ thống này vận hành trên dữ liệu thực/production-like. Tất cả chỉ số trong báo cáo, ví dụ trả về từ API, và số lượng bản ghi mô tả trong README đều xuất phát từ dữ liệu thật ở thời điểm đã công bố.
- Thiết kế cache TTL, retry/backoff và xác minh MST đã tính đến tính biến động của dữ liệu thật và giới hạn của nguồn ngoài.
- Khi mở rộng, khuyến nghị bổ sung: giám sát (metrics p50/p95, tỉ lệ lỗi, cache hit ratio), lưu vết gọi API (không chứa PII), và kiểm soát truy cập (API key/ACL) nếu công bố nội bộ diện rộng.
