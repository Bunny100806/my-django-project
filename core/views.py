from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Post, Profile
from .forms import PostForm, ProfileForm
from core.tasks import send_post_notification  # Celery task

# ========== Homepage ==========
def home(request):
    return HttpResponse("<h1>Welcome to My Django API!</h1><p>Go to <code>/api/posts/</code> to use the API.</p>")

# ========== Feed ==========
@login_required
def feed(request):
    posts = Post.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})

# ========== Authentication ==========
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# ========== Profile Views ==========
@login_required
def profile_detail(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})

def profile_redirect(request):
    return redirect('profile')  # Named URL must be 'profile'

# ========== Post Views ==========
def post_list(request):
    posts = Post.objects.select_related('author').all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        send_post_notification.delay(post.id)
        return redirect('post_list')
    return render(request, 'core/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        return redirect('post_list')

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save()
        send_post_notification.delay(post.id)
        return redirect('post_list')
    return render(request, 'core/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'core/post_confirm_delete.html', {'post': post})

# ========== REST API ==========
from rest_framework import viewsets, permissions
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        send_post_notification.delay(post.id)

    def perform_update(self, serializer):
        post = serializer.save()
        send_post_notification.delay(post.id)
