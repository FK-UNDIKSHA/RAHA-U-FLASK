# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from apps import db
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.forms import LoginForm, DoctorProfileForm
from apps.authentication.models import Users, Pengguna, Dokter

@blueprint.route('/demo')
@login_required
def index_demo():

    return render_template('home/index_demo.html', segment='demo')


@blueprint.route('/index')
@login_required
def index():

    if str(current_user.role[0]) == 'admin':
        return render_template('home/index.html', segment='index')
    elif str(current_user.role[0]) == 'dokter':
        return render_template('home/index_dokter.html', segment='index')
    else:
        return render_template('home/index_pasien.html', segment='index')

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def Profile():
    msg = ""
    #After POST THEN RENDER
    if str(current_user.role[0]) == 'admin':
        return render_template('home/profile.html', segment='profile')
    elif str(current_user.role[0]) == 'dokter':
        #form_changer = DoctorProfileForm(request.form)
        print(request.form)
        dokter = Dokter.query.filter_by(username=current_user.username).first()
        user = Users.query.filter_by(username=current_user.username).first()

        if request.method == "POST":
            email = request.form['email']
            no_str = request.form['no_str']
            nama = request.form['nama']
            alamat = request.form['alamat']

            user.email = email
            dokter.no_str = no_str
            dokter.nama = nama
            dokter.alamat = alamat
            #db.session.add(dokter)
            db.session.commit()
            msg = "Profile Changed"

        return render_template('home/profile_dokter.html', segment='profile', success=True, msg=msg, dokter=dokter)
    else:
        user = Users.query.filter_by(username=current_user.username).first()
        pengguna = Pengguna.query.filter_by(username=current_user.username).first()
        if request.method == "POST":
            email = request.form['email']
            nik = request.form['nik']
            nama = request.form['nama']
            alamat = request.form['alamat']

            user.email = email
            pengguna.nik = nik
            pengguna.nama = nama
            pengguna.alamat = alamat
            db.session.commit()
            msg = "Profile Changed"
        return render_template('home/profile_pasien.html', segment='profile', pengguna=pengguna)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
