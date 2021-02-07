import redis

r = redis.Redis()
r.mset({'nome': 'Francesco', 'nome2': 'Come Stai'})
