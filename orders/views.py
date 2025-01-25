import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from shop.recommender import Recommender
import pdfkit
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

wkhtml_to_pdf = os.path.join(
    settings.BASE_DIR, "wkhtmltopdf.exe")

def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            #add products to the recommendation engine
            r = Recommender()
            r.products_bought(cart.get_products())
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})

    
@staff_member_required
def admin_order_pdf(request, order_id):
    options = {
    'page-size': 'A4',
    'page-height': "13in",
    'page-width': "10in",
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'encoding': "UTF-8",
    'no-outline': None,
    "enable-local-file-access": ""
    }
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    return response
