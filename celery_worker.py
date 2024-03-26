#!/usr/bin/env python
import pika, os, sys
from supabase import create_client
from celery import Celery
# from common.repository import repository

def initialize_supabase_client():
    url = "https://bgmgoumpqknyexxrjmji.supabase.co" #os.environ.get("SUPABASE_URL")
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJnbWdvdW1wcWtueWV4eHJqbWppIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMzc1MjQ1NywiZXhwIjoyMDE5MzI4NDU3fQ.yyyapRQwLl83Bv6H9fbr63oEfvdU-LhIidXCH1bJgOA" #os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)
    return client

# create a supabase client
client = initialize_supabase_client()
app = Celery('workflows')
app.config_from_object('celeryconfig')
app.autodiscover_tasks(packages=['tasks'], force=True)


def get_workflows():
    workflows = client.table("workflows").select("*").execute()
    return workflows.data

def parse_workflows(trigger, workflows):
    # for every workflow check against the trigger 
    # and run the task scheduler
    for workflow in workflows:
        if workflow["trigger"] == trigger:
            actions = workflow["actions"]
            print(actions)
            # try:
            #     repository[actions["first"]["action"]].apply_async(
            #         # args=[actions["first"]["details"]]
            #     )
            # except Exception as e:
            #     print(f"error {e}")
            
            # INFO: This is where the action runner function is invoked

def callback(ch, method, properties, body):
    trigger_name = body.decode("utf-8")
    # get the workflows
    workflows = get_workflows()
    # parse the workflows
    parse_workflows(workflows=workflows, trigger=trigger_name)


def runner():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='triggers', durable=True)
    channel.basic_consume(queue='triggers', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        runner()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)