from flask import render_template, redirect, url_for, flash, session, request
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm
from app import db

@post_bp.route('/post')
def all_posts():
    posts = db.session.execute(db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())).scalars().all()
    return render_template('posts.html', posts=posts)

@post_bp.route('/post/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)

@post_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get('username', 'Anonymous')
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,  # <-- ЗМІНЕНО ТУТ
            author=author
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.all_posts'))
    return render_template('add_post.html', form=form)

@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data  # <-- ЗМІНЕНО ТУТ
        if form.publish_date.data:
            post.posted = form.publish_date.data
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