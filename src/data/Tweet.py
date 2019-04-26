

class Tweet(object):
    def __init__(self, user, content, time_dif, is_source):
        self.user = user
        self.content = content
        self.time_dif = time_dif
        self.is_source = is_source

