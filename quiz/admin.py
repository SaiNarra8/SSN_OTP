from django.contrib import admin

# Register your models here.
from .models import Question,Result,Course,Passage,Email,LongPassage

admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Course)
admin.site.register(Email)
admin.site.register(Passage)
admin.site.register(LongPassage)


