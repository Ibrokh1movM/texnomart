from django.contrib import admin
from texnomart.models import Category, Product, Image, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'total_price')
    list_filter = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Mahsulotlar soni"

    def total_price(self, obj):
        return sum(product.price for product in obj.products.all())
    total_price.short_description = "Umumiy narx"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_count', 'short_description')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('price',)
    ordering = ('name',)
    list_per_page = 20

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Rasmlar soni"

    def short_description(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    short_description.short_description = "Qisqa tavsif"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_primary')
    list_filter = ('is_primary', 'product')
    search_fields = ('product__name',)
    list_editable = ('is_primary',)

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "Rasm yo‘q"
    image_preview.short_description = "Rasm"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'short_message', 'rating', 'created_at', 'has_image')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('message', 'user__username', 'product__name', 'good_comment', 'bad_comment')
    list_editable = ('rating',)
    ordering = ('-created_at',)
    list_per_page = 20
    date_hierarchy = 'created_at'

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = "Qisqa xabar"

    def has_image(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "Rasm yo‘q"
    has_image.short_description = "Rasm mavjud"

    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'rating')
        }),
        ('Comment Details', {
            'fields': ('message', 'good_comment', 'bad_comment', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

admin.site.site_header = "Texnomart Admin Paneli"
admin.site.site_title = "Texnomart"
admin.site.index_title = "Xush kelibsiz, Texnomart boshqaruv paneliga!"