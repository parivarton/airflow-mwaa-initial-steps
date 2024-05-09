from fastapi.testclient import TestClient
from basic_fast_api.app.feedback_review_analysis_api import app


client = TestClient(app)

def test_create_review():
    # Test creating a review
    response = client.post(
        "/reviews/",
        json={
            "customer_id": 1,
            "product_id": 1,
            "review": "This product is great!",
            "rating": 5
        },
    )
    #print(response)
    assert response.status_code == 200
    assert response.json() == {"message": "Review added successfully"}

def test_get_product_review_stats():
    # Test getting product review stats
    response = client.get("/product-review-stats/")
    assert response.status_code == 200
    product_review_stats = response.json()
    # Add assertions based on expected product review stats

def test_get_stats():
    # Test getting all reviews
    response = client.get("/stats/")
    assert response.status_code == 200
    reviews = response.json()
    # Add assertions based on expected reviews

# Run the tests
test_create_review()
test_get_product_review_stats()
test_get_stats()
