import pika
import json
import pymysql.cursors
import requests
import os


database = pymysql.connect(host=os.getenv('MYSQL_HOST'),
                           user=os.getenv('MYSQL_USER'),
                           password=os.getenv('MYSQL_ROOT_PASSWORD'),
                           database=os.getenv('MYSQL_DATABASE'),
                           port=int(os.getenv('MYSQL_PORT')),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def make_insert(cn, data, table):
    with cn.cursor() as cursor:
        sql = f"""INSERT INTO {table} ({','.join(k for k in data.keys())})
                  VALUES ({','.join(f'"{v}"' for v in data.values())})"""
        cursor.execute(sql)
    cn.commit()
    with cn.cursor() as cursor:
        sql = f"""SELECT * FROM {table} WHERE name='{data.get('name')}'"""
        cursor.execute(sql)
        airport = cursor.fetchone()
    return airport


def make_update(cn, data, table):
    with cn.cursor() as cursor:
        _id = data.pop('id')
        sql = f"""UPDATE {table} SET {','.join(f'{k}="{v}"' for k,v in data.items())}
               WHERE  id='{_id}'"""
        cursor.execute(sql)
    cn.commit()
    with cn.cursor() as cursor:
        sql = f"""SELECT * FROM {table} WHERE id='{_id}'"""
        cursor.execute(sql)
        airport = cursor.fetchone()
    return airport


def make_delete(cn, data, table):
    with cn.cursor() as cursor:
        _id = data.pop('id')
        sql = f"""UPDATE {table} SET deleted=1 WHERE  id='{_id}'"""
        cursor.execute(sql)
    cn.commit()


print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(
             pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
channel = connection.channel()
channel.queue_declare(queue='cmd_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    cmd = body.decode('utf-8')
    data_dict = json.loads(cmd)

    if data_dict['cmd'] == 'create':
        airport = make_insert(database, data_dict['data'], 'airport')

    elif data_dict['cmd'] == 'update':
        airport = make_update(database, data_dict['data'], 'airport')

    elif data_dict['cmd'] == 'delete':
        make_delete(database, data_dict['data'], 'airport')

    ch.basic_ack(delivery_tag=method.delivery_tag)

    if airport:
        requests.post('http://api:5000/airports/webhook', json=airport)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='cmd_queue', on_message_callback=callback)
channel.start_consuming()
