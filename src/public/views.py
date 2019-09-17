"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template
from .forms import LogUserForm, secti,masoform,vstupnitestform
from ..data.database import db
from ..data.models import LogUser
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET','POST'])
def vstupnitest():
    from ..data.models import Vysledky
    from flask import flash
    form = vstupnitestform()
    if form.validate_on_submit():
        vysledek=0
        if form.otazka1.data ==2:
            vysledek=vysledek+1
        if form.otazka2.data ==0:
            vysledek=vysledek+1
        if form.otazka3.data.upper() == "ELEPHANT":
            vysledek=vysledek+1
            i = Vysledky(username=form.Jmeno.data,hodnoceni=vysledek)
            db.session.add(i)
            db.session.commit()
            flash("Vysledek ulozen", category="Error")
            return str(vysledek)
    return render_template('public/vstupnitest.tmpl', form=form)
