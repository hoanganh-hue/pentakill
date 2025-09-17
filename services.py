from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Optional

from cachetools import TTLCache

from .config import settings
from .thongtindoanhnghiep_api_client import ThongTinDoanhNghiepAPIClient


def normalize_mst(raw_mst: str) -> Optional[str]:
    if raw_mst is None:
        return None
    digits = re.sub(r"\D", "", str(raw_mst))
    if len(digits) in (10, 13):
        return digits
    return None


class RetryClientWrapper:
    def __init__(self, client: ThongTinDoanhNghiepAPIClient):
        self.client = client

    def _retry(self, func, *args, **kwargs):
        delay = settings.RETRY_INITIAL_DELAY_SECONDS
        for attempt in range(1, settings.RETRY_MAX_ATTEMPTS + 1):
            resp = func(*args, **kwargs)
            if resp is not None:
                return resp
            if attempt == settings.RETRY_MAX_ATTEMPTS:
                break
            time.sleep(delay)
            delay *= settings.RETRY_BACKOFF_FACTOR
        return None

    # Catalog
    def get_cities(self):
        return self._retry(self.client.get_cities)

    def get_city_detail(self, city_id: int):
        return self._retry(self.client.get_city_detail, city_id)

    def get_districts_by_city(self, city_id: int):
        return self._retry(self.client.get_districts_by_city, city_id)

    def get_district_detail(self, district_id: int):
        return self._retry(self.client.get_district_detail, district_id)

    def get_wards_by_district(self, district_id: int):
        return self._retry(self.client.get_wards_by_district, district_id)

    def get_ward_detail(self, ward_id: int):
        return self._retry(self.client.get_ward_detail, ward_id)

    def get_industries(self):
        return self._retry(self.client.get_industries)

    # Companies
    def search_companies(self, k=None, l=None, i=None, r=None, p=None):
        return self._retry(self.client.search_companies, k, l, i, r, p)

    def get_company_detail_by_mst(self, mst: str):
        return self._retry(self.client.get_company_detail_by_mst, mst)


def map_company_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not raw:
        return {}
    return {
        "MaSoThue": raw.get("MaSoThue"),
        "Title": raw.get("Title"),
        "TitleEn": raw.get("TitleEn"),
        "DiaChiCongTy": raw.get("DiaChiCongTy"),
        "TinhThanhTitle": raw.get("TinhThanhTitle"),
        "QuanHuyenTitle": raw.get("QuanHuyenTitle"),
        "NgayCap": raw.get("NgayCap"),
        "ExitsInGDT": raw.get("ExitsInGDT"),
        "NoiDangKyQuanLy_CoQuanTitle": raw.get("NoiDangKyQuanLy_CoQuanTitle"),
        "ChuSoHuu": raw.get("ChuSoHuu"),
        "GiamDoc": raw.get("GiamDoc"),
        "NganhNgheTitle": raw.get("NganhNgheTitle"),
    }


class CatalogService:
    def __init__(self, client: Optional[ThongTinDoanhNghiepAPIClient] = None):
        base_client = client or ThongTinDoanhNghiepAPIClient()
        self.client = RetryClientWrapper(base_client)
        self.cache_cities = TTLCache(maxsize=1024, ttl=settings.CATALOG_TTL_SECONDS)
        self.cache_districts_by_city = TTLCache(maxsize=4096, ttl=settings.CATALOG_TTL_SECONDS)
        self.cache_wards_by_district = TTLCache(maxsize=8192, ttl=settings.CATALOG_TTL_SECONDS)
        self.cache_industries = TTLCache(maxsize=1024, ttl=settings.CATALOG_TTL_SECONDS)

    def get_cities(self):
        key = "cities"
        if key in self.cache_cities:
            return self.cache_cities[key]
        data = self.client.get_cities()
        if data is not None:
            self.cache_cities[key] = data
        return data

    def get_districts_by_city(self, city_id: int):
        if city_id in self.cache_districts_by_city:
            return self.cache_districts_by_city[city_id]
        data = self.client.get_districts_by_city(city_id)
        if data is not None:
            self.cache_districts_by_city[city_id] = data
        return data

    def get_wards_by_district(self, district_id: int):
        if district_id in self.cache_wards_by_district:
            return self.cache_wards_by_district[district_id]
        data = self.client.get_wards_by_district(district_id)
        if data is not None:
            self.cache_wards_by_district[district_id] = data
        return data

    def get_industries(self):
        key = "industries"
        if key in self.cache_industries:
            return self.cache_industries[key]
        data = self.client.get_industries()
        if data is not None:
            self.cache_industries[key] = data
        return data


class CompanyService:
    def __init__(self, client: Optional[ThongTinDoanhNghiepAPIClient] = None):
        base_client = client or ThongTinDoanhNghiepAPIClient()
        self.client = RetryClientWrapper(base_client)
        self.cache_company_by_mst = TTLCache(maxsize=4096, ttl=settings.COMPANY_TTL_SECONDS)

    def get_company_by_mst(self, raw_mst: str) -> Optional[Dict[str, Any]]:
        mst = normalize_mst(raw_mst)
        if not mst:
            return None
        key = mst
        if key in self.cache_company_by_mst:
            return self.cache_company_by_mst[key]
        raw = self.client.get_company_detail_by_mst(mst)
        if not raw:
            return None
        mapped = map_company_payload(raw)
        # basic verification
        if mapped.get("MaSoThue") and mapped["MaSoThue"][:10] != mst[:10]:
            return None
        self.cache_company_by_mst[key] = mapped
        return mapped

    def search_companies(self, k=None, l=None, i=None, r=None, p=None):
        return self.client.search_companies(k=k, l=l, i=i, r=r, p=p)


