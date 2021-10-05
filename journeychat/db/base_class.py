"""
Taken from template: https://github.com/tiangolo/full-stack-fastapi-postgresql

This base class extends sqlalchemy base model,
allowing for autonaming of tabels.
"""

import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
