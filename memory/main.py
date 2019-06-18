# 首先安装memory_profiler和psutil（psutil主要用于提高memory_profile的性能，建议安装）（可使用pip直接安装）
# pip install memory_profiler
# pip install psutil
#
# 具体运行方式为如下：（在待检测代码所在目录中打开命令行运行如下代码）
#
# mprof run test.py
# 结果会生成一个.dat文件，如”mprofile_20160716170529.dat”，里面记录了内存随时间的变化
# mprof plot
# 使用该命令以图片的形式展示出来