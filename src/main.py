import os
import time

import schedule
from telebot import TeleBot
from redis import Redis

from service.utils import get_send_rewards_func


def main():
    bot_instance = TeleBot(os.getenv('TG_TOKEN'))
    redis_instance = Redis(os.getenv('REDIS-HOST', 'redis'))
    schedule.every(1).hours.do(get_send_rewards_func(bot_instance, redis_instance))
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
