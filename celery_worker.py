import pika, os, sys
from supabase import create_client
from celery import Celery
from dotenv import load_dotenv
from action_runner import action_runner

# load the environment variables
load_dotenv()

def initialize_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)
    return client

# create a supabase client
client = initialize_supabase_client()
celery_app = Celery('workflows', broker="amqp://localhost")
celery_app.autodiscover_tasks(
    packages=["action_runner"],
    related_name="action",
    force=True
)


def get_workflows():
    workflows = client.table("workflows").select("*").execute()
    return workflows.data

def parse_workflows(trigger, workflows):
    # for every workflow check against the trigger 
    # and run the task scheduler
    for workflow in workflows:
        if workflow["trigger"] == trigger:
            actions_map = workflow["actions"]
            print(actions_map)
            try:
                action_runner.apply_async(
                    args=[
                        actions_map,
                        "first"
                    ]
                )
            except Exception as e:
                print(f"ERROR: something wrong with parsing {e}")

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