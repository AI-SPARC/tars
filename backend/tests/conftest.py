import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from main import app  # Import the FastAPI application
from core.deps import get_session  # API dependency for database session
from core.base import Base  # Database models

# Define the test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Create an asynchronous session factory for tests
TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    """
    Initializes and tears down the test database.

    This fixture creates all tables before running any tests and drops them afterward.
    It ensures a fresh database state for the test session.

    Yields:
        None: Allows the test session to proceed.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session(init_test_db):
    """
    Provides a clean asynchronous database session for each test.

    This fixture ensures that all tables are cleared before each test, avoiding conflicts such as
    unique constraint violations. Each test gets an isolated session.

    Args:
        init_test_db: Ensures the test database is initialized before session creation.

    Yields:
        AsyncSession: A fresh database session for the test.
    """
    async with TestSessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

        yield session

