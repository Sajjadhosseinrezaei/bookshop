from django.db import models
from utils.models import TimeStampedModel


class Product(TimeStampedModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="اسلاگ"
    )

    name = models.CharField(
        max_length=255,
        verbose_name="نام کتاب"
    )

    price = models.PositiveIntegerField(
        verbose_name="قیمت (تومان)"
    )

    discount_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت با تخفیف (تومان)"
    )


    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="موجودی انبار"
    )

    author = models.CharField(
        max_length=255,
        verbose_name="نویسنده"
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته‌بندی"
    )

    main_topic = models.CharField(
        max_length=150,
        verbose_name="موضوع اصلی"
    )

    secondary_topic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="موضوع فرعی"
    )

    translator = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="مترجم"
    )


    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="ناشر"
    )


    description = models.TextField(
        verbose_name="توضیحات"
    )

    language = models.CharField(
        max_length=50,
        verbose_name="زبان"
    )

    more = models.JSONField(
        blank=True,
        default=dict,
        verbose_name="اطلاعات تکمیلی"
    )

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ["-created"]

    def __str__(self):
        return self.name




class Category(TimeStampedModel):

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام دسته‌بندی"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دسته‌بندی والد"
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        db_index=True,
        verbose_name="اسلاگ"
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name
    


class Publisher(TimeStampedModel):

    image = models.ImageField(
        upload_to="publishers/",
        blank=True,
        null=True,
        verbose_name="لوگوی ناشر"
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="نام ناشر"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    slug = models.SlugField(
    max_length=220,
    unique=True,
    db_index=True,
    verbose_name="اسلاگ"
    )

    class Meta:
        verbose_name = "ناشر"
        verbose_name_plural = "ناشران"
        ordering = ["name"]

    def __str__(self):
        return self.name