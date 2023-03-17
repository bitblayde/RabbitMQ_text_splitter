import os
import sys
import pika

def load_data(filename):
    with open(filename, 'r') as f:
        text = f.read()
    os.remove(filename)
    return text


def my_print(pid, filename, length):
    print(f"Hi there my PID is {pid}. I have just open {filename} with {length} elements.")

def make_queue(text, filename, pid):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body = text,
            properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(f"Hi there my PID is {pid}. I have just sent {filename}.")

def main(filename):
    text = load_data(filename)
    make_queue(text, filename, os.getpid())

#if __name__ == "__main__":
#    main()