import praw
import csv
import json
import time

source = 'redditposts.csv'

reddit = praw.Reddit(user_agent= '',
    client_id='',
    client_secret="",
    username='',
    password='')


#Set up Subreddit
subreddit = reddit.subreddit('politics')
submissions = subreddit.hot(limit=1) #limit is # of posts to pull from, could do subreddit.new, rising... etc

##could also use submission ID:
##submissions = []
##oneSub = reddit.submission(id='8ggcp8')
            
#get data and output into csv format
def getRecent (filename):
    #csv file setup
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["Author", "Submission Link", "Comment Id", "Parent Id", "Timestamp", "Comment Body"])
        #Loop through submissions for comments
        for instance in submissions:
            instance.comments.replace_more(limit=0)
            comments = instance.comments.list()
            #Loop through each comment of chosen submission
            for item in comments:
                body = item.body
                author = item.author
                timestamp = item.created_utc
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) #change to local time
                id = item.fullname
                parentId = item.parent().fullname
                submissionLink = instance.fullname
                #write to csv file with header
                writer.writerow([author, submissionLink , id, parentId, timestamp, body])

#MAIN
getRecent(source)
print("done")

#resources
#http://praw.readthedocs.io/en/latest/getting_started/quick_start.html#obtain-submission-instances-from-a-subreddit
#http://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html?highlight=created%20utc
