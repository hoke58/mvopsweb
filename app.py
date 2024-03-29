"""
Author: 蒋宁
Department: 实施运维部
Date: 2024/3/1
Process：可实现对信息报送内容修改，暂无登录鉴权功能，自适应需要测试
# gzops
# P1GsL$EK
"""

from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, make_response, g
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import json
import hashlib
from urllib.parse import quote_plus as urlquote


app = Flask(__name__)
app.secret_key = 'microvideo'  # 用于安全地签名session cookie

# 测试备份数据库
SQLALCHEMY_BINDS = {
    'back': 'mysql+pymysql://root:123456@10.120.128.3/back'
    # 'back': 'mysql+pymysql://back_prozhdd:BKpr.134@192.168.211.8/prozhdd'
}

# 允许修改多少天之内的单子
ALLOWED_DAYS = 30

# 测试主数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# f'mysql+pymysql://root:{urlquote("Zhdd@2021")}@192.168.251.36/zhdd' 密码有特殊字符引起保障时，需要编码
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@10.120.128.3/zhdd'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{urlquote("Zhdd@2021")}@192.168.251.36/zhdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS


# 增加jwt校验配置
app.config['JWT_SECRET_KEY'] = 'mv-jwt-key'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False


jwt = JWTManager(app)
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
    f_createtime = db.Column(db.DateTime)



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
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


class TEventClear(db.Model):
    __tablename__ = 't_event_clear'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


class TEventConmain(db.Model):
    __tablename__ = 't_event_conmain'
    f_eventid = db.Column(db.Integer, primary_key=True)
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


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
    # f_accidentdesc = db.Column(db.String(6000))


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
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


class TEventClear2(db.Model):
    __tablename__ = 't_event_clear'
    __bind_key__ = 'back'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 更新主键字段名和类型
    f_eventid = db.Column(db.String(40), nullable=False)
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


class TEventConmain2(db.Model):
    __tablename__ = 't_event_conmain'
    __bind_key__ = 'back'
    f_eventid = db.Column(db.Integer, primary_key=True)
    # f_up_jamnum = db.Column(db.String(255))
    # f_down_jamnum = db.Column(db.String(255))


# 创建一个路由，用于获取JWT令牌
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('POST模式：获取用户')
        if request.is_json:
            username = request.json.get('username', None)
            password = request.json.get('password', None)
        else:
            username = request.form.get('username', None)
            password = request.form.get('password', None)

        # Read the username and password from auth.json
        with open('auth.json', 'r') as f:
            auth_data = json.load(f)

        # Check if the username exists in the auth_data
        if username not in auth_data:
            return jsonify({"msg": "Bad username or password"}), 401

        stored_password = auth_data[username]

        # Hash the input password
        salted_password = password + app.secret_key
        hashed_password = hashlib.md5(salted_password.encode()).hexdigest()

        if hashed_password != stored_password:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        response = make_response(redirect(url_for('index')))
        expire_date = datetime.now()
        expire_date = expire_date + timedelta(hours=8)
        response.set_cookie('access_token_cookie', access_token, expires=expire_date)
        return response
    else:
        try:
            # print('get模式：获取用户')
            current_user = get_jwt_identity()
            # print(current_user)
            if current_user:
                return redirect('/')
        except Exception as e:
            print(e)
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('access_token_cookie')

    return response


@app.before_request
@jwt_required(optional=True, locations=['cookies'])
def load_logged_in_user():
    # List of routes to exclude from authentication
    excluded_paths = ['/login', '/static/bootstrap.min.css']
    if request.path not in excluded_paths:
        try:
            current_user = get_jwt_identity()
            # print(request.form)
            if current_user:
                g.user = current_user
            else:
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', current_user=g.user)


