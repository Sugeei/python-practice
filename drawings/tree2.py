from turtle import *
from turtle import Turtle
import turtle
from random import *
from math import *


def tree(tobj, n, l):
    tobj.pd()  # 下笔
    # 阴影效果
    t = cos(radians(tobj.heading() + 45)) / 8 + 0.25
    tobj.pencolor(t, t, t)
    tobj.pensize(n / 3)
    tobj.forward(l)  # 画树枝

    if n > 0:
        b = random() * 15 + 10  # 右分支偏转角度
        c = random() * 15 + 10  # 左分支偏转角度
        d = l * (random() * 0.25 + 0.7)  # 下一个分支的长度
        # 右转一定角度,画右分支
        tobj.right(b)
        tree(tobj, n - 1, d)
        # 左转一定角度，画左分支
        tobj.left(b + c)
        tree(tobj, n - 1, d)
        # 转回来
        tobj.right(c)
    else:
        # 画叶子
        tobj.right(90)
        n = cos(radians(tobj.heading() - 45)) / 4 + 0.5
        tobj.pencolor(n, n * 0.8, n * 0.8)
        tobj.circle(3)
        tobj.left(90)
        # 添加0.3倍的飘落叶子
        if (random() > 0.7):
            tobj.pu()
            # 飘落
            t = tobj.heading()
            an = -40 + random() * 40
            tobj.setheading(an)
            dis = int(800 * random() * 0.5 + 400 * random() * 0.3 + 200 * random() * 0.2)
            tobj.forward(dis)
            tobj.setheading(t)
            # 画叶子
            tobj.pd()
            tobj.right(90)
            n = cos(radians(tobj.heading() - 45)) / 4 + 0.5
            tobj.pencolor(n * 0.5 + 0.5, 0.4 + n * 0.4, 0.4 + n * 0.4)
            tobj.circle(2)
            tobj.left(90)
            tobj.pu()
            # 返回
            t = tobj.heading()
            tobj.setheading(an)
            tobj.backward(dis)
            tobj.setheading(t)
    tobj.pu()
    tobj.backward(l)  # 退回


# Turtle.h
# Turtle.speed()
tobj = Turtle()
wn=turtle.Screen()
wn.bgcolor(0.5, 0.5, 0.5)
tobj.ht()  # 隐藏turtle
tobj.speed(0)  # 速度 1-10渐进，0 最快
# tobj.tracer(0,0)
tobj.pu()  # 抬笔
tobj.backward(100)
tobj.left(90)  # 左转90度
tobj.pu()  # 抬笔
tobj.backward(300)  # 后退300
tree(tobj, 12, 100)  # 递归7层
done()
# ————————————————
# 版权声明：本文为CSDN博主「Soul fragments」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/weixin_43943977/article/details/102691392
