from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from blog.models import BlogComment


def _recount_comments(post):
    from .models import BlogComment

    n = BlogComment.objects.filter(
        post=post, status=BlogComment.Status.APPROVED
    ).count()
    if post.comentarios_count != n:
        post.comentarios_count = n
        post.save(update_fields=["comentarios_count", "actualizado"])


@receiver(post_save, sender=BlogComment)
def _comment_saved(sender, instance, **kwargs):
    _recount_comments(instance.post)


@receiver(post_delete, sender=BlogComment)
def _comment_deleted(sender, instance, **kwargs):
    _recount_comments(instance.post)
