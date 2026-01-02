from django.db import models
from django.conf import settings
from utils.models import TimeStampedModel
from products.models import Product
from django.core.validators import MinValueValidator

class Cart(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="کاربر"
    )
    total_price = models.PositiveIntegerField(
        default=0,
        verbose_name="مبلغ کل (تومان)"
    )

    discount_price = models.PositiveIntegerField(
        default=0,
        verbose_name="مبلغ نهایی پس از تخفیف (تومان)"
    )

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"
        ordering = ["-created"]

    def __str__(self):
        return f"سبد خرید #{self.id} - {self.user}"
    


class CartItem(TimeStampedModel):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
        verbose_name="محصول"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد"
    )

    price = models.PositiveIntegerField(
        verbose_name="قیمت واحد (تومان)"
    )

    discount_price = models.PositiveIntegerField(
        verbose_name="قیمت واحد با تخفیف (تومان)"
    )

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product} × {self.quantity}"
    


class DiscountCode(TimeStampedModel):

    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name="کد تخفیف"
    )

    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="مبلغ تخفیف (تومان)"
    )

    usage_limit_per_user = models.PositiveIntegerField(
        default=1,
        verbose_name="حداکثر تعداد استفاده برای هر کاربر"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    start = models.DateTimeField(
        verbose_name="زمان شروع"
    )

    end = models.DateTimeField(
        verbose_name="زمان پایان"
    )

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
        ordering = ["-created"]

    def __str__(self):
        return self.code


class DiscountUser(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="used_discounts",
        verbose_name="کاربر"
    )

    discount_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
        related_name="usages",
        verbose_name="کد تخفیف"
    )

    used_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان استفاده"
    )

    class Meta:
        verbose_name = "استفاده از کد تخفیف"
        verbose_name_plural = "استفاده‌های کد تخفیف"
        unique_together = ("user", "discount_code")


class Order(TimeStampedModel):

    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("processing", "در حال پردازش"),
        ("shipped", "ارسال شده"),
        ("completed", "تکمیل شده"),
        ("canceled", "لغو شده"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="کاربر"
    )

    transport = models.ForeignKey(
        "Transport",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="روش ارسال"
        , blank=True
    )

    total_price = models.PositiveIntegerField(
        verbose_name="مبلغ کل (تومان)"
    )

    discount_price = models.PositiveIntegerField(
        default=0,
        verbose_name="مبلغ تخفیف (تومان)"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت سفارش"
    )

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created"]

    def __str__(self):
        return f"سفارش #{self.id}"
    


class OrderItem(TimeStampedModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="محصول"
    )

    product_title = models.CharField(
        max_length=255,
        editable=False,
        verbose_name="عنوان محصول"
    )

    product_sku = models.CharField(
        max_length=100,
        editable=False,
        verbose_name="شناسه کالا"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد"
    )

    price = models.PositiveIntegerField(
        verbose_name="قیمت واحد (تومان)"
    )

    discount_price = models.PositiveIntegerField(
        default=0,
        verbose_name="تخفیف واحد (تومان)"
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.product_title} × {self.quantity}"



class Transport(TimeStampedModel):

    name_company = models.CharField(
        max_length=150,
        verbose_name="نام شرکت حمل‌ونقل"
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="کد رهگیری"
    )

    send_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ ارسال"
    )

    class Meta:
        verbose_name = "روش ارسال"
        verbose_name_plural = "روش‌های ارسال"

    def __str__(self):
        return self.name_company
