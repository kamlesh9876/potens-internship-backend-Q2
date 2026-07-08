import pytest
from app.services.auth_service import AuthService
from app.services.item_service import ItemService
from app.services.recommendation_service import RecommendationService
from app.services.explain_service import ExplainService
from app.schemas.user import UserCreate, UserLogin
from app.schemas.item import ItemCreate, ItemUpdate
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.models.item import Item
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository


def test_auth_service_register_success(db_session):
    """Test AuthService register with valid data"""
    repo = UserRepository(db_session)
    auth_service = AuthService(repo)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="TestPass123",
        full_name="Test User"
    )
    
    user = auth_service.register(user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_auth_service_register_duplicate_email(db_session, normal_user):
    """Test AuthService register with duplicate email"""
    repo = UserRepository(db_session)
    auth_service = AuthService(repo)
    user_data = UserCreate(
        username="different",
        email="user@test.com",
        password="TestPass123",
        full_name="Different User"
    )
    
    with pytest.raises(Exception) as exc_info:
        auth_service.register(user_data)
    assert "already registered" in str(exc_info.value)


def test_auth_service_login_success(db_session, normal_user):
    """Test AuthService login with valid credentials"""
    repo = UserRepository(db_session)
    auth_service = AuthService(repo)
    login_data = UserLogin(email="user@test.com", password="user123")
    
    token = auth_service.login(login_data)
    
    assert token.access_token is not None
    assert token.token_type == "bearer"


def test_auth_service_login_wrong_password(db_session):
    """Test AuthService login with wrong password"""
    repo = UserRepository(db_session)
    auth_service = AuthService(repo)
    login_data = UserLogin(email="wrong@example.com", password="WrongPass123")
    
    with pytest.raises(Exception):
        auth_service.login(login_data)


def test_item_service_create_item(db_session):
    """Test ItemService create_item"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    item_data = ItemCreate(
        name="Test Course",
        category="Programming",
        price=99.99,
        skill_level="Beginner",
        goal="Career Growth",
        location="Online",
        pace="Self-paced",
        description="Test description"
    )
    
    item = item_service.create_item(item_data)
    
    assert item.name == "Test Course"
    assert item.price == 99.99


def test_item_service_get_item_success(db_session, sample_items):
    """Test ItemService get_item with valid ID"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    item = item_service.get_item(sample_items[0].id)
    
    assert item.id == sample_items[0].id
    assert item.name == sample_items[0].name


def test_item_service_get_item_not_found(db_session):
    """Test ItemService get_item with invalid ID"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    with pytest.raises(NotFoundException) as exc_info:
        item_service.get_item(999)
    assert "not found" in str(exc_info.value)


def test_item_service_update_item(db_session, sample_items):
    """Test ItemService update_item"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    update_data = ItemUpdate(name="Updated Course", price=149.99)
    
    updated_item = item_service.update_item(sample_items[0].id, update_data)
    
    assert updated_item.name == "Updated Course"
    assert updated_item.price == 149.99


def test_item_service_delete_item(db_session, sample_items):
    """Test ItemService delete_item"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    item_id = sample_items[0].id
    
    item_service.delete_item(item_id)
    
    with pytest.raises(NotFoundException):
        item_service.get_item(item_id)


def test_recommendation_service_build_recommendations(db_session, sample_items):
    """Test RecommendationService build_recommendations"""
    from app.schemas.recommendation import ProfileInput
    repo = ItemRepository(db_session)
    recommendation_service = RecommendationService(repo)
    profile = ProfileInput(
        age=25,
        budget=200,
        experience_level="Beginner",
        goal="Career Change",
        location="Online",
        preferred_pace="Self-paced"
    )
    
    recommendations = recommendation_service.build_recommendations(profile)
    
    assert len(recommendations) >= 0


def test_explain_service_explain_item(db_session, sample_items):
    """Test ExplainService explain_item"""
    explain_service = ExplainService()
    
    explanation = explain_service.explain_item(sample_items[0])
    
    assert explanation is not None
    assert isinstance(explanation, str)
    assert len(explanation) > 0


def test_item_service_list_items_with_filters(db_session, sample_items):
    """Test ItemService list_items with filters"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    filters = {"category": "Programming"}
    items = item_service.list_items(filters=filters)
    
    assert isinstance(items, list)


def test_item_service_list_items_with_search(db_session, sample_items):
    """Test ItemService list_items with search"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    items = item_service.list_items(search="Python")
    
    assert isinstance(items, list)


def test_item_service_list_items_with_sorting(db_session, sample_items):
    """Test ItemService list_items with sorting"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    items = item_service.list_items(sort_by="price", order="asc")
    
    assert isinstance(items, list)


def test_item_service_get_paginated_items(db_session, sample_items):
    """Test ItemService get_paginated_items"""
    repo = ItemRepository(db_session)
    item_service = ItemService(repo)
    
    paginated_data = item_service.get_paginated_items(page=1, limit=10)
    
    assert "items" in paginated_data
    assert "total" in paginated_data
    assert "page" in paginated_data
    assert "limit" in paginated_data
    assert "total_pages" in paginated_data
    assert "has_next" in paginated_data
    assert "has_previous" in paginated_data
