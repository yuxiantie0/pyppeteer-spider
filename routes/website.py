from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Website

bp = Blueprint('website', __name__)

# 网站管理列表页面
@bp.route('/websites')
def website_list():
    websites = Website.query.all()
    return render_template('website/list.html', websites=websites)

# 添加网站
@bp.route('/website/add', methods=['GET', 'POST'])
def website_add():
    if request.method == 'POST':
        website = Website(
            name=request.form['name'],
            identifier=request.form['identifier'],
            homepage=request.form['homepage']
        )
        db.session.add(website)
        db.session.commit()
        return redirect(url_for('website.website_list'))
    return render_template('website/form.html')

# 编辑网站
@bp.route('/website/edit/<int:id>', methods=['GET', 'POST'])
def website_edit(id):
    website = Website.query.get_or_404(id)
    if request.method == 'POST':
        website.name = request.form['name']
        website.identifier = request.form['identifier']
        website.homepage = request.form['homepage']
        db.session.commit()
        return redirect(url_for('website.website_list'))
    return render_template('website/form.html', website=website)

# 删除网站
@bp.route('/website/delete/<int:id>')
def website_delete(id):
    website = Website.query.get_or_404(id)
    db.session.delete(website)
    db.session.commit()
    return redirect(url_for('website.list')) 