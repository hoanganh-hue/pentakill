from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from ..services import CatalogService, CompanyService


app = FastAPI(title="Enterprise API - ThongTinDoanhNghiep Wrapper")

catalog_service = CatalogService()
company_service = CompanyService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/companies/{mst}")
def get_company_by_mst(mst: str):
    data = company_service.get_company_by_mst(mst)
    if not data:
        raise HTTPException(status_code=404, detail="Company not found or invalid MST")
    return JSONResponse(content=data)


@app.get("/companies/search")
def search_companies(
    k: str | None = Query(default=None),
    l: str | None = Query(default=None),
    i: int | None = Query(default=None),
    p: int | None = Query(default=1, ge=1),
    r: int | None = Query(default=20, ge=1, le=200),
):
    result = company_service.search_companies(k=k, l=l, i=i, r=r, p=p)
    if result is None:
        raise HTTPException(status_code=503, detail="Upstream unavailable")
    return JSONResponse(content=result)


@app.get("/catalog/cities")
def get_cities():
    result = catalog_service.get_cities()
    if result is None:
        raise HTTPException(status_code=503, detail="Upstream unavailable")
    return JSONResponse(content=result)


@app.get("/catalog/cities/{city_id}/districts")
def get_districts_by_city(city_id: int):
    result = catalog_service.get_districts_by_city(city_id)
    if result is None:
        raise HTTPException(status_code=503, detail="Upstream unavailable")
    return JSONResponse(content=result)


@app.get("/catalog/districts/{district_id}/wards")
def get_wards_by_district(district_id: int):
    result = catalog_service.get_wards_by_district(district_id)
    if result is None:
        raise HTTPException(status_code=503, detail="Upstream unavailable")
    return JSONResponse(content=result)


@app.get("/catalog/industries")
def get_industries():
    result = catalog_service.get_industries()
    if result is None:
        raise HTTPException(status_code=503, detail="Upstream unavailable")
    return JSONResponse(content=result)


