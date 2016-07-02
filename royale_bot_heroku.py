import praw
import time
import os

import unicodedata


class RoyaleBot:
    def __init__(self):
        self.r = praw.Reddit(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        self.subreddit_name = "test"
        self.ids_commented = []
        self.ending = "\n\nI am a bot. Question/problem? Ask my master: /u/iknowyourwoman\n\n[Source](https://github.com/sarbajitsaha/RoyaleBot)"
        with open("ids","r+") as f:
            data = f.read()
            data = data.split("\n")
            for d in data:
                self.ids_commented.append(d.strip())

    def load_credentials(self):
        self.r.login(os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD'], disable_warning=True) #logged in

    def send_royale_stats(self):
        subreddit = self.r.get_subreddit(self.subreddit_name)
        cmts = subreddit.get_comments()
        cmts = praw.helpers.flatten_tree(cmts)
        for c in cmts:
            id = c.id
            id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
            body = c.body
            if(self.check_condition(c,body)):
                self.add_comment(c, id, self.cmt, body)

    def check_condition(self,c,body):
        words = body.split()
        for i in range(len(words)):
            words[i] = words[i].lower()
        if "royalebot!" in words:
            with open("cmts", "a") as f:
                f.write(body + "\n")
            #files = os.listdir("data")
            if(len(words)!=2):
                return False
            name = words[1]
            print (name)
            try:
                f = open("data/"+name)
                self.cmt = f.read()
            except IOError:
                self.cmt = "Sorry couldn't find this troop. Remember not to put spaces in between and only use two words e.g. write Royale Giant as RoyaleGiant\n\nTo call the bot comment as rbot! royalegiant"
            return True
        else:
            return False

    def add_comment(self, c, id, cmt, body):
        print (self.ids_commented)
        try:
            if id not in self.ids_commented:
                print ("Id is : " + id)
                print ("Making comment to -> {0}".format(body))
                c.reply(cmt+self.ending)
                self.add_ids_to_file(id)
                self.ids_commented.append(id)
            else:
                print ("Id present {0}".format(id))
        except praw.errors.RateLimitExceeded as error:
            print("Ratelimit: {0} seconds".format(error.sleep_time))
            time.sleep(error.sleep_time)

    def add_ids_to_file(self,id):
        with open("ids","a") as f:
            f.write(id.strip()+"\n")


if __name__=="__main__":
    rbot = RoyaleBot()
    rbot.load_credentials()
    while True:
        rbot.send_royale_stats()
        print ("waiting for a minute before checking")
        time.sleep(60)

