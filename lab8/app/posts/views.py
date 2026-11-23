from flask import render_template, redirect, url_for, flash, request
from app.posts import post_bp
from app.posts.models import Post, User, Tag
from app.posts.forms import PostForm
from app import db
from sqlalchemy import select, func

@post_bp.route('/post')
def all_posts():
    stmt = select(Post).where(Post.is_active == True).order_by(Post.publish_date.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('posts.html', posts=posts)

@post_bp.route('/post/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)

@post_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    # Заповнюємо списки авторів та тегів
    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    
    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            publish_date=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data
        )
        
        # Додаємо теги (Many-to-Many)
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags = selected_tags
        
        db.session.add(new_post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.all_posts'))
    
    return render_template('add_post.html', form=form)

@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    
    # Заповнюємо списки
    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if request.method == 'GET':
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.publish_date = form.publish_date.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        
        # Оновлюємо теги
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = selected_tags
        
        db.session.commit()
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))
    
    return render_template('add_post.html', form=form, is_edit=True)

@post_bp.route('/post/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост видалено!', 'info')
        return redirect(url_for('posts.all_posts'))
    return render_template('delete_confirm.html', post=post)