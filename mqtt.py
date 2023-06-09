import time

import ujson
from machine import RTC
from umqtt.simple import MQTTClient

from config.global_variable import *

rtc = RTC()


def on_message(topic, msg):
    try:
        msg = ujson.loads(msg)
        if msg['source'] == 'server':
            if msg['operation'] == 'login':
                if msg['status'] == 'success':
                    if 'time' in msg:
                        (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(
                            int(msg['time'] - 946656000))
                        rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
                else:
                    raise Exception("Login failed!")

            if msg['operation'] == 'heart':
                if getvalue('working_status') == 'working':
                    working_config = getvalue('working_info')
                    send(ujson.dumps({
                        "source": "device",
                        "operation": "heart",
                        "status": "working",
                        "internal_temp": working_config[0],
                        "ambient_temp": working_config[1],
                        "ambient_hum": working_config[2],
                        "target_temp": working_config[3],
                        "remain_time": working_config[4],
                        "work_plan": getvalue('work_plan')
                    }))

                elif getvalue('working_status') is not None:
                    send(ujson.dumps({
                        "source": "device",
                        "operation": "heart",
                        "status": getvalue('working_status'),
                        "work_plan": getvalue('work_plan')
                    }))

                else:
                    send(ujson.dumps({
                        "source": "device",
                        "operation": "heart",
                        "status": "free",
                        "work_plan": getvalue('work_plan')
                    }))

            if msg['operation'] == 'set_work_config':
                work_time = msg['work_time']
                target_temp = msg['target_temp']
                set_var('work_config', [target_temp, work_time])

                if getvalue('page') != 'working':
                    set_var('page', 'working')
                else:
                    set_var('update_config', True)

                send(ujson.dumps({
                    "source": "device",
                    "operation": "ack",
                    "ack_seq": msg['seq']
                }))

            if msg['operation'] == 'add_work_plan':
                work_plan = {
                    "plan_id": msg['plan_id'],
                    "start_time": msg['start_time'],
                    "work_time": msg['work_time'],
                    "target_temp": msg['target_temp']
                }
                getvalue('work_plan').append(work_plan)

                send(ujson.dumps({
                    "source": "device",
                    "operation": "ack",
                    "ack_seq": msg['seq']
                }))

            if msg['operation'] == 'delete_work_plan':
                for plan in getvalue('work_plan'):
                    if plan['plan_id'] == msg['plan_id']:
                        getvalue('work_plan').remove(plan)
                        break

    except Exception as e:
        print(e)


def connect_to_server(server, port, client_id, username, password):
    client = MQTTClient(client_id, server, port, username, password)
    client.set_callback(on_message)
    client.connect()
    set_var('mqtt_client', client)
    set_var('topic', f'device/smartoven/{client_id}')
    client.subscribe(getvalue('topic'))
    client.publish('device/smartoven/login', ujson.dumps({
        "source": "device",
        "operation": "login",
        "connect_name": client_id,
        "require_time": (time.time() < 100)
    }), qos=0)


def receive():
    client = getvalue('mqtt_client')
    while True:
        if True:
            client.wait_msg()
        else:
            client.check_msg()
            time.sleep(1)


def send(message):
    client = getvalue('mqtt_client')
    client.publish(getvalue('topic'), message, qos=0)
