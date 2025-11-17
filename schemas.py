"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Watch(BaseModel):
    """
    Luxury watches offered by Monaco Watch Company
    Collection name: "watch"
    """
    name: str = Field(..., description="Model name")
    brand: str = Field(..., description="Brand name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Retail price in USD")
    currency: str = Field("USD", description="Currency code")
    images: List[HttpUrl] = Field(default_factory=list, description="Gallery image URLs")
    thumbnail: Optional[HttpUrl] = Field(None, description="Primary image URL")
    movement: Optional[str] = Field(None, description="Movement type (Automatic, Manual, Quartz)")
    case: Optional[str] = Field(None, description="Case material & size")
    strap: Optional[str] = Field(None, description="Strap/Band material")
    water_resistance: Optional[str] = Field(None, description="Water resistance rating")
    power_reserve: Optional[str] = Field(None, description="Power reserve details")
    complications: List[str] = Field(default_factory=list, description="Complications like Chronograph, GMT")
    featured: bool = Field(False, description="Show on homepage features")
    in_stock: bool = Field(True, description="Inventory status")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")

class BlogPost(BaseModel):
    """
    Editorial blog posts for SEO
    Collection name: "blogpost" -> we will use alias collection name "blog" in queries
    """
    slug: str = Field(..., description="URL-friendly slug")
    title: str = Field(..., description="Post title")
    excerpt: str = Field(..., description="Short summary")
    content: str = Field(..., description="Full content (markdown allowed)")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    locale: str = Field("en", description="Language code: en, de, fr")
    hero_image: Optional[HttpUrl] = Field(None, description="Header image URL")
