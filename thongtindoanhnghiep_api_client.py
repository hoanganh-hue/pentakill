import requests
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "https://thongtindoanhnghiep.co"

class ThongTinDoanhNghiepAPIClient:
    def __init__(self):
        self.base_url = BASE_URL

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, verify=True) # verify=True để đảm bảo HTTPS
            response.raise_for_status() # Nâng lỗi cho các mã trạng thái HTTP lỗi (4xx hoặc 5xx)
            logging.info(f"Request successful for {endpoint}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An unexpected error occurred: {req_err}")
            return None

    def get_cities(self):
        """Lấy về toàn bộ danh mục Tỉnh/Thành phố"""
        logging.info("Fetching all cities...")
        return self._make_request("/api/city")

    def get_city_detail(self, city_id: int):
        """Lấy về chi tiết một Tỉnh/Thành phố"""
        logging.info(f"Fetching detail for city ID: {city_id}...")
        return self._make_request(f"/api/city/{city_id}")

    def get_districts_by_city(self, city_id: int):
        """Lấy về toàn bộ Quận/Huyện theo Tỉnh/Thành phố"""
        logging.info(f"Fetching districts for city ID: {city_id}...")
        return self._make_request(f"/api/city/{city_id}/district")

    def get_district_detail(self, district_id: int):
        """Lấy về chi tiết một Quận/Huyện"""
        logging.info(f"Fetching detail for district ID: {district_id}...")
        return self._make_request(f"/api/district/{district_id}")

    def get_wards_by_district(self, district_id: int):
        """Lấy về toàn bộ phường, xã & thị trấn thuộc Quận/Huyện"""
        logging.info(f"Fetching wards for district ID: {district_id}...")
        return self._make_request(f"/api/district/{district_id}/ward")

    def get_ward_detail(self, ward_id: int):
        """Lấy về chi tiết phường, xã, thị trấn"""
        logging.info(f"Fetching detail for ward ID: {ward_id}...")
        return self._make_request(f"/api/ward/{ward_id}")

    def get_industries(self):
        """Lấy về toàn bộ danh mục ngành nghề kinh doanh"""
        logging.info("Fetching all industries...")
        return self._make_request("/api/industry")

    def search_companies(self, k=None, l=None, i=None, r=None, p=None):
        """Lọc danh sách doanh nghiệp theo các tiêu chí khác nhau"""
        logging.info(f"Searching companies with params: k={k}, l={l}, i={i}, r={r}, p={p}...")
        params = {}
        if k: params["k"] = k
        if l: params["l"] = l
        if i: params["i"] = i
        if r: params["r"] = r
        if p: params["p"] = p
        return self._make_request("/api/company", params=params)

    def get_company_detail_by_mst(self, mst: str):
        """Lấy về chi tiết doanh nghiệp theo mã số thuế"""
        logging.info(f"Fetching detail for company MST: {mst}...")
        return self._make_request(f"/api/company/{mst}")

