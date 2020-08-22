from django.utils.text import slugify
import datetime

def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: 'foo-bar' => 'foo-bar-1-21'

    :param 'klass' is Class model.
    :param 'field' is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    now = datetime.datetime.now()
    if klass.objects.filter(slug=unique_slug).order_by("-id").exists():
        unique_slug = '%s-%s-%s-%s-%s-%s-%s-%s' % (origin_slug, klass.objects.filter(slug=unique_slug).order_by("-id").first().id, now.year, now.month, now.day, now.hour, now.minute, now.second)
    return unique_slug