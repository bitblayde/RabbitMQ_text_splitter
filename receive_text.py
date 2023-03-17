import pika
import os, sys
import utils


args = sys.argv

if len(args) < 2:
    N_FILES = 0
    stop = False
else:
    N_FILES = int(args[1])
    stop = True

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

FILE_COUNTER = 1

def save_text(text, root):
    global FILE_COUNTER
    
    if not os.path.exists(root):
        os.makedirs(root)

    filename = f"text_{FILE_COUNTER}.txt"
    FILE_COUNTER += 1

    filename = os.path.join(root, filename)

    with open(filename, 'w') as f:
        f.write(text.decode())

def callback(ch, method, properties, body):
    print(FILE_COUNTER, N_FILES)
    if FILE_COUNTER >= N_FILES and stop:
        ch.stop_consuming()

    print(f" [x] Received: file number {FILE_COUNTER}")
    save_text(text = body, root="./received_text")
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
a = channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
