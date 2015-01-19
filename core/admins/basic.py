from django.contrib import admin


class BasicAdmin(admin.ModelAdmin):
    save_on_top = True