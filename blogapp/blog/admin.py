from django.contrib import admin
from . models import Blog, Category, Comment
from django.utils.safestring import mark_safe

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title","is_active","is_home","slug", "selected_categories",)
    list_editable = ("is_active","is_home",)
    search_fields = ("title","description","slug",)
    readonly_fields = ("slug",)
    list_filter = ("is_active","is_home", "categories")
    
    def selected_categories(self, obj):
        html = "<ul>" 
        
        for category in obj.categories.all():
            html += "<li>" + category.name + "</li>"    
        html += "</ul>" 
        return mark_safe(html)
        
admin.site.register(Blog, BlogAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug",)  
    readonly_fields = ("slug",)
    
admin.site.register(Category, CategoryAdmin,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'blog', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
 
# admin.site.register(Comment,)   
    