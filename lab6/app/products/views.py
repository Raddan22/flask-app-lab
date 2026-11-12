import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.products.forms import ProductForm
from app.products.models import get_all_products, get_product_by_id, add_product, update_product, delete_product

products_bp = Blueprint('products', __name__, template_folder='templates/products', url_prefix='/products')

# Зберігаємо в глобальну папку app/static/uploads/
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_image(file):
    if file and file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return f"uploads/{filename}"
    return None

@products_bp.route('/')
def list_products():
    products = get_all_products()
    return render_template('products.html', products=products)

@products_bp.route('/<int:id>')
def detail_product(id):
    product = get_product_by_id(id)
    if not product:
        abort(404)
    return render_template('detail_product.html', product=product)

@products_bp.route('/add', methods=['GET', 'POST'])
def add_product_view():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_image(form.image.data)
        data = {
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path
        }
        add_product(data)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('add_product.html', form=form)

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_product_view(id):
    product = get_product_by_id(id)
    if not product:
        abort(404)
        
    form = ProductForm(data=product)
    
    # Очищаємо поле файлу при GET-запиті, щоб уникнути помилки 'str' object has no attribute 'filename'
    if request.method == 'GET':
        form.image.data = None
    
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
        }
        
        # Якщо завантажили нове зображення - зберігаємо, інакше залишаємо старе
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            image_path = save_image(form.image.data)
            if image_path:
                data['image'] = image_path
                
        update_product(id, data)
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.detail_product', id=id))
        
    return render_template('edit_product.html', form=form, product=product)

@products_bp.route('/<int:id>/delete', methods=['POST'])
def delete_product_view(id):
    product = get_product_by_id(id)
    if not product:
        abort(404)
    delete_product(id)
    flash('Товар видалено!', 'info')
    return redirect(url_for('products.list_products'))