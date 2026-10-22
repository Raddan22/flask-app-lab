from flask import Blueprint, render_template, abort
from app.products.data import products

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def list_products():
    # ЗМІНЕНО ТУТ: прибрано "products/"
    return render_template('products.html', products=products)

@products_bp.route('/<int:id>')
def detail_product(id):
    product = next((p for p in products if p['id'] == id), None)
    if product is None:
        abort(404)
    # ЗМІНЕНО ТУТ: прибрано "products/"
    return render_template('detail_product.html', product=product)