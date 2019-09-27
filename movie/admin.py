from django.contrib import admin
from movie.models import BasedOnId, BasedOnTitle

# Register your models here.
admin.site.register(BasedOnId)
admin.site.register(BasedOnTitle)
