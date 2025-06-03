from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from school_site.core.db import Base
from school_site.core.models import TimestampMixin, FileMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('price IS NULL OR price >= 0', name='positive_price_check'),
    )

    photo = relationship("Photo", back_populates="product", uselist=False, cascade="all, delete-orphan")


class Photo(Base, TimestampMixin, FileMixin):
    __tablename__ = "photo_products"

    product_id = Column(PostgresUUID(as_uuid=True), ForeignKey("products.id"), unique=True)

    product = relationship("Product", back_populates="photo")