# 修改这个路由以直接从查询字符串获取`orderid`
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        # if orderid is None:
        if request.args.get('Eorderid') is None:
            return render_template('index.html', current_user=g.user, event=None)
        orderid = request.args.get('Eorderid').strip()
        event = TEvent.query.filter_by(f_vc_orderid=orderid).first()
        retrofit_info = None

        if event:
            if not check_time(event):
                return render_template('index.html', prompt=f'订单 {orderid} 超出最大允许修改天数{ALLOWED_DAYS}天。', current_user=g.user)
            spare_info = TEventSpare.query.filter_by(f_eventid=event.f_eventid).all()
            if event.f_typeid == 0:
                retrofit_info = TEventAccidentRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            elif event.f_typeid == 1:
                retrofit_info = TEventClearRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            elif event.f_typeid == 3:
                retrofit_info = TEventConmainRetrofit.query.filter_by(f_eventid=event.f_eventid).first()
            elif event.f_typeid == 10:
                retrofit_info = TEventAbnormal.query.filter_by(f_eventid=event.f_eventid).first()
                # jam_info = None
                # 根据需要添加其他条件分支
            return render_template('index.html', event=event, retrofit_info=retrofit_info,
                                   spare_info=spare_info, current_user=g.user)

        return render_template('index.html', prompt=f'查无 {orderid} 信息，请检查', current_user=g.user)
    # POST
    else:
        orderid = request.form.get('orderid')  # 获取表单中的订单号
        print('获取表单中的订单号: ',orderid)
        try:
            event_id = request.form.get('event_id')

            # 首先获取TEvent实例
            event = TEvent.query.filter_by(f_eventid=event_id).first()

            if event:
                # 根据event.f_typeid来判断更新哪个子表
                print('修改过程总揽')
                retrofit_model = None
                if event.f_typeid == 0:
                    retrofit_model = TEventAccidentRetrofit
                    retrofit_model2 = TEventAccidentRetrofit2
                elif event.f_typeid == 1:
                    retrofit_model = TEventClearRetrofit
                    retrofit_model2 = TEventClearRetrofit2
                elif event.f_typeid == 3:
                    retrofit_model = TEventConmainRetrofit
                    retrofit_model2 = TEventConmainRetrofit2
                elif event.f_typeid == 10:
                    retrofit_model = TEventAbnormal
                    retrofit_model2 = TEventAbnormal2

                if retrofit_model:
                    # 获取子表实例
                    retrofit_info = retrofit_model.query.filter_by(f_eventid=event_id).first()
                    if retrofit_info:
                        retrofit2 = retrofit_model2.query.filter_by(f_eventid=event_id).first()
                        if retrofit2:
                            retrofit2.f_eventid = retrofit_info.f_eventid
                            retrofit2.f_vc_early = retrofit_info.f_vc_early
                            retrofit2.f_vc_renewal = retrofit_info.f_vc_renewal
                            retrofit2.f_vc_final = retrofit_info.f_vc_final
                        else:
                            retrofit2 = retrofit_model2(f_eventid=retrofit_info.f_eventid,
                                                        f_vc_early=retrofit_info.f_vc_early,
                                                        f_vc_renewal=retrofit_info.f_vc_renewal,
                                                        f_vc_final=retrofit_info.f_vc_final)
                            db.session.add(retrofit2)
                        f_vc_early = request.form.get('f_vc_early')
                        f_vc_renewal = request.form.get('f_vc_renewal')
                        f_vc_final = request.form.get('f_vc_final')
                        # 直接对实例属性赋值
                        retrofit_info.f_vc_early = f_vc_early
                        retrofit_info.f_vc_renewal = f_vc_renewal
                        # 修改终报，则主表终报一起修改
                        if retrofit_info.f_vc_final != f_vc_final:
                            retrofit_info.f_vc_final = f_vc_final
                            event.f_accidentdesc = f_vc_final

                # 更新TEventSpare表
                spare_ids = request.form.getlist('spare_id')
                for spare_id in spare_ids:
                    f_vc_renewal_spare = request.form.get(f'f_vc_renewal_spare_{spare_id}')
                    spare = TEventSpare.query.filter_by(f_vc_id=spare_id).first()
                    if spare:
                        spare2 = TEventSpare2.query.filter_by(f_vc_id=spare_id).first()
                        if spare2:
                            spare2.f_vc_id = spare.f_vc_id,
                            spare2.f_eventid = spare.f_eventid,
                            spare2.f_vc_renewal = spare.f_vc_renewal,
                            spare2.f_createtime = spare.f_createtime,
                            spare2.f_vc_spare = spare.f_vc_spare,
                            spare2.f_vc_createjopnum = spare.f_vc_createjopnum,
                            spare2.f_vc_createname = spare.f_vc_createname
                        else:
                            spare2 = TEventSpare2(f_vc_id=spare.f_vc_id,
                                                  f_eventid=spare.f_eventid,
                                                  f_vc_renewal=spare.f_vc_renewal,
                                                  f_createtime=spare.f_createtime,
                                                  f_vc_spare=spare.f_vc_spare,
                                                  f_vc_createjopnum=spare.f_vc_createjopnum,
                                                  f_vc_createname=spare.f_vc_createname)
                            db.session.add(spare2)
                        spare.f_vc_renewal = f_vc_renewal_spare
                print("提交数据库")
                db.session.commit()

                flash('修改成功', 'success')

            else:
                flash('未找到对应的事件', 'error')

        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f'修改失败: {e}', 'error')
        print('update done!')

        return redirect(url_for('edit', Eorderid=orderid))




