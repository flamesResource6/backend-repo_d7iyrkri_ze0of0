import os
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import Watch

app = FastAPI(title="Monaco Watch Company API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WatchOut(BaseModel):
    id: str
    name: str
    brand: str
    description: Optional[str] = None
    price: float
    currency: str
    images: List[str] = []
    thumbnail: Optional[str] = None
    movement: Optional[str] = None
    case: Optional[str] = None
    strap: Optional[str] = None
    water_resistance: Optional[str] = None
    power_reserve: Optional[str] = None
    complications: List[str] = []
    featured: bool = False
    in_stock: bool = True
    rating: Optional[float] = None


def _doc_to_watch_out(doc) -> WatchOut:
    return WatchOut(
        id=str(doc.get("_id")),
        name=doc.get("name"),
        brand=doc.get("brand"),
        description=doc.get("description"),
        price=float(doc.get("price", 0)),
        currency=doc.get("currency", "USD"),
        images=[str(u) for u in doc.get("images", [])],
        thumbnail=str(doc.get("thumbnail")) if doc.get("thumbnail") else None,
        movement=doc.get("movement"),
        case=doc.get("case"),
        strap=doc.get("strap"),
        water_resistance=doc.get("water_resistance"),
        power_reserve=doc.get("power_reserve"),
        complications=doc.get("complications", []),
        featured=bool(doc.get("featured", False)),
        in_stock=bool(doc.get("in_stock", True)),
        rating=doc.get("rating"),
    )


@app.get("/")
def read_root():
    return {"message": "Monaco Watch Company Backend Running"}


@app.get("/api/watches", response_model=List[WatchOut])
def list_watches(
    featured: Optional[bool] = Query(default=None, description="Filter by featured flag"),
    limit: int = Query(default=12, ge=1, le=50)
):
    """List watches, optionally filtering to featured only"""
    # Seed demo data if empty
    if db is not None and db["watch"].count_documents({}) == 0:
        _seed_demo_watches()

    filter_query = {}
    if featured is not None:
        filter_query["featured"] = featured
    docs = get_documents("watch", filter_query, limit)
    return [_doc_to_watch_out(d) for d in docs]


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


@app.post("/api/seed")
def seed():
    """Manually seed demo watches (idempotent)"""
    _seed_demo_watches(force=True)
    return {"status": "ok"}


def _seed_demo_watches(force: bool = False):
    """Insert a small curated set of demo watches if collection empty or force=True"""
    if db is None:
        return
    col = db["watch"]
    if not force and col.count_documents({}) > 0:
        return

    demo: List[Watch] = [
        Watch(
            name="Monaco Heritage Chronograph",
            brand="Monaco Watch Co.",
            description="A square-case chronograph inspired by the spirit of the Riviera.",
            price=9200,
            currency="USD",
            thumbnail="https://images.unsplash.com/photo-1526045612212-70caf35c14df?q=80&w=1600&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1526045612212-70caf35c14df?q=80&w=1600&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1511385348-a52b4a160dc2?q=80&w=1600&auto=format&fit=crop"
            ],
            movement="Automatic",
            case="Stainless steel 39mm",
            strap="Alligator leather",
            water_resistance="100m",
            power_reserve="42h",
            complications=["Chronograph", "Date"],
            featured=True,
            in_stock=True,
            rating=4.8
        ),
        Watch(
            name="Azur Moonphase",
            brand="Monaco Watch Co.",
            description="Elegant moonphase with a deep azure dial and applied indices.",
            price=11800,
            currency="USD",
            thumbnail="https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=1600&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=1600&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1518546305927-5a555bb7020a?q=80&w=1600&auto=format&fit=crop"
            ],
            movement="Automatic",
            case="18k rose gold 41mm",
            strap="Blue calfskin",
            water_resistance="50m",
            power_reserve="70h",
            complications=["Moonphase", "Date"],
            featured=True,
            in_stock=True,
            rating=4.9
        ),
        Watch(
            name="Port Royale Diver",
            brand="Monaco Watch Co.",
            description="Professional diver with ceramic bezel and luminous markers.",
            price=7800,
            currency="USD",
            thumbnail="https://images.unsplash.com/photo-1516478177764-9fe5bd7e9717?q=80&w=1600&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1516478177764-9fe5bd7e9717?q=80&w=1600&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1490367532201-b9bc1dc483f6?q=80&w=1600&auto=format&fit=crop"
            ],
            movement="Automatic",
            case="Titanium 42mm",
            strap="Rubber",
            water_resistance="300m",
            power_reserve="60h",
            complications=["Helium valve", "Date"],
            featured=False,
            in_stock=True,
            rating=4.7
        ),
    ]

    # Upsert-like behavior by name
    for w in demo:
        existing = col.find_one({"name": w.name})
        if existing and not force:
            continue
        if existing and force:
            col.delete_one({"_id": existing["_id"]})
        create_document("watch", w)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
