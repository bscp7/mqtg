import os
import time

import click
import pymqi
from dotenv import load_dotenv

load_dotenv()


@click.group()
def cli():
    pass


@click.command()
@click.option('--count', default=1, help='Number of messages to publish')
@click.option('--delay', default=0.0, type=float, help='Wait between publishing message')
def put(count, delay):
    """Publish message(s) to a queue"""
    conn_info = '%s(%s)' % (os.getenv("HOST"), os.getenv("PORT"))
    qmgr = pymqi.connect(os.getenv("QUEUE_MANAGER"),
                         os.getenv("CHANNEL"),
                         conn_info,
                         os.getenv("USER"),
                         os.getenv("PASSWORD"))
    queue = pymqi.Queue(qmgr, os.getenv("QUEUE"))
    click.echo(f"Sending {count} message(s) with a delay of {delay} seconds between each message.")

    for _ in range(count):
        queue.put(f"Hello {count}!")
        click.echo("!", nl=False)
        time.sleep(delay)
    queue.close()
    qmgr.disconnect()
    click.echo(f"\nSent: {count}")


@click.command()
@click.option('--delay', default=0.0, type=float, help='Wait between receiving next message')
def get(delay):
    """Receive message(s) from a queue"""
    conn_info = '%s(%s)' % (os.getenv("HOST"), os.getenv("PORT"))
    qmgr = pymqi.connect(os.getenv("QUEUE_MANAGER"),
                         os.getenv("CHANNEL"),
                         conn_info,
                         os.getenv("USER"),
                         os.getenv("PASSWORD"))
    queue = pymqi.Queue(qmgr, os.getenv("QUEUE"))

    count = 0
    try:
        while True:
            _ = queue.get(None)
            count += 1
            click.echo("!", nl=False)
            time.sleep(delay)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            if count == 0:
                click.echo("No messages available.")
            else:
                click.echo("\nAll messages received.")
        else:
            raise e
    click.echo(f"Received: {count}")
    queue.close()
    qmgr.disconnect()


cli.add_command(put)
cli.add_command(get)

if __name__ == '__main__':
    cli()
