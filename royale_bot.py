import os

import praw
import time
import unicodedata

import dropbox.dropbox

class RoyaleBot:
    def __init__(self,heroku=False):
        self.heroku = heroku
        self.r = praw.Reddit(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        self.subreddit_name1 = "clashroyale"
        self.subreddit_name2 = "royalebot"
        self.ids_commented = []
        self.cmts = []
        if(heroku):
            self.access_token = os.environ['DROPBOX_ACCESS_TOKEN']
        else:
            f = open("credentials")
            data = f.read().split("\n")
            f.close()
            self.access_token = data[2]
        self.client = dropbox.client.DropboxClient(self.access_token)
        self.ending = "\n\nI am a bot. Question/problem? Ask my master: /u/iknowyourwoman\n\n[Source](https://github.com/sarbajitsaha/RoyaleBot)"

    def load_credentials(self):
        if self.heroku:
            self.r.login(os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD'], disable_warning=True)  # logged in
        else:
            f = open("credentials")
            cred = []
            for line in f:
                cred.append(line.strip())
            self.r.login(cred[0], cred[1], disable_warning=True) #logged in
            f.close()

    def send_royale_stats(self):
        subreddit = self.r.get_subreddit(self.subreddit_name1 + '+' + self.subreddit_name2)
        cmts = subreddit.get_comments()
        cmts = praw.helpers.flatten_tree(cmts)
        for c in cmts:
            id = c.id
            body = c.body
            if(self.check_condition(body,id)):
                self.add_comment(c, id, self.cmt, body)

    def check_condition(self,body,id):
        words = body.split()
        for i in range(len(words)):
            words[i] = words[i].lower().strip()
        if ("royalebot!" in words) or ("rbot!" in words):
            if id not in self.ids_commented:
                self.cmts.append(body)
            if(len(words)==1):
                self.cmt = "To call the bot comment as royalebot! {troop name} or rbot! {troop name}"
            elif(len(words)==2):
                name = words[1]
            else:
                name = words[1] + words[2]
            print (name)
            try:
                f = open("data/"+name)
                self.cmt = f.read()
                f.close()
            except IOError:
                self.cmt = "Sorry couldn't find this troop. \n\nTo call the bot comment as royalebot! {troop name} or rbot! {troop name}"
            return True
        else:
            return False

    def add_comment(self, c, id, cmt, body):
        try:
            if id not in self.ids_commented:
                print ("Id is : " + id)
                print ("Making comment to -> {0}".format(body))
                c.reply(cmt+self.ending)
                self.ids_commented.append(id)
            else:
                print ("Id present {0}".format(id))
        except praw.errors.RateLimitExceeded as error:
            print("Ratelimit: {0} seconds".format(error.sleep_time))
            time.sleep(error.sleep_time)

    def get_ids_cmts_dropbox(self):
        self.ids_commented = []
        self.cmts = []
        f, metadata = self.client.get_file_and_metadata('ids.txt')
        data = f.read().decode('UTF-8').split("\n")
        for d in data:
            self.ids_commented.append(d.strip())
        print ("Added ids -> {0}".format(len(self.ids_commented)))
        f, metadata = self.client.get_file_and_metadata('cmts.txt')
        data = f.read().decode('UTF-8').split("\n")
        for d in data:
            self.cmts.append(d.strip())
        print ("Added cmts -> {0}".format(len(self.cmts)))

    def add_ids_cmts_dropbox(self):
        str = ""
        for id in self.ids_commented:
            str+=(id+"\n")
        response = self.client.put_file('ids.txt', str, overwrite=True)
        print ('Uploaded ids: ', response)
        str = ""
        for cmt in self.cmts:
            str += (cmt + "\n")
        response = self.client.put_file('cmts.txt', str, overwrite=True)
        print('Uploaded cmts: ', response)


if __name__=="__main__":
    try:
        heroku = os.environ['HEROKU']
    except:
        print("Not heroku")
        heroku = False
    rbot = RoyaleBot(heroku=heroku)
    rbot.load_credentials()
    rbot.get_ids_cmts_dropbox()
    i = 0
    while True:
        if (heroku==False):
            os.system("cls")
        rbot.send_royale_stats()
        print ("Waiting for a minute before checking")
        i+=1
        if(i%2==0):
            rbot.add_ids_cmts_dropbox()
            rbot.get_ids_cmts_dropbox()
        time.sleep(60)



