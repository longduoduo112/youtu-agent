from sqlmodel import SQLModel, select

from ..utils import SQLModelUtils, get_logger

logger = get_logger(__name__)


class DBService:
    @staticmethod
    def add(data: SQLModel | list[SQLModel]) -> None:
        """Add record(s) to db."""
        if isinstance(data, SQLModel):
            data = [data]
        elif isinstance(data, list):
            assert isinstance(data[0], SQLModel), "data must be a SQLModel or list of SQLModel"
        else:
            raise ValueError("data must be a SQLModel or list of SQLModel")
        with SQLModelUtils.create_session() as session:
            session.add_all(data)
            session.commit()

    @staticmethod
    def query(model_class: type[SQLModel], filters: dict = None) -> list[SQLModel]:
        """Query records with optional filters."""
        with SQLModelUtils.create_session() as session:
            stmt = select(model_class)
            if filters:
                for key, value in filters.items():
                    stmt = stmt.where(getattr(model_class, key) == value)
            return session.exec(stmt).all()

    @staticmethod
    def get_by_id(model_class: type[SQLModel], id: int) -> SQLModel | None:
        """Get a single record by ID."""
        with SQLModelUtils.create_session() as session:
            return session.get(model_class, id)

    @staticmethod
    def update(data: SQLModel) -> None:
        """Update a record."""
        with SQLModelUtils.create_session() as session:
            session.add(data)
            session.commit()
            session.refresh(data)

    @staticmethod
    def delete(data: SQLModel) -> None:
        """Delete a record."""
        with SQLModelUtils.create_session() as session:
            session.delete(data)
            session.commit()
