from fastapi import APIRouter
from src.config import categories, complexity, regions
from src.catalogs.schema import catalogs

router = APIRouter(
    prefix="/catalogs",
    tags=["catalogs"]
)

@router.get("/{catalogName}")
def getCatalog(catalogName: catalogs) -> list:
    match(catalogName):
        case("category"):
            return categories
        case("complexity"):
            return complexity
        case("country"):
            return regions
