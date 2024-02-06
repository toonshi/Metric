from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserReviewForm
from .models import Institution
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
# views.py
# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserReviewForm
from .models import Institution

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
