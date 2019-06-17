import tweepy


def create_api():
    consumer_key = '9TvVKS8HRroMN4wQtBdzNA'
    consumer_secret = 'BrmSzXi4sGzDiRdj7kbPHMRLQNMkbpHeDqtLhWPhU'
    access_token = '1287392767-m7gcpy3wkpNpvMpywC9wwBTzIivWVXvLabhZMlA'
    access_token_secret = 'RHNCzFoLOpUHZhLQu7mDkJGsgtA3xtpKm35596ZfuRY'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api

def get_tweet_content(api, tweet_ids):
    tweet_ids = list(tweet_ids)
    nb_tweets = len(tweet_ids)
    result = []

    for i in range(int(nb_tweets / 100) + 1):
        min = i * 100
        max = (i + 1) * 100
        max = max if max < nb_tweets else nb_tweets

        if min < max:
            status_list = api.statuses_lookup(tweet_ids[min: max], tweet_mode='extended')
            for status in status_list:
                id = status.id_str
                text = status.full_text

                result.append((id, text))

    return result