# coding=utf-8

import json
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("conf/config.cfg")

db_obj = SQLAlchemy(app)


class Notice(db_obj.Model):

    id = db_obj.Column(db_obj.Integer, primary_key=True, autoincrement=True)
    title = db_obj.Column(db_obj.String(20))
    content = db_obj.Column(db_obj.Text)
    pub_date = db_obj.Column(db_obj.Date, default=datetime.now())
    status = db_obj.Column(db_obj.SmallInteger, default=0)

    __tablename__ = 'notice'

    def __repr__(self):
        return '<Notice %r>' % self.title

    @staticmethod
    def init_db():
        # 删除表
        print("开始删除表...")
        db_obj.drop_all()

        # 创建表
        print("开始创建表...")
        db_obj.create_all()

        # 增加记录
        print("开始添加记录...")
        notice1 = Notice(title='新用户注册说明', content='充值页面上，多了个6元的首充特惠。充值6元后即可得12红豆，再加上188元大礼包中18元直减券，相当于6元即可购买专家28元的方案。188元大礼包是在新用户注册后，绑定手机号，即可领取。')
        notice2 = Notice(title='购买会员说明', content='需要加入VIP的请点击以下图标充值后加入 游客无法加入 需要先注册成为本站会员后方可加入 购买过任何本站收费内容的可点击右侧导航条上的QQ在线咨询 并提供你注册的会员名用来核实 如果需要加入本站QQ群请先互加好友并告知 我会发送群邀请给你。')
        notice3 = Notice(title='优惠券使用说明', content='优惠券有使用期限限制，过了有效期不能使用；订单中包含特价商品时不能使用优惠券，优惠券不能与其他优惠（如促销活动）同时使用；优惠券只能抵扣订单金额，优惠金额超出订单金额部分不能再次使用，不能兑换现金；')

        db_obj.session.add(notice1)
        db_obj.session.add(notice2)
        db_obj.session.add(notice3)

        db_obj.session.commit()


@app.route("/", methods=["GET"])
def test():
    return "hello flask!"


# 获取轮播图列表
@app.route("/rotation_images", methods=["GET"])
def rotation_images():
    rotation_image_dict = ["static/img/lunbo_1.jpg", "static/img/lunbo_2.jpg", "static/img/lunbo_3.jpg"]
    return json.dumps({"data": rotation_image_dict})


# 获取公告列表
@app.route("/notices", methods=["GET"])
def notices():
    notices = Notice.query.all()

    notices_list = [{"id": i.id, "title": i.title, "content": i.content} for i in notices]
    print(notices_list)

    return json.dumps({"data": notices_list})


if __name__ == "__main__":

    Notice.init_db()

    app.run(host="0.0.0.0", port=10010, debug=True)
