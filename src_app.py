from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from collections import defaultdict
from datetime import datetime

app = FastAPI()

class Review(BaseModel):
    customer_id: int
    product_id: int
    review: str
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 to 5")
    review_time: datetime

class ProductReviewStats(BaseModel):
    product_id: int
    good_reviews: int
    bad_reviews: int
    neutral_reviews: int


def analyze_review(review: str) -> str:
    # Perform text analysis to determine if the review is good or bad
    # This is just a placeholder implementation
    if "good" in review.lower():
        return "good"
    elif "bad" in review.lower():
        return "bad"
    else:
        return "neutral"

class ReviewManager:
    def __init__(self):
        self.reviews = []

    def add_review(self, review: Review):
        self.reviews.append(review)

    def get_product_review_stats(self) -> List[ProductReviewStats]:
        stats = defaultdict(lambda: defaultdict(int))


        for review in self.reviews:
            sentiment = analyze_review(review.review)
            stats[review.product_id][sentiment + "_reviews"] += 1

        product_review_stats = []
        for product_id, sentiment_counts in stats.items():
            stats = ProductReviewStats(
                product_id=product_id,
                good_reviews=sentiment_counts["good_reviews"],
                bad_reviews=sentiment_counts["bad_reviews"],
                neutral_reviews=sentiment_counts["neutral_reviews"]
            )
            product_review_stats.append(stats)

        return product_review_stats

review_manager = ReviewManager()

@app.post("/reviews/")
async def create_review(customer_id: int, product_id: int, review: str, rating: int):
    review_time = datetime.now().timestamp()
    review_obj = Review(customer_id = customer_id,
                        product_id=product_id,
                        review=review,
                        rating=rating,
                        review_time=review_time)
    review_manager.add_review(review_obj)
    return {"message": "Review added successfully"}

@app.get("/product-review-stats/")
async def get_product_review_stats():
    return review_manager.get_product_review_stats()

@app.get("/stats/")
async def get_stats():
    return review_manager.reviews
