"""
Author: 蒋宁
Department: 实施运维部
Date: 2024/3/1
Process：可实现对信息报送内容修改，暂无登录鉴权功能，自适应需要测试
"""

from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'microvideo'  # 用于安全地签名session cookie

# 数据库配置
DB_DIALECT = 'mysql'
DB_DRIVER = 'pymysql'
DB_USERNAME = 'root'
DB_PASSWORD = 'Zhdd@2021'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'zhdd'

app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/zhdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 定义数据库模型省略...
class TEvent(db.Model):
    __tablename__ = 't_event'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_orderid = db.Column(db.String(255), unique=True)
    f_typeid = db.Column(db.Integer)
    f_state = db.Column(db.String(255))
    f_eventstate = db.Column(db.String(255))

class TEventAccidentRetrofit(db.Model):
    __tablename__ = 't_event_accident_retrofit'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventClearRetrofit(db.Model):
    __tablename__ = 't_event_clear_retrofit'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventConmainRetrofit(db.Model):
    __tablename__ = 't_event_conmain_retrofit'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventAbnormal(db.Model):
    __tablename__ = 't_event_abnormal'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventSpare(db.Model):
    __tablename__ = 't_event_spare'
    f_vc_id = db.Column(db.String(40), primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)  # 确保类型为String且与数据库一致
    f_vc_renewal = db.Column(db.String(6000))
    f_createtime = db.Column(db.DateTime)
    f_vc_spare = db.Column(db.String(255))
    f_vc_createjopnum = db.Column(db.String(255))
    f_vc_createname = db.Column(db.String(255))


# 添加其他子表模型...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('query', orderid=request.form['orderid']))
    return render_template('index.html')

# 修改这个路由以直接从查询字符串获取`orderid`
@app.route('/query', methods=['GET'])
def query():
    orderid = request.args.get('orderid')
    event = TEvent.query.filter_by(f_vc_orderid=orderid).first()
    retrofit_info = None
    spare_info = []  # 在这里初始化spare_info为一个空列表
    if event:
        if event.f_typeid == 0:
            retrofit_info = TEventAccidentRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 1:
            retrofit_info = TEventClearRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 3:
            retrofit_info = TEventConmainRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 10:
            retrofit_info = TEventAbnormal.query.filter_by(f_eventid=event.f_eventid).first()
        spare_info = TEventSpare.query.filter_by(f_eventid=event.f_eventid).all()
            # 根据需要添加其他条件分支
            # ...
    return render_template('results.html', event=event, retrofit_info=retrofit_info, spare_info=spare_info)

@app.route('/update', methods=['POST'])
def update():
    orderid = request.form.get('orderid')  # 获取表单中的订单号

    try:
        event_id = request.form.get('event_id')
        f_state = request.form.get('f_state')
        f_eventstate = request.form.get('f_eventstate')

        # 首先获取TEvent实例
        event = TEvent.query.filter_by(f_eventid=event_id).first()
        if event:
            event.f_state = f_state
            event.f_eventstate = f_eventstate

            # 根据event.f_typeid来判断更新哪个子表
            retrofit_model = None
            if event.f_typeid == 0:
                retrofit_model = TEventAccidentRetrofit
            elif event.f_typeid == 1:
                retrofit_model = TEventClearRetrofit
            elif event.f_typeid == 3:
                retrofit_model = TEventConmainRetrofit
            elif event.f_typeid == 10:
                retrofit_model = TEventAbnormal

            if retrofit_model:
                # 获取子表实例
                retrofit = retrofit_model.query.filter_by(f_eventid=event_id).first()
                if retrofit:
                    f_vc_early = request.form.get('f_vc_early')
                    f_vc_renewal = request.form.get('f_vc_renewal')
                    f_vc_final = request.form.get('f_vc_final')
                    # 直接对实例属性赋值
                    retrofit.f_vc_early = f_vc_early
                    retrofit.f_vc_renewal = f_vc_renewal
                    retrofit.f_vc_final = f_vc_final

            # 更新TEventSpare表
            spare_ids = request.form.getlist('spare_id')
            for spare_id in spare_ids:
                f_vc_renewal_spare = request.form.get(f'f_vc_renewal_spare_{spare_id}')
                spare = TEventSpare.query.filter_by(f_vc_id=spare_id).first()
                if spare:
                    spare.f_vc_renewal = f_vc_renewal_spare

            db.session.commit()
            flash('修改成功', 'success')
        else:
            flash('未找到对应的事件', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'修改失败: {e}', 'error')

    return redirect(url_for('query', orderid=orderid))


if __name__ == '__main__':
    app.run(debug=True)
