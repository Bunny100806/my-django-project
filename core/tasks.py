from celery import shared_task

@shared_task
def send_post_notification(post_id):
    # Your notification sending logic here
    print(f"Notification sent for post {post_id}")
from celery import shared_task

@shared_task
def send_post_notification(post_id):
    print(f"Notification sent for post {post_id}")
