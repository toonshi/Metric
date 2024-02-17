# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .forms import UserReviewForm
# from .models import Institution
'''
def institution_detail(request, institution_id):
    institution = Institution.objects.get(pk=institution_id)
    if request.method == 'POST':
        form = UserReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.institution = institution
            review.save()
            return JsonResponse({'success': True})  # Return a success JSON response
        else:
            return JsonResponse({'errors': form.errors}, status=400)  # Return form errors if validation fails
    else:
        form = UserReviewForm()
    return render(request, 'institution_detail.html', {'institution': institution, 'form': form})
'''
# # views.py
# # views.py
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .forms import UserReviewForm
# from .models import Institution

# def institution_detail(request, institution_id):
#     institution = Institution.objects.get(pk=institution_id)
#     if request.method == 'POST':
#         form = UserReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.institution = institution
#             review.save()
#             return JsonResponse({'success': True})  # Return a success JSON response
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)  # Return form errors if validation fails
#     else:
#         form = UserReviewForm()
#     return render(request, 'institution_detail.html', {'institution': institution, 'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserReviewForm
from .models import Institution, Insurance, UserReview, Service

def review_submit(request, institution_id):
    if request.method == 'POST':
        form = UserReviewForm(request.POST)
        if form.is_valid():
            # Associate the review with the correct institution
            institution = Institution.objects.get(pk=institution_id)
            review = form.save(commit=False)
            review.institution = institution
            review.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = UserReviewForm()
    return render(request, 'reason.html', {'form': form})


def institution_detail(request, institution_id):
    # Retrieve the institution
    institution = get_object_or_404(Institution, pk=institution_id)
    
    # Retrieve associated data (insurances, reviews, services)
    insurances = Insurance.objects.filter(institution=institution)
    reviews = UserReview.objects.filter(institution=institution)
    services = Service.objects.filter(institution=institution)
    
    # Handle review submission
    if request.method == 'POST':
        form = UserReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.institution = institution
            review.save()
            return redirect('success_page')  # Redirect to a success page after review submission
    else:
        form = UserReviewForm()
        
    # Render the template with all data and form
    context = {
        'institution': institution,
        'insurances': insurances,
        'reviews': reviews,
        'services': services,
        'form': form,
        'latitude': institution.latitude,  # Pass latitude value
        'longitude': institution.longitude,  # Pass longitude value

    }
    return render(request, 'reason.html', context)

def institution_list(request):
    institutions = Institution.objects.all()
    return render(request, 'reason.html', {'institutions': institutions})
