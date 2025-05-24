from celery import shared_task
from .models import Post

@shared_task
def send_post_notification(post_id):
    post = Post.objects.get(pk=post_id)
    # simulate sending an email
    print(f"Email sent for post: {post.title}")