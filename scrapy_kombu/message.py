import logging

from amqp import UnexpectedFrame
from kombu import Connection
from kombu.connection import ChannelPool
from kombu.transport.pyamqp import Channel

from tenacity import retry, stop_after_attempt


class KombuConnection:
    def __init__(self, parameters):
        self.logger = logging.getLogger()
        self.con: Connection = None
        self.channel_pool: ChannelPool
        self._parameters = parameters
        self._create_connection()
        self.channel = self.acquire()

    @retry(stop=stop_after_attempt(5))
    def _create_connection(self):  # noqa
        self.con = Connection(**self._parameters)
        self.channel_pool = ChannelPool(self.con)
        self.channel: Channel = self.channel_pool.acquire()

    def _acquire(self, **kwargs):
        if not self.con.connected:
            self.con.connect()
        return self.channel_pool.acquire(**kwargs)

    def acquire(self, **kwargs):
        return self.wrap(self._acquire, **kwargs)

    def _ack(self, delivery_tag: int):
        self.channel.basic_ack(delivery_tag)

    def ack(self, delivery_tag: int):
        return self.wrap(self._ack, delivery_tag)

    def _reject(self, delivery_tag: int):
        self.channel.basic_reject(delivery_tag, requeue=True)

    def reject(self, delivery_tag: int):
        return self.wrap(self._reject, delivery_tag)

    def _get(self, queue, no_ack=True):
        return self.channel.basic_get(queue, no_ack)

    def get(self, queue, no_ack=False):
        return self.wrap(self._get, queue, no_ack)

    def wrap(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BrokenPipeError:
            self.channel = self.channel_pool.acquire()
        except (ConnectionResetError, TimeoutError):
            self.reset()
        except UnexpectedFrame as e:
            self._create_connection()
            self.logger.warning(f'UnexpectedFrame')

    def reset(self):
        self.logger.info(f'reconnecting...')
        if self.con:
            self.con.release()
        self._create_connection()

    def close(self):
        self.con.release()
