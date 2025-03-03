from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from extensions import db
from models import Website, Cookie
from config.settings import COOKIE_DAILY_LIMIT
import json

bp = Blueprint('cookie', __name__)

# Cookie管理列表页面
@bp.route('/cookies')
def cookie_list():
    cookies = Cookie.query.all()
    return render_template('cookie/list.html', cookies=cookies)

# 添加Cookie
@bp.route('/cookie/add', methods=['GET', 'POST'])
def cookie_add():
    if request.method == 'POST':
        cookie = Cookie(
            website_id=request.form['website_id'],
            account=request.form['account'],
            cookie_value=request.form['cookie_value'],
            note=request.form.get('note', '')
        )
        db.session.add(cookie)
        db.session.commit()
        return redirect(url_for('cookie.cookie_list'))
    websites = Website.query.all()
    return render_template('cookie/form.html', websites=websites)

# 编辑Cookie
@bp.route('/cookie/edit/<int:id>', methods=['GET', 'POST'])
def cookie_edit(id):
    cookie = Cookie.query.get_or_404(id)
    if request.method == 'POST':
        cookie.website_id = request.form['website_id']
        cookie.account = request.form['account']
        cookie.cookie_value = request.form['cookie_value']
        cookie.note = request.form.get('note', '')
        db.session.commit()
        return redirect(url_for('cookie.cookie_list'))
    websites = Website.query.all()
    return render_template('cookie/form.html', cookie=cookie, websites=websites)

# 删除Cookie
@bp.route('/cookie/delete/<int:id>')
def cookie_delete(id):
    cookie = Cookie.query.get_or_404(id)
    db.session.delete(cookie)
    db.session.commit()
    return redirect(url_for('cookie.cookie_list'))

# 切换Cookie状态
@bp.route('/cookie/toggle/<int:id>')
def cookie_toggle(id):
    cookie = Cookie.query.get_or_404(id)
    cookie.is_valid = not cookie.is_valid
    db.session.commit()
    return jsonify({'status': 'success', 'is_valid': cookie.is_valid})

# API: 获取Cookie
@bp.route('/api/getcookie')
def get_cookie():
    site = request.args.get('site')
    account = request.args.get('account')
    num = request.args.get('num', type=int, default=1)
    
    if not site:
        return jsonify({'status': 'error', 'message': 'Site parameter is required'})
    
    # 获取有效且未超过使用限制的Cookie
    query = Cookie.query.join(Website).filter(
        Website.identifier == site,
        Cookie.is_valid == True,
        Cookie.daily_used < COOKIE_DAILY_LIMIT
    )
    
    if account:
        query = query.filter(Cookie.account == account)
    
    # 按使用次数升序排序，优先使用使用次数少的Cookie
    cookies = query.order_by(Cookie.daily_used.asc()).limit(num).all()
    
    if not cookies:
        return jsonify({'status': 'error', 'message': 'No valid cookies found or usage limit exceeded'})
    
    result = []
    for cookie in cookies:
        cookie.total_used += 1
        cookie.daily_used += 1
        cookie_data = json.loads(cookie.cookie_value)
        result.append(cookie_data)  # 使用append，保持每个cookie的数组结构
        
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': result
    })

# API: 使Cookie失效
@bp.route('/api/expirecookie', methods=['POST'])
def expire_cookie():
    cookie_value = request.form.get('cookie')
    if not cookie_value:
        return jsonify({'status': 'error', 'message': 'Cookie value is required'})

    cookie_data = json.loads(cookie_value)
    pin_id = ""
    for item in cookie_data:
        if item['name'] == 'pinId':
            pin_id = item['value']
            break

    cookie = Cookie.query.filter(Cookie.cookie_value.like('%'+pin_id+'%')).first()
    # cookie = Cookie.query.filter_by(cookie_value=cookie_value).first()
    if not cookie:
        return jsonify({'status': 'error', 'message': 'Cookie not found'})
    
    cookie.is_valid = False
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Cookie expired successfully'}) 