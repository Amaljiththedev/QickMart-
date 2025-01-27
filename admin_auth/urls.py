from django.contrib import admin
from django.urls import path, include
from .views import *
from category import views as category_views
from products import views as products_views
from inventory import views as stock_management

urlpatterns = [
    path("", admin_login, name="admin_login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("generate-pdf-report/", report_pdf_order, name="generate_pdf_report"),
    path("usermanagement/", User_management, name="user_management"),
    path("status/<int:user_id>/block/", block, name="block_status"),
    path("status/<int:user_id>/unblock/", unblock, name="unblock_status"),
    path("userviewdetails/<int:user_id>/", userviewdetails, name="userviewdetails"),
    path("category/", category_views.category_list, name="category"),
    path("add_category/", category_views.add_category, name="add_category"),
    path("edit_category/<int:id>/", category_views.edit_category, name="edit_category"),
    path(
        "delete_category/<int:id>/",
        category_views.delete_category,
        name="delete_category",
    ),
    path(
        "block_category/<int:id>/", category_views.block_category, name="block_category"
    ),
    path(
        "unblock_category/<int:id>/",
        category_views.unblock_category,
        name="unblock_category",
    ),
    path("product_management/", products_views.product_view, name="product_management"),
    path("add_product/", products_views.add_product, name="add_product"),
    path("edit_product/<int:id>/", products_views.update_product, name="edit"),
    path("add_brand/", category_views.add_brand, name="add_brand"),
    path("block_product/<int:id>/", products_views.block_product, name="block_product"),
    path(
        "unblock_product/<int:id>/",
        products_views.unblock_product,
        name="unblock_product",
    ),
    path(
        "delete_product/<int:id>/", products_views.delete_product, name="delete_product"
    ),
    path(
        "add-variant/<int:product_id>/", products_views.add_variant, name="add_variant"
    ),
    path("logout/", admin_logout, name="logout"),
    path("delete_user/<int:id>/", delete_user, name="delete_user"),
    path(
        "banner_management/", category_views.banner_management, name="banner_management"
    ),
    path("add_banner/", category_views.add_banner, name="add_banner"),
    path("update_banner/<int:id>", category_views.update_banner, name="update_banner"),
    path("delete_banner/<int:id>", category_views.delete_banner, name="delete_banner"),
    path("block_banner/<int:id>", category_views.block_banner, name="block_banner "),
    path(
        "unblock_banner/<int:id>", category_views.unblock_banner, name="unblock_banner"
    ),
    path("stock/", stock_management.stock_management, name="stock_management"),
    path("update-stock/", stock_management.update_stock, name="update_stock"),
    path(
        "ordermanagement/", stock_management.order_management, name="order_management"
    ),
    path(
        "update_status/<int:order_id>/",
        stock_management.update_status,
        name="update_status",
    ),
    path("variant_management/", products_views.variant_management, name="variant"),
    path(
        "show_variants/<int:product_id>",
        products_views.show_variants,
        name="show_variants",
    ),
    path(
        "variant/<int:variant_id>/block/",
        products_views.block_variant,
        name="block_variant",
    ),
    path(
        "variant/<int:variant_id>/delete/",
        products_views.delete_variant,
        name="delete_variant",
    ),
    path(
        "block-variant/<int:variant_id>/",
        products_views.block_variant,
        name="block_variant",
    ),
    path(
        "unblock-variant/<int:variant_id>/",
        products_views.unblock_variant,
        name="unblock_variant",
    ),
    path(
        "update-order/<int:order_id>/",
        stock_management.update_order_details,
        name="update_order_details",
    ),
    path(
        "refund-order/<int:order_id>/",
        stock_management.refund_order,
        name="refund_order",
    ),
    path("coupon/", stock_management.coupon_list, name="coupon_management"),
    path("add-coupon", stock_management.add_coupon, name="add_coupon"),
    path(
        "edit-coupon/<int:coupon_id>/", stock_management.edit_coupon, name="edit_coupon"
    ),
    path(
        "delete-coupon/<int:coupon_id>/",
        stock_management.delete_coupon,
        name="delete_coupon",
    ),
]
