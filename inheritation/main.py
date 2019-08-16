# 基数中变量a没有初始化，在继承类中赋值， 基数中函数funca调用了变量a, 函数funca在外部被调用，是否能正确输出
# 继承类中重写了funca, 外部调用时调用的是基类的还继承类中的

from inheritation.market_value import MarketValue
from inheritation.mobility import Mobility

MarketValue().write()
Mobility().write()

