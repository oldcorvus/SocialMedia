from django.contrib import admin
from .models import Article, Category
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
    

def article_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='P')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))

article_published.short_description = "انتشار مقالات"

def article_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status='D')
        if rows_updated == 1:
            message_bit = "پیش‌نویس شد."
        else:
            message_bit = "پیش‌نویس شدند."
        modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))

article_draft.short_description = "پیشنویس مقالات"




class ArticleAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['title','thumbnail_tag', 'author', 'get_created_jalali_create','get_created_jalali_publish','get_created_jalali_update','status','category_str']
    list_filter = ['status','publish']
    raw_id_fields = ('author',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status','-publish']
    actions =[article_published, article_draft]

    def get_created_jalali_publish(self, obj):
     return datetime2jalali(obj.publish).strftime('%y/%m/%d تاريخ _ %H:%M:%S ساعت')

    def get_created_jalali_create(self, obj):
     return datetime2jalali(obj.created).strftime('%y/%m/%d تاريخ _ %H:%M:%S ساعت')

    def get_created_jalali_update(self, obj):
     return datetime2jalali(obj.updated).strftime('%y/%m/%d تاريخ _ %H:%M:%S ساعت')

    get_created_jalali_publish.short_description = 'تاریخ انتشار'
    get_created_jalali_create.short_description = 'تاریخ ساخت'
    get_created_jalali_update.short_description = 'تاریخ ويرايش'
    get_created_jalali_publish.admin_order_field = 'publish'

    def category_str(self , obj):
        return ", ".join([category.title for category in obj.category.all()])
    category_str.short_description = 'دسته بندي ها '

admin.site.register(Article, ArticleAdmin)


def category_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status= True)
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))

category_published.short_description = "انتشار دسته بندی "

def category_draft(modeladmin, request, queryset):
        rows_updated = queryset.update(status= False)
        if rows_updated == 1:
            message_bit = "پیش‌نویس شد."
        else:
            message_bit = "پیش‌نویس شدند."
        modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))

category_draft.short_description = "پیشنویس دسته بندی"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover','parent','slug','status']
    search_fields = ['title','description']
    list_filter = ['status']
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    actions =[category_published, category_draft]

admin.site.register(Category, CategoryAdmin)
