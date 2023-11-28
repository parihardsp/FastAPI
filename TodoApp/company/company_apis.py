from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"Conmapny Name": "Ex Company Pvt. Ltd."}

@router.get("/employees")
async def number_of_employees():
    return {"Total Employees": 201}
