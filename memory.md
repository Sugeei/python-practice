使用memory_profiler监测python代码运行时内存消耗
2018年01月29日 19:54:39 clovermini 阅读数：6329
前几天一直在寻找能够输出python函数运行时最大内存消耗的方式，看了一堆的博客和知乎，也尝试了很多方法，最后选择使用memory_profiler中的mprof功能来进行测量的，它的原理是在代码运行过程中每0.1S统计一次内存，并生成统计图。

具体的使用方式如下：

首先安装memory_profiler和psutil（psutil主要用于提高memory_profile的性能，建议安装）（可使用pip直接安装）
pip install memory_profiler
pip install psutil

具体运行方式为如下：（在待检测代码所在目录中打开命令行运行如下代码）

mprof run test.py
结果会生成一个.dat文件，如”mprofile_20160716170529.dat”，里面记录了内存随时间的变化
mprof plot
使用该命令以图片的形式展示出来