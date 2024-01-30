from django.contrib import admin
from urllib.parse import urljoin

from django.utils.html import format_html


# Register your models here.
def create_image_response(file, width=100, height=100):
    return format_html('<img src="{url}" width="{width}" height={height} />'.format(
        url=file.url,
        width=width,
        height=height,
    ))
