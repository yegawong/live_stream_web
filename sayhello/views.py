# -*- coding: utf-8 -*-
"""
    :author: (Yega)
    :copyright: © 2021 yega
    :license: MIT, see LICENSE for more details.
"""
import datetime
import psutil
import time
from flask import flash, redirect, url_for, render_template, request

from sayhello import app, db
from sayhello.models import Message, Adress
from sayhello.auth import generate_adress
from sayhello.forward import live, stop_live


@app.route('/', methods=['GET', 'POST'])
def index():
    address = generate_adress()
    site_messages = Message.query.order_by(Message.timestamp.desc()).all()
    starttask_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_status = 'STOP'
    task_cnt = 0
    if site_messages:
        task_status = 'RUN'
        task_cnt = len(site_messages)
        start_time = site_messages[-1].timestamp + datetime.timedelta(hours=8)
        starttask_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html',
                           site_messages=site_messages,
                           address=address,
                           starttask_time=starttask_time,
                           task_status=task_status,
                           task_cnt=task_cnt,
                           )


@app.route('/starttask', methods=['POST'])
def starttask():
    if request.method == 'POST':
        result = request.form
        if 'name' in result and 'url' in result and result['name'] and result['url']:
            pid = start_task(result['name'], result['url'])
            flash('{} 开始转播, pid: {}'.format(result['name'], pid))
    return redirect(url_for('index'))


def start_task(name, url):
    adress = Adress.query.all()
    if not adress:
        return -1
    res = Adress.query.filter_by(id=adress[0].id).first()
    rtmp_laliu = res.rtmp
    pid = live(rtmp_laliu, url)
    if pid == 0:
        flash('{} 开始转播失败, 请重新提交'.format(name))
        return redirect(url_for('index'))
    site_message = Message(pid=pid, url=url, name=name)
    db.session.add(site_message)
    db.session.commit()
    return pid


@app.route('/stoptask', methods=['POST'])
def stoptask():
    if request.method == 'POST':
        result = request.form
        if 'stop_alltask' in result:
            delete_all_task()
            flash('全部停止转播')
        elif 'stop_onetask' in result and result['stop_onetask']:
            delete_task(result['stop_onetask'])
            flash('{} 停止转播'.format(result['stop_onetask']))
    return redirect(url_for('index'))


def delete_task(task_name):
    site_message = Message.query.filter_by(name=task_name).first()
    pid = int(site_message.pid)
    stop_live(pid)
    stop_live(pid+1)
    db.session.delete(site_message)
    db.session.commit()


def delete_all_task():
    site_message = Message.query.all()
    if not site_message:
        return
    for task in site_message:
        delete_task(task.name)

@app.route('/getinfo', methods=['GET'])
def getinfo():
    cpu, memory = getMemCpu()
    return {'cpu':cpu, 'memory':memory}

last_time = 0
last_cpu = 0
last_memory = 0
def getMemCpu():
    global last_time, last_cpu, last_memory
    delta_time = time.time() - last_time
    if last_time != 0 and delta_time < 30:
        return last_cpu, last_memory
    data = psutil.virtual_memory()
    total = data.total #总内存,单位为byte
    free = data.available #可以内存
    memory = "%d"%(int(round(data.percent)))
    cpu = "%d"%psutil.cpu_percent(interval=1)
    last_time = time.time()
    last_cpu, last_memory = cpu, memory
    return cpu, memory