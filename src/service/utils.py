import os
import requests

from telebot import TeleBot
from redis import Redis


def get_send_rewards_func(bot_instance: TeleBot, redis_instance: Redis):
    def send_rewards():
        rewards_link = os.getenv('REWARDS-LINK', 'https://api.coinmarketcap.com/shop/v3/product/list')
        chat_id = os.getenv('TG_CHAT_ID')
        rewards = get_rewards(rewards_link)
        message = generate_message_for_tg(rewards, redis_instance)
        bot_instance.send_message(chat_id, message)

    return send_rewards


def get_rewards(rewards_link):
    rewards_data = []
    json_request = get_default_json_request()
    while rewards := requests.post(rewards_link, json=json_request).json()['data'].get('list'):
        rewards_data.extend(rewards)
        json_request['currentPage'] += 1
    return rewards_data


def get_default_json_request():
    return {
        'currentPage': 1,
        'pageSize': 99999
    }


def get_new_rewards(rewards, redis_instance):
    all_rewards = set(reward.decode() for reward in redis_instance.smembers('unique_rewards'))
    return rewards - all_rewards


def generate_message_for_tg(rewards, redis_instance):
    rewards = set(reward['productId'] for reward in rewards)
    new_rewards = get_new_rewards(rewards, redis_instance)
    for reward in rewards:
        redis_instance.sadd('unique_rewards',  reward)
    if new_rewards:
        message = 'New Reward on CoinMarketCap'
    else:
        message = 'No new reward in CoinMarketCap'
    return message
