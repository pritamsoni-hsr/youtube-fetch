from __future__ import absolute_import, unicode_literals
import random
from celery import Celery, chord
from decouple import config
from tasks import fetch_data


class CeleryConfig:
    CELERY_BROKER_URL = config(
        'CELERY_BROKER_URL', default='redis://127.0.0.1:6379'
    )  # noqa
    CELERY_TIMEZONE = config('CELERY_TIMEZONE', default='UTC')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_RESULT_PERSISTENT = True


app = Celery('YT')
app.config_from_object(CeleryConfig(), namespace='CELERY')
paginationToken = config('TOKEN', cast=str, default=None)
#################
#   Variables
#################

topQueries = ['football', 'bhand', 'avengers', 'cricket', 'marvels', 'batman', 'superman', 'twenty one pilots', 'temp', 'lindsey', 'Load', 'Peace', 'C.G.', 'Tec', 'DepC', 'DC++', 'Maggu', 'Makhana', 'Machana', 'Stud', 'Tempo', 'Junta', 'Dep', 'Prof', 'V.P.', 'P.S.I.', 'Fakka', 'Faccha', 'Facchi', 'G.P.L.', 'Funda', 'Happa', 'FacAd', 'H.O.D.', 'Pakau', 'Illu', 'O.P.', 'Intro', 'P.P.O.', 'P.P.T.', 'T.O.A.T.', 'Panji', 'Chhagi', 'Satti', 'Atthi', 'Nehli', 'Dehli', 'Dassi', 'D.P.', 'Banda', 'Bandi', 'Bhajan', 'Pondy', 'Bhaat', 'Batti', 'Ghaasi', 'Indu', 'Meta', 'Lohar', 'Fight', 'Chhedis', 'D.O.S.A.', 'Acads', 'Archi', 'Taapna', 'Soc', 'Secy', 'Room', 'R.D.C.', 'Maal', 'Matka', 'Matki', ]  # noqa


def get_query(): return topQueries[random.randint(0, len(topQueries)-1)]  # noqa


#################
#    Tasks
#################
@app.task
def fetchStore(query):
    print(query[0])
    query = query[0]
    token, _ = fetch_data(**query)
    return (token, _)


@app.task
def set_query(query):
    # was using to dynamically set query, didn't work out.
    return {"query": query}


@app.task
def cyclic_task(*args):
    # used to query dynamically celery doesn't provide this.
    if len(args) != 3:
        return args
    if args[2]:
        token, _ = fetch_data(query=args[0], token=args[1])
        if token =='End of results':  # if end of results update query
            token, _ = fetch_data(query=get_query(), token=args[1])
    else:
        token, _ = None, False

    return args[0], token, _


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0, fetchStore.s(query=get_query()), name='FETCH DATA')  # noqa

    # sender.add_periodic_task(20.0, set_query.s('world'), name='UPDATE QUERY', expires=10)  # noqa

    # sender.add_periodic_task(10.0, chord(set_query.s('worhjl'))(fetchStore.s()), name='CHORD QUERY')  # noqa
    sender.add_periodic_task(10.0, chord(cyclic_task.s(get_query(), paginationToken, False))(cyclic_task.s()), name='CHORD QUERY')  # noqa
