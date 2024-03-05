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

# 需要绑定的备份数据库
SQLALCHEMY_BINDS = {
    'back': 'mysql+pymysql://root:123456@10.120.128.0/back'
}

# 生产数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@10.120.128.0/zhdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# 定义数据库模型省略...
class TEvent(db.Model):
    __tablename__ = 't_event'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_orderid = db.Column(db.String(255), unique=True)
    f_typeid = db.Column(db.Integer)
    f_state = db.Column(db.String(255))
    f_eventstate = db.Column(db.String(255))
    f_accidentdesc = db.Column(db.String(6000))

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

class TEventAccident(db.Model):
    __tablename__ = 't_event_accident'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))

class TEventClear(db.Model):
    __tablename__ = 't_event_clear'
    id = db.Column(db.String(40), primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))

class TEventConmain(db.Model):
    __tablename__ = 't_event_conmain'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))

# 添加其他子表模型...

##### for backing
class TEvent2(db.Model):
    __tablename__ = 't_event'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_orderid = db.Column(db.String(255), unique=True)
    f_typeid = db.Column(db.Integer)
    f_state = db.Column(db.String(255))
    f_eventstate = db.Column(db.String(255))
    f_accidentdesc = db.Column(db.String(6000))

class TEventAccidentRetrofit2(db.Model):
    __tablename__ = 't_event_accident_retrofit'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventClearRetrofit2(db.Model):
    __tablename__ = 't_event_clear_retrofit'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventConmainRetrofit2(db.Model):
    __tablename__ = 't_event_conmain_retrofit'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventAbnormal2(db.Model):
    __tablename__ = 't_event_abnormal'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_vc_early = db.Column(db.String(255))
    f_vc_renewal = db.Column(db.String(255))
    f_vc_final = db.Column(db.String(255))

class TEventSpare2(db.Model):
    __tablename__ = 't_event_spare'
    __bind_key__ = 'back'
    f_vc_id = db.Column(db.String(40), primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)  # 确保类型为String且与数据库一致
    f_vc_renewal = db.Column(db.String(6000))
    f_createtime = db.Column(db.DateTime)
    f_vc_spare = db.Column(db.String(255))
    f_vc_createjopnum = db.Column(db.String(255))
    f_vc_createname = db.Column(db.String(255))

class TEventAccident2(db.Model):
    __tablename__ = 't_event_accident'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))

class TEventClear2(db.Model):
    __tablename__ = 't_event_clear'
    __bind_key__ = 'back'
    id = db.Column(db.String(40), primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))

class TEventConmain2(db.Model):
    __tablename__ = 't_event_conmain'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    f_up_jamnum = db.Column(db.String(255))
    f_down_jamnum = db.Column(db.String(255))



@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


# 修改这个路由以直接从查询字符串获取`orderid`
@app.route('/query', methods=['GET'])
# @jwt_required()
def query():
    orderid = request.args.get('orderid')
    event = TEvent.query.filter_by(f_vc_orderid=orderid).first()

    retrofit_info = None
    spare_info = []  # 在这里初始化spare_info为一个空列表
    if event:
        if event.f_typeid == 0:
            retrofit_info = TEventAccidentRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            jam_info = TEventAccident.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 1:
            retrofit_info = TEventClearRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            jam_info = TEventClear.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 3:
            retrofit_info = TEventConmainRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            jam_info = TEventConmain.query.filter_by(f_eventid=event.f_eventid).first()
        elif event.f_typeid == 10:
            retrofit_info = TEventAbnormal.query.filter_by(f_eventid=event.f_eventid).first()

        spare_info = TEventSpare.query.filter_by(f_eventid=event.f_eventid).all()
            # 根据需要添加其他条件分支
            # ...
    return render_template('results.html', event=event, retrofit_info=retrofit_info, jam_info=jam_info, spare_info=spare_info)

