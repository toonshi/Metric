
# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Institution, UserReview
from .forms import UserReviewForm

def institution_detail(request, institution_id):
    # Get the selected institution
    institution = get_object_or_404(Institution, pk=institution_id)

    # Handle form submission
    if request.method == 'POST':
        form = UserReviewForm(request.POST)
        if form.is_valid():
            # Save the review and associate it with the selected institution
            review = form.save(commit=False)
            review.institution = institution
            review.user = request.user  # Assuming you have user authentication
            review.save()
            return redirect('success_page')  # Redirect to a success page after submitting the review
    else:
        form = UserReviewForm()

    return render(request, 'institution_detail.html', {'institution': institution, 'form': form})
