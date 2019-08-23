# planA
34

set:

redisConn.set("key", df.to_msgpack(compress='zlib'))
get:

pd.read_msgpack(redisConn.get("key"))


planB
zlib together like this, assuming a dataframe df and a local instance of redis:

import pickle
import redis
import zlib

EXPIRATION_SECONDS = 600

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set
r.setex("key", EXPIRATION_SECONDS, zlib.compress( pickle.dumps(df)))

# Get
rehydrated_df = pickle.loads(zlib.decompress(r.get("key")))
There isn't anything anything dataframe specific about this.

Caveats

the other answer using msgpack is better -- use it if it works for you
pickling can be dangerous -- your Redis server needs to be secure or you're asking for trouble