@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        orderid = request.form.get('orderid').strip()
        event = TEvent.query.filter_by(f_vc_orderid=orderid).first()
        print(event.f_create_time)

        if event:
            # f_eventstate 0进行中，1结案
            # f_state 事件进展状态 1-10
            # 进行结案与恢复操作

            event2 = TEvent2.query.filter_by(f_eventid=event.f_eventid).first()
            if event2:
                event2.f_eventid = event.f_eventid
                event2.f_state = event.f_state
                event2.f_eventstate = event.f_eventstate
                # event2.f_accidentdesc = event.f_accidentdesc
                event2.f_typeid = event.f_typeid
                event2.f_vc_orderid = event.f_vc_orderid
            else:
                event2 = TEvent2(f_eventid=event.f_eventid,
                                 f_state=event.f_state,
                                 f_eventstate=event.f_eventstate,
                                 f_typeid=event.f_typeid,
                                 f_vc_orderid=event.f_vc_orderid)
            db.session.add(event2)

            if str(event.f_eventstate) == '1':
                event.f_state = '9'
                event.f_eventstate = '0'
            elif str(event.f_eventstate) == '0':
                event.f_state = '10'
                event.f_eventstate = '1'
            print('事件恢复')

            db.session.commit()
            return render_template('search.html', event=event, current_user=g.user)

        prompt = orderid
        return render_template('search.html', prompt=prompt, current_user=g.user)
    else:
        if request.args.get('Sorderid') is None:
            return render_template('search.html',current_user=g.user)

        orderid = request.args.get('Sorderid').strip()
        event = TEvent.query.filter_by(f_vc_orderid=orderid).first()

        if event:
            if check_time(event):
                return render_template('search.html', event=event, current_user=g.user)
            else:
                return render_template('search.html', prompt=f'订单{orderid}超出最大允许修改天数{ALLOWED_DAYS}天。', current_user=g.user)
        else:
            return render_template('search.html', prompt=f'查无{orderid}信息，请检查', current_user=g.user)


def check_time(event):
    today = datetime.today()
    event_createtime = datetime.strptime(event.f_createtime.strftime('%Y-%m-%d'), '%Y-%m-%d')
    delta = today - event_createtime

    if delta.days > ALLOWED_DAYS:
        return False
    return True



if __name__ == '__main__':
    # python3 -m flask run --host=0.0.0.0 --port=5000
    app.run(debug=True, host='0.0.0.0', port=8080)
