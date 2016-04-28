# coding=utf-8

from flask import Flask
from flask import render_template, redirect
import db
import json
import settings


app = Flask(__name__)


@app.route("/test")
def test():
    return "OK"


@app.route("/")
def index():
    return redirect("/static/nacional.html")

@app.route('/<school_id>')
def get_school_info(school_id):
    conn = db.connect(settings.DB_HOST, settings.DB_USER, 
        settings.DB_PASSWD, settings.DB_NAME)
    
    # school uf
    school_uf = db.get_school_uf(conn, school_id)
    if school_uf is not None:
        uf_score_avg = db.get_uf_score_avg(conn, school_uf)
    school_city = db.get_school_city(conn, school_id)
    if school_city is not None:
        city_score_avg = db.get_city_score_avg(conn, school_city)
        
    # num students
    total_students = db.get_total_lines(conn, school_id)
    total_absents = db.get_total_absents(conn, school_id)
    
    # avg
    avg_score1, avg_score2, avg_score3, avg_score4, avg_score5, avg_total = db.get_score_avg(conn, school_id)
    
    # sex
    score_avg_sex = db.get_score_avg_sex(conn, school_id)
       
    # score interval
    score_count = [
        db.get_count_per_score_interval(conn, 0, 0, school_id),
        db.get_count_per_score_interval(conn, 1, 99, school_id),
        db.get_count_per_score_interval(conn, 100, 199, school_id),
        db.get_count_per_score_interval(conn, 200, 299, school_id),
        db.get_count_per_score_interval(conn, 300, 399, school_id),
        db.get_count_per_score_interval(conn, 400, 499, school_id),
        db.get_count_per_score_interval(conn, 500, 599, school_id),
        db.get_count_per_score_interval(conn, 600, 699, school_id),
        db.get_count_per_score_interval(conn, 700, 799, school_id),
        db.get_count_per_score_interval(conn, 800, 899, school_id),
        db.get_count_per_score_interval(conn, 900, 999, school_id),
        db.get_count_per_score_interval(conn, 1000, 1000, school_id)
    ]

    db.close_connection(conn)

    score_interval_data = [
        ['notas', 'alunos', { 'role': 'annotation' }],
        ["0", int(score_count[0]), int(score_count[0])],
        ["1-99", int(score_count[1]), int(score_count[1])],
        ["100-199", int(score_count[2]), int(score_count[2])],
        ["200-299", int(score_count[3]), int(score_count[3])],
        ["300-399", int(score_count[4]), int(score_count[4])],
        ["400-499", int(score_count[5]), int(score_count[5])],
        ["500-599", int(score_count[6]), int(score_count[6])],
        ["600-699", int(score_count[7]), int(score_count[7])],
        ["700-799", int(score_count[8]), int(score_count[8])],
        ["800-899", int(score_count[9]), int(score_count[9])],
        ["900-999", int(score_count[10]), int(score_count[10])],
        ["1000", int(score_count[11]), int(score_count[11])]
    ]
    
    return render_template('school_info.html', **locals())


if __name__ == "__main__":
    app.debug = False
    app.run()
