from __future__ import annotations

import os
from typing import List, Dict, Any

import pandas as pd

from ..services import CompanyService, map_company_payload, normalize_mst


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Đường dẫn theo yêu cầu
INPUT_MST_TXT = os.path.join(PROJECT_ROOT, "input-masothue.txt")
OUTPUT_ENTERPRISE_AND_BHXH = os.path.join(
    PROJECT_ROOT,
    "output-data-doanhnghieo+bhxh.xlsx",
)
OUTPUT_ENTERPRISE_ONLY = os.path.join(
    PROJECT_ROOT,
    "output-data-doanhnghiep.xlsx",
)


ENTERPRISE_COLUMNS = [
    "MaSoThue",
    "Title",
    "TitleEn",
    "DiaChiCongTy",
    "TinhThanhTitle",
    "QuanHuyenTitle",
    "NgayCap",
    "ExitsInGDT",
    "NoiDangKyQuanLy_CoQuanTitle",
    "ChuSoHuu",
    "GiamDoc",
    "NganhNgheTitle",
]

# Các cột BHXH để trống (placeholder) ở giai đoạn 1
BHXH_PLACEHOLDER_COLUMNS = [
    "BHXH_MaSo",
    "BHXH_TrangThai",
    "BHXH_TyLeThamGia",
]


def read_mst_list(input_path: str) -> List[str]:
    msts: List[str] = []
    if not os.path.exists(input_path):
        return msts
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#"):
                continue
            normalized = normalize_mst(raw)
            if normalized:
                msts.append(normalized)
    # Loại trùng MST
    return list(dict.fromkeys(msts))


def fetch_enterprise_data(mst_list: List[str]) -> List[Dict[str, Any]]:
    service = CompanyService()
    results: List[Dict[str, Any]] = []
    for mst in mst_list:
        data = service.get_company_by_mst(mst)
        if data:
            # Đảm bảo chỉ lấy các cột doanh nghiệp cần thiết
            row = {k: data.get(k) for k in ENTERPRISE_COLUMNS}
            results.append(row)
        else:
            # Nếu không tìm thấy, vẫn ghi ra MST với các cột rỗng để dễ đối soát
            empty_row = {k: None for k in ENTERPRISE_COLUMNS}
            empty_row["MaSoThue"] = mst
            results.append(empty_row)
    return results


def write_excel_enterprise_and_bhxh(rows: List[Dict[str, Any]], output_path: str) -> None:
    # Gắn thêm cột BHXH rỗng theo yêu cầu giai đoạn 1
    enriched_rows: List[Dict[str, Any]] = []
    for row in rows:
        new_row = dict(row)
        for col in BHXH_PLACEHOLDER_COLUMNS:
            new_row[col] = None
        enriched_rows.append(new_row)

    df = pd.DataFrame(enriched_rows, columns=ENTERPRISE_COLUMNS + BHXH_PLACEHOLDER_COLUMNS)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)


def write_excel_enterprise_only(rows: List[Dict[str, Any]], output_path: str) -> None:
    df = pd.DataFrame(rows, columns=ENTERPRISE_COLUMNS)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)


def main() -> None:
    # 1) Đọc danh sách MST từ input-masothue.txt
    mst_list = read_mst_list(INPUT_MST_TXT)
    if not mst_list:
        print("No MSTs found in input-masothue.txt. Please add at least one MST.")
        return

    # 2) Gọi dịch vụ doanh nghiệp để lấy dữ liệu chuẩn hóa
    enterprise_rows = fetch_enterprise_data(mst_list)

    # 3) Ghi đầu ra giai đoạn 1: Doanh nghiệp + khung BHXH (trống)
    write_excel_enterprise_and_bhxh(enterprise_rows, OUTPUT_ENTERPRISE_AND_BHXH)
    print(f"Wrote enterprise+bhxh placeholder to: {OUTPUT_ENTERPRISE_AND_BHXH}")

    # 4) (GIAI ĐOẠN 2 - VSS bên ngoài)
    #    Sau khi hệ thống VSS xử lý và điền thông tin BHXH dựa trên file ở bước 3,
    #    kết quả cuối cùng được yêu cầu ghi ra output-data-doanhnghiep.xlsx.
    #    Ở đây, tạo sẵn phiên bản 'enterprise only' để đảm bảo công thức pipeline
    #    và giúp tích hợp thuận tiện (có thể bị thay thế bởi file sau khi VSS xử lý).
    write_excel_enterprise_only(enterprise_rows, OUTPUT_ENTERPRISE_ONLY)
    print(f"Wrote enterprise-only to: {OUTPUT_ENTERPRISE_ONLY}")


if __name__ == "__main__":
    main()


