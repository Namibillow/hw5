#!/anaconda3/envs/py27/bin/python
# -*- coding: utf-8 -*-


from google.appengine.api import urlfetch
import json
from flask import Flask, render_template, request, redirect
import sys
from itertools import izip_longest as zip_longest
import random

import bfs
import utils
import dijkstra

app = Flask(__name__)
app.debug = True

### LOAD JSON FILES #######
networkJson = urlfetch.fetch("http://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

outtagesJson = urlfetch.fetch("http://fantasy-transit.appspot.com/outtages?format=json").content
outtages = json.loads(outtagesJson.decode('utf-8'))

timeJson = urlfetch.fetch('http://fantasy-transit.appspot.com/schedules?format=json').content
timeSchedule = json.loads(timeJson.decode('utf-8'))


############################
#
NUM_STATIONS = 122
CHOICES = ['fastest', 'easiest', 'shortest']
LINE_COLORS = {'東横線': '#fc8d62', '池上線': '#e78ac3', '大井町線': "#ffd92f", "山手線": '#66c2a5', "目黒線": '#8da0cb', "多摩川線": "#a6d854", "日比谷線": '#e5c494'}


@app.route('/')
# / のリクエスト（例えば http://localhost:8080/ ）をこの関数で処理する。
# ここでメニューを表示をしているだけです。
def root():
    return render_template('hello.html')


@app.route('/pata', methods=['GET', 'POST'])
# /pata のリクエスト（例えば http://localhost:8080/pata ）をこの関数で処理する。
# これをパタトクカシーーを処理するようにしています。
def pata():
    if request.method == "POST":

        word1 = [ch for ch in request.form.get('word1')]
        word2 = [ch for ch in request.form.get('word2')]

        # if one of a word exists, then perform an alternative merge
        if word1 or word2:
            pata = [v for v in sum(zip_longest(word1, word2), ()) if v is not None]
            pata = ''.join(pata)
            word1 = ''.join(word1)
            word2 = ''.join(word2)
        else:
            pata = None

            # pata.htmlのテンプレートの内容を埋め込んで、返事を返す。
        return render_template('pata.html', word={"word1": word1, "word2": word2}, pata=pata)
    else:
        return render_template('pata.html')


@app.route('/norikae', methods=['GET', 'POST'])
# /norikae のリクエスト（例えば http://localhost:8080/norikae ）をこの関数で処理する。
# ここで乗り換え案内をするように編集してください。
def norikae():
    if request.method == "POST":
        start = request.form.get('start')
        dest = request.form.get('dest')
        choice = request.form.get('options')
        date = request.form.get('date')
        input_time = date.split()[1].split(':')
        # print(date)
        # print(date.split()[1].split(':'))

        # CASE 1: if start and dest is the same:
        if start == dest:
            return "It's same whyyyy"
        else:
            if choice == CHOICES[0]:
                # if non-weighted graph
                connect_list = utils.create_pairs(network)
                graph = utils.build_graph(connect_list, outtages)
                path, dist = bfs.print_bfs(graph, start, dest)

            elif choice == CHOICES[1]:
                pass
            elif choice == CHOICES[2]:
                graph = utils.build_weighted_graph(timeSchedule)
                dijkstra.print_dfs(graph, start, dest)
                schedules = utils.process_timeJson(timeSchedule)
                path, dist = None, None

        # return redirect('/')
        return render_template('result.html', path=path, dist=dist, time=None)
    else:
        rand_num = [random.randint(1, NUM_STATIONS + 1) for _ in range(2)]

        return render_template('norikae.html', network=network, selected_stations=rand_num)
