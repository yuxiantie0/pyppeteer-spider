from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from functools import wraps
from models.user import User
from extensions import db
from datetime import datetime

bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('需要管理员权限', 'danger')
            return redirect(url_for('website.website_list'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            user.last_login = datetime.utcnow()
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('website.website_list'))
        
        flash('用户名或密码错误', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@bp.route('/users')
@admin_required
def user_list():
    users = User.query.all()
    return render_template('auth/user_list.html', users=users)

@bp.route('/user/add', methods=['GET', 'POST'])
@admin_required
def user_add():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return render_template('auth/user_form.html')
        
        user = User(username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('用户创建成功', 'success')
        return redirect(url_for('auth.user_list'))
    
    return render_template('auth/user_form.html')

@bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def user_edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        
        if username != user.username and User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return render_template('auth/user_form.html', user=user)
        
        user.username = username
        if password:
            user.set_password(password)
        user.is_admin = is_admin
        db.session.commit()
        flash('用户更新成功', 'success')
        return redirect(url_for('auth.user_list'))
    
    return render_template('auth/user_form.html', user=user)

@bp.route('/user/delete/<int:id>')
@admin_required
def user_delete(id):
    user = User.query.get_or_404(id)
    if user.username == 'admin':
        flash('无法删除管理员账户', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('用户删除成功', 'success')
    return redirect(url_for('auth.user_list')) 