@app.route('/update', methods=['POST'])
# @jwt_required()
def update():
    orderid = request.form.get('orderid')  # 获取表单中的订单号

    try:
        event_id = request.form.get('event_id')
        f_state = request.form.get('f_state')
        f_eventstate = request.form.get('f_eventstate')
        f_accidentdesc = request.form.get('f_accidentdesc')

        # 首先获取TEvent实例
        event = TEvent.query.filter_by(f_eventid=event_id).first()

        if event:
            event2 = TEvent2.query.filter_by(f_eventid=event_id).first()
            event2.f_eventid=event.f_eventid,
            event2.f_state=event.f_state,
            event2.f_eventstate=event.f_eventstate,
            event2.f_accidentdesc=event.f_accidentdesc,
            event2.f_typeid=event.f_typeid,
            event2.f_vc_orderid=event.f_vc_orderid
            # db.session.add(event2)
            event.f_state = f_state
            event.f_eventstate = f_eventstate
            event.f_accidentdesc = f_accidentdesc

            # 根据event.f_typeid来判断更新哪个子表
            retrofit_model = None
            jam_model = None
            if event.f_typeid == 0:
                retrofit_model = TEventAccidentRetrofit
                jam_model = TEventAccident
                retrofit_model2 = TEventAccidentRetrofit2
                jam_model2 = TEventAccident2
            elif event.f_typeid == 1:
                retrofit_model = TEventClearRetrofit
                jam_model = TEventClear
                retrofit_model2 = TEventClearRetrofit2
                jam_model2 = TEventClear2
            elif event.f_typeid == 3:
                retrofit_model = TEventConmainRetrofit
                jam_model = TEventConmain
                retrofit_model2 = TEventConmainRetrofit2
                jam_model2 = TEventConmain2
            elif event.f_typeid == 10:
                retrofit_model = TEventAbnormal
                retrofit_model2 = TEventAbnormal2

            if jam_model:
                # 获取子表实例
                jam = jam_model.query.filter_by(f_eventid=event_id).first()
                if jam:
                    jam2 = jam_model2.query.filter_by(f_eventid=event_id).first()
                    jam2.f_eventid=jam.f_eventid,
                    jam2.f_up_jamnum=jam.f_up_jamnum,
                    jam2.f_down_jamnum=jam.f_down_jamnum
                    # db.session.add(jam2)
                    f_up_jamnum = request.form.get('f_up_jamnum')
                    f_down_jamnum = request.form.get('f_down_jamnum')
                    # 直接对实例属性赋值
                    jam.f_up_jamnum = f_up_jamnum
                    jam.f_down_jamnum = f_down_jamnum

            if retrofit_model:
                # 获取子表实例
                retrofit = retrofit_model.query.filter_by(f_eventid=event_id).first()
                if retrofit:
                    retrofit2 = retrofit_model2.query.filter_by(f_eventid=event_id).first()
                    retrofit2.f_eventid=retrofit.f_eventid,
                    retrofit2.f_eventidf_vc_early=retrofit.f_vc_early,
                    retrofit2.f_eventidf_vc_renewal=retrofit.f_vc_renewal,
                    retrofit2.f_eventidf_vc_final=retrofit.f_vc_final
                    # db.session.add(retrofit2)
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
                    spare2 = TEventSpare2.query.filter_by(f_vc_id=spare_id).first()
                    spare2.f_vc_id=spare.f_vc_id,
                    spare2.f_eventid=spare.f_eventid,
                    spare2.f_vc_renewal=spare.f_vc_renewal,
                    spare2.f_createtime=spare.f_createtime,
                    spare2.f_vc_spare=spare.f_vc_spare,
                    spare2.f_vc_createjopnum=spare.f_vc_createjopnum,
                    spare2.f_vc_createname=spare.f_vc_createname
                    db.session.add(spare2)
                    spare.f_vc_renewal = f_vc_renewal_spare
            print("提交数据库")
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
