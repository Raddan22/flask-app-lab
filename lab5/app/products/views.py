from flask import Blueprint, render_template, abort
from app.products.data import products

products_bp = Blueprint('products', __name__, template_folder='templates/products', url_prefix='/products')

@products_bp.route('/')
def list_products():
    return render_template('products/products.html', products=products)

@products_bp.route('/<int:id>')
def detail_product(id):
    product = next((p for p in products if p['id'] == id), None)
    if product is None:
        abort(404)
    return render_template('products/detail_product.html', product=product)