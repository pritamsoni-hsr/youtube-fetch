import os
import random

from celery import chord
from flask import Flask, request, jsonify, render_template

import celeryQ
# from flask_cors import CORS

from sqlalchemy import desc
from db import setup_db, Videos

VIDEOS_PER_PAGE = 12


class AppConfig:
    DEBUG = True


app = Flask(__name__)
app.config.from_object(AppConfig())

setup_db(app)


@app.route('/<string:q>')
def videos(q):
    page = request.args.get('page', '1')
    page = int(page) if page.isdigit() else 1
    tag = request.args.get('tag', None)
    queryset = (
        Videos.query.filter(Videos.title.contains(q))
        .order_by(desc(Videos.publishedAt))

    )  # noqa
    count = queryset.count()
    if count > 0:
        queryset = queryset.paginate(page, VIDEOS_PER_PAGE, error_out=True)
        results = [v.format() for v in queryset.items]
    else:
        # run the job in worker
        chord(celeryQ.cyclic_task.s(q, None, False))(celeryQ.cyclic_task.s())
        results = 'No video found for searched query, try something else'
    return jsonify({'count': count, 'results': results, 'page': page})


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/all/')
def show_all():
    page = request.args.get('page', '1')
    page = int(page) if page.isdigit() else 1
    tag = request.args.get('tag', None)
    queryset = Videos.query.filter()
    count = queryset.count()
    queryset = queryset.paginate(page, VIDEOS_PER_PAGE, error_out=True)
    results = [v.format() for v in queryset.items]
    return jsonify({'count': count, 'results': results, 'page': page})


if __name__ == '__main__':
    app.run()
