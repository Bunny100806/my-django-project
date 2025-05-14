from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile
from .forms import PostForm, ProfileForm

# ========== Homepage ==========
def home(request):
    return render(request, 'core/home.html')

# ========== Authentication ==========
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # ensure profile is created
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# ========== Profile Views ==========
@login_required
def profile_detail(request):
    # Ensure profile exists (safety net if signal failed)
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile_detail.html', {'profile': request.user.profile})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})

@login_required
def profile_redirect(request):
    return redirect('profile')

# ========== Post Views ==========
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'core/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'core/post_form.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'core/post_confirm_delete.html', {'post': post})
