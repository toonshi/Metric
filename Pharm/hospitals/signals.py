#signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserReview, Institution

@receiver(post_save, sender=UserReview)
def update_review_summary(sender, instance, created, **kwargs):
    if created or instance.review != instance._original_review:
        institution = instance.institution
        reviews = institution.reviews.all()
        reviews_text = [review.review for review in reviews]
        institution.review_summary = summarize_reviews(reviews_text)  # Update review summary
        institution.save()


def summarize_reviews(reviews):
    # Implement your summarization logic here
    summary = " ".join(reviews)  # Just concatenating all reviews for now
    return summary