if __name__ == "__main__":
    client = ThongTinDoanhNghiepAPIClient()

    first_city_id = None
    first_district_id = None
    first_ward_id = None
    first_company_mst = None

    # Ví dụ sử dụng và test các endpoint
    print("\n--- Testing get_cities ---")
    cities_response = client.get_cities()
    if cities_response:
        cities = cities_response.get("LtsItems", [])
        if cities:
            print(f"Found {len(cities)} cities. First city: {cities[0]['Title']}")
            first_city_id = cities[0]["ID"]
        else:
            print("No cities found in the LtsItems key.")
    else:
        print("Failed to get cities response.")

    if first_city_id:
        print(f"\n--- Testing get_city_detail for ID {first_city_id} ---")
        city_detail = client.get_city_detail(first_city_id)
        if city_detail: print(f"Detail for city {first_city_id}: {city_detail['Title']}")
        else: print(f"Failed to get detail for city {first_city_id}.")

        print(f"\n--- Testing get_districts_by_city for ID {first_city_id} ---")
        districts_response = client.get_districts_by_city(first_city_id)
        if districts_response:
            districts = districts_response.get("LtsItems", [])
            if districts:
                print(f"Found {len(districts)} districts in city {first_city_id}. First district: {districts[0]['Title']}")
                first_district_id = districts[0]["ID"]
            else:
                print("No districts found in the LtsItems key.")
        else:
            print(f"Failed to get districts for city {first_city_id}.")

    if first_district_id:
        print(f"\n--- Testing get_district_detail for ID {first_district_id} ---")
        district_detail = client.get_district_detail(first_district_id)
        if district_detail: print(f"Detail for district {first_district_id}: {district_detail['Title']}")
        else: print(f"Failed to get detail for district {first_district_id}.")

        print(f"\n--- Testing get_wards_by_district for ID {first_district_id} ---")
        wards_response = client.get_wards_by_district(first_district_id)
        if wards_response:
            wards = wards_response.get("LtsItems", [])
            if wards:
                print(f"Found {len(wards)} wards in district {first_district_id}. First ward: {wards[0]['Title']}")
                first_ward_id = wards[0]["ID"]
            else:
                print("No wards found in the LtsItems key.")
        else:
            print(f"Failed to get wards for district {first_district_id}.")

    if first_ward_id:
        print(f"\n--- Testing get_ward_detail for ID {first_ward_id} ---")
        ward_detail = client.get_ward_detail(first_ward_id)
        if ward_detail: print(f"Detail for ward {first_ward_id}: {ward_detail['Title']}")
        else: print(f"Failed to get detail for ward {first_ward_id}.")

    print("\n--- Testing get_industries ---")
    industries_response = client.get_industries()
    if industries_response:
        industries = industries_response.get("LtsItems", [])
        if industries:
            print(f"Found {len(industries)} industries. First industry: {industries[0]['Title']}")
        else:
            print("No industries found in the LtsItems key.")
    else:
        print("Failed to get industries response.")

    print("\n--- Testing search_companies (k=Cong Ty Co phan Cong Nghe, l=ha-noi, p=1) ---")
    companies_search = client.search_companies(k="Cong Ty Co phan Cong Nghe", l="ha-noi", p=1)
    if companies_search:
        company_data = companies_search.get("data", [])
        if company_data:
            print(f"Found {len(company_data)} companies. First company: {company_data[0]['Title']}")
            first_company_mst = company_data[0]["MaSoThue"]
        else:
            print("No companies found in the data key.")
    else:
        print("Failed to search companies.")

    if first_company_mst:
        print(f"\n--- Testing get_company_detail_by_mst for MST {first_company_mst} ---")
        company_detail_mst = client.get_company_detail_by_mst(first_company_mst)
        if company_detail_mst: print(f"Detail for company {first_company_mst}: {company_detail_mst['Title']}")
        else: print(f"Failed to get detail for company {first_company_mst}.")

    print("\n--- Testing search_companies (error case - non-existent company name) ---")
    companies_search_error = client.search_companies(k="Cong Ty Khong Ton Tai XYZ") # Tên công ty không tồn tại
    if companies_search_error:
        if not companies_search_error.get("data"):
            print("Error handling for non-existent company name worked as expected (no data returned).")
        else:
            print(f"Error handling for non-existent company name failed. Response: {companies_search_error}")
    else:
        print("Error handling for non-existent company name worked as expected (no response).")

    print("\n--- Testing get_company_detail_by_mst (error case - non-existent MST) ---")
    company_detail_non_existent = client.get_company_detail_by_mst("0000000000") # MST không tồn tại
    if company_detail_non_existent is None:
        print("Error handling for non-existent MST worked as expected.")
    else:
        if company_detail_non_existent.get("Title") is None:
            print("Error handling for non-existent MST worked as expected (empty object returned).")
        else:
            print(f"Error handling for non-existent MST failed. Response: {company_detail_non_existent}")
