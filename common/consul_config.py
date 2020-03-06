import consul
import traceback
import logging

logger = logging.getLogger("default")

def get_key_value(host,port,key):
    c = consul.Consul(host=host,port=port,scheme="http")
    return str(c.kv.get(key)[1]["Value"],encoding="utf-8")

def put_key_value(host,port,key,value):
    c = consul.Consul(host=host,port=port,scheme="http")
    try:
        c.kv.put(key,value)
    except Exception:
        logger.info(traceback.format_exc())

def list_key(host,port):
    c = consul.Consul(host=host,port=port,scheme="http")
    key_list = [key["Key"] for key in c.kv.get("config",recurse=True)[1]]
    return key_list