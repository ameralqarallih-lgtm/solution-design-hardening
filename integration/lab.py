"""Fixed disposable-lab endpoints. Never point these fixtures at a real application."""
import os
import unittest

def require_lab():
    if os.environ.get('SDH_ISOLATED_LAB') != '1':
        raise unittest.SkipTest('Run inside the supplied isolated Compose lab')

def pg():
    require_lab()
    import psycopg
    return psycopg.connect(host='postgres', dbname='sdh_lab', user='sdh_lab', password='sdh_lab_only', connect_timeout=5, options='-c statement_timeout=8000 -c lock_timeout=5000')

def cache():
    require_lab()
    import redis
    return redis.Redis(host='redis', socket_connect_timeout=5, socket_timeout=5, decode_responses=True)

def broker():
    require_lab()
    import pika
    return pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('sdh_lab','sdh_lab_only'), socket_timeout=5, stack_timeout=10, blocked_connection_timeout=8, heartbeat=15))
