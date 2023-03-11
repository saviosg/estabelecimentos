from bson import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import login_required
from forms import EstabelecimentoForm
from elastic import es
from mongo import mongo

routes = Blueprint('routes', __name__)
es_routes = Blueprint('elastic', __name__, url_prefix='/elastic')
mongo_routes = Blueprint('mongo', __name__, url_prefix='/mongo')
routes.register_blueprint(es_routes)
routes.register_blueprint(mongo_routes)

@routes.get('/')
@login_required
def homepage():
    return redirect(url_for('routes.elastic.es_list'))

@routes.get('/todo/')
@login_required
def todo():
    return render_template('todo.html')

@es_routes.get('/')
@login_required
def es_list():
    resp = es.search(index='estabelecimentos', ignore_unavailable=True, query={'match_all': {}})
    documents = [doc['_source'] | { 'id': doc['_id'] } for doc in resp['hits']['hits']]
    return render_template('list.html', documents=documents)

@es_routes.get('/new')
@login_required
def es_add_page():
    form = EstabelecimentoForm()
    return render_template('edit.html', form=form)

@es_routes.post('/new')
@login_required
def es_add_send():
    form = EstabelecimentoForm(request.form)
    success = form.validate_on_submit()
    if success:
        es.index(index='estabelecimentos', document=form.data, refresh='wait_for')
        flash('Adicionado com sucesso', 'success')
        return redirect(url_for('routes.elastic.es_list'))
    else:
        return render_template('edit.html', form=form, document=form.data)

@es_routes.get('/edit/<id>')
@login_required
def es_edit(id):
    doc = es.get(index='estabelecimentos', id=id)
    form = EstabelecimentoForm()
    return render_template('edit.html', form=form, document=doc['_source'] | { 'id': doc['_id'] })

@es_routes.post('/edit/<id>')
@login_required
def es_save(id):
    form = EstabelecimentoForm(request.form)
    success = form.validate_on_submit()
    if success:
        es.update(index='estabelecimentos', id=id, doc=form.data, refresh='wait_for')
        flash('Alterado com sucesso', 'success')
        return redirect(url_for('routes.elastic.es_list'))
    else:
        return render_template('edit.html', form=form, document=form.data)

@es_routes.post('/delete/<id>')
@login_required
def es_delete(id):
    es.delete(index='estabelecimentos', id=id, refresh='wait_for')
    flash('Removido com sucesso', 'success')
    return redirect(url_for('routes.elastic.es_list'))

@mongo_routes.get('/')
@login_required
def mongo_list():
    resp = mongo.estabelecimentos.find({})
    documents = [doc | { 'id': doc['_id'] } for doc in resp]
    return render_template('list.html', documents=documents)

@mongo_routes.get('/new')
@login_required
def mongo_add_page():
    form = EstabelecimentoForm()
    return render_template('edit.html', form=form)

@mongo_routes.post('/new')
@login_required
def mongo_add_send():
    form = EstabelecimentoForm(request.form)
    success = form.validate_on_submit()
    if success:
        mongo.estabelecimentos.insert_one(form.data)
        flash('Adicionado com sucesso', 'success')
        return redirect(url_for('routes.mongo.mongo_list'))
    else:
        return render_template('edit.html', form=form, document=form.data)

@mongo_routes.get('/edit/<id>')
@login_required
def mongo_edit(id):
    doc = mongo.estabelecimentos.find_one({ '_id': ObjectId(id) })
    form = EstabelecimentoForm()
    return render_template('edit.html', form=form, document=doc | { 'id': doc['_id'] })

@mongo_routes.post('/edit/<id>')
@login_required
def mongo_save(id):
    form = EstabelecimentoForm(request.form)
    success = form.validate_on_submit()
    if success:
        mongo.estabelecimentos.update_one({ '_id': ObjectId(id) }, { '$set': form.data })
        flash('Alterado com sucesso', 'success')
        return redirect(url_for('routes.mongo.mongo_list'))
    else:
        return render_template('edit.html', form=form, document=form.data)

@mongo_routes.post('/delete/<id>')
@login_required
def mongo_delete(id):
    mongo.estabelecimentos.delete_one({ '_id': ObjectId(id) })
    flash('Removido com sucesso', 'success')
    return redirect(url_for('routes.mongo.mongo_list'))
