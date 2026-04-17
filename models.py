from sqlalchemy import DateTime, LargeBinary
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, validates
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients_master"

    client_id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    client_type: Mapped[Optional[str]] = mapped_column(String(15), default="new")
    client_status: Mapped[Optional[str]] = mapped_column(String(15), default="active")
    client_name: Mapped[str] = mapped_column(String(150), nullable=False)
    client_email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    client_phone: Mapped[Optional[str]] = mapped_column(String(20))
    company_name: Mapped[Optional[str]] = mapped_column(String(100))
    company_address: Mapped[Optional[str]] = mapped_column(String(150))
    company_website: Mapped[Optional[str]] = mapped_column(String(100))
    company_logo: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # One-to-Many relationship with Orders
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="client", cascade="all, delete-orphan")
    # One-to-Many relationship with Ecom Products
    ecom_products: Mapped[List["EcomProductData"]] = relationship("EcomProductData", back_populates="client", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "order_data"

    order_id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    client_id: Mapped[str] = mapped_column(String(32), ForeignKey("clients_master.client_id", ondelete="CASCADE"))
    client_name: Mapped[str] = mapped_column(String(100))
    ordered_posts: Mapped[int] = mapped_column(Integer, nullable=False)
    package: Mapped[str] = mapped_column(String(100), nullable=False)
    package_code: Mapped[Optional[str]] = mapped_column(String(50))
    is_monthly: Mapped[bool] = mapped_column(Boolean, default=False)
    unit_post_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_order_price: Mapped[float] = mapped_column(Float, nullable=False)
    brand_guidelines: Mapped[Optional[str]] = mapped_column(String(1000))
    product_or_service_name: Mapped[Optional[str]] = mapped_column(String(100))
    product_or_service_features: Mapped[Optional[str]] = mapped_column(String(100))
    business_objectives: Mapped[Optional[str]] = mapped_column(String(1000))
    business_offers: Mapped[Optional[str]] = mapped_column(String(1000))
    client_requirements: Mapped[Optional[str]] = mapped_column(String(1000))
    target_country: Mapped[Optional[str]] = mapped_column(String(100))
    target_audience: Mapped[Optional[str]] = mapped_column(String(100))
    target_religious_groups: Mapped[Optional[str]] = mapped_column(String(200))

    status: Mapped[str] = mapped_column(String(15), default="active")
    
    # Payment Info
    pay_medium: Mapped[Optional[str]] = mapped_column(String(15))
    bkash_number: Mapped[Optional[str]] = mapped_column(String(20))
    bkash_trx_id: Mapped[Optional[str]] = mapped_column(String(100))
    nogod_number: Mapped[Optional[str]] = mapped_column(String(20))
    nogod_trx_id: Mapped[Optional[str]] = mapped_column(String(100))
    bank_acc_name: Mapped[Optional[str]] = mapped_column(String(150))
    bank_acc_number: Mapped[Optional[str]] = mapped_column(String(50))
    bank_trx_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    order_date: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    # One-to-Many relationship with Content
    contents: Mapped[List["Content"]] = relationship("Content", back_populates="order", cascade="all, delete-orphan")


class Content(Base):
    __tablename__ = "content_engine_data"

    content_id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    order_id: Mapped[str] = mapped_column(String(32), ForeignKey("order_data.order_id", ondelete="CASCADE"))
    text_prompt: Mapped[Optional[str]] = mapped_column(String(5000))
    post_text_raw: Mapped[Optional[str]] = mapped_column(String(5000))
    post_text_formatted: Mapped[Optional[str]] = mapped_column(String(5000))
    text_status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    image_prompt: Mapped[Optional[str]] = mapped_column(String(5000))
    image_status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    drive_image_url: Mapped[Optional[str]] = mapped_column(String(200))
    raw_image_path: Mapped[Optional[str]] = mapped_column(String(200))
    batch_job_id: Mapped[Optional[str]] = mapped_column(String(100))
    batch_job_rqst_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    batch_job_comp_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    batch_job_status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    upscale_required: Mapped[bool] = mapped_column(Boolean, default=False)
    upscale_status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    f4k_image_path: Mapped[Optional[str]] = mapped_column(String(200)) 
    post_to_socials: Mapped[bool] = mapped_column(Boolean, default=False)
    save_to_drive: Mapped[bool] = mapped_column(Boolean, default=True)
    gdrive_status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    status: Mapped[Optional[str]] = mapped_column(String(15), default="active")

    # Relationship with Order
    order: Mapped["Order"] = relationship("Order", back_populates="contents")


class EcomContentStyle(Base):
    __tablename__ = "ecom_content_styles"

    style_id: Mapped[str] = mapped_column(String(8), primary_key=True, index=True, default=lambda: uuid.uuid4().hex[:8])
    style_name: Mapped[str] = mapped_column(String(150), nullable=False)
    style_alias: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)



    def __init__(self, **kwargs):
        if "style_id" not in kwargs:
            kwargs["style_id"] = uuid.uuid4().hex[:8]
        if "style_alias" not in kwargs:
            kwargs["style_alias"] = f"style_{kwargs['style_id']}"
        super().__init__(**kwargs)


class EcomProductData(Base):
    __tablename__ = "ecom_product_data"

    product_id: Mapped[str] = mapped_column(String(8), primary_key=True, index=True, default=lambda: uuid.uuid4().hex[:8])
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    sku: Mapped[Optional[str]] = mapped_column(String(100))
    color: Mapped[Optional[str]] = mapped_column(String(50))
    client_id: Mapped[str] = mapped_column(String(32), ForeignKey("clients_master.client_id", ondelete="CASCADE"))
    product_category: Mapped[Optional[str]] = mapped_column(String(100))
    product_subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    product_url: Mapped[Optional[str]] = mapped_column(String(500))
    platform: Mapped[Optional[str]] = mapped_column(String(50))
    caption: Mapped[Optional[str]] = mapped_column(String(5000))
    image: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    styles: Mapped[Optional[str]] = mapped_column(String(1000))
    images_done: Mapped[Optional[str]] = mapped_column(String(15), default="0/0")
    status: Mapped[Optional[str]] = mapped_column(String(15), default="pending")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Relationship with Client
    client: Mapped["Client"] = relationship("Client", back_populates="ecom_products")

    # --- Calculated properties ---

    @property
    def product_alias(self) -> str:
        return f"image_{self.product_id}"

    @property
    def img_file_name(self) -> str:
        parts = [p for p in [self.product_category, self.product_subcategory] if p]
        s_alias = (self.styles or "").replace(',', '_')
        segments = ["image"] + parts + [s_alias, self.product_id]
        return "_".join(filter(None, segments)) + ".png"

    @property
    def img_file_path(self) -> str:
        company = (self.client.company_name if self.client else "").replace(" ", "")
        path_parts = [p for p in [self.product_category, self.product_subcategory] if p]
        return "/".join(["assets", "e_commerce_samples", company, "inputs"] + path_parts + [self.img_file_name])

    @property
    def logo_path(self) -> str:
        """Path to the client logo PNG, stored at the root of the client's assets folder."""
        company = (self.client.company_name if self.client else "").replace(" ", "")
        return f"assets/e_commerce_samples/{company}/logo.png"

    # --- Image auto-resize validator ---

    @validates("image")
    def _resize_image(self, _key, value):
        """Auto-resize incoming image data to 100x100 pixels."""
        if value is None:
            return value
        from PIL import Image
        from io import BytesIO
        img = Image.open(BytesIO(value))
        img = img.convert("RGBA") if img.mode in ("RGBA", "P", "LA") else img.convert("RGB")
        img = img.resize((100, 100), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()



