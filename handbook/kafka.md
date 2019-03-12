Kafka设计解析 http://www.jasongj.com/kafka/high_throughput/

分布式消息系统， 发布、订阅消息系统
1. 消息持久化 常数复杂度访问性能
2. 高吞吐率，100K/s
3. 分布式消费， Partition 内部的顺序传输
4. 同时支持离线和实时
5. 支持水平扩展

Broker - 物理服务器
Topic - 逻辑类别
Partition - 物理上每个Topic包含一个或多个Partition

事务机制
Broker 为每个 topic, partition维护一个序号，且每次commit将其对应序号递增。
若序号不是增1， 则将消息丢弃。

Partition并行处理
Topic是逻辑概念， partition物理上对应一个文件夹。
Partition内部顺序读取

Kafka深度解析
http://www.jasongj.com/tags/Kafka/
http://www.jasongj.com/2015/01/02/Kafka%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90/

