Tested on **Ubuntu**

To start this project use ***run_cluster.sh***

To check is everything is up and running use `curl http://localhost:9200/de-enriched-data/_count`
to check if data is transmitted to elasticsearch.

Or you can run console consumer with `kafka-console-consumer.sh --bootstrap-server kafka-1:9092 --topic
[topic_name (de-source-data, de-enriched-data)] [--partition <int>]`