from flask import Flask, jsonify
import praw

reddit = praw.Reddit(client_id="stzfa8KjwNZpzg",
                     client_secret="lBPzlZ5hkVrwpLKEnBUhcvSBpyM",
                     user_agent="app v1 (by u/vesperenth657)",)

subreddit = reddit.subreddit('writingprompts')
titlesList = []
postsList = []
mainComments = []

for post in subreddit.hot(limit = 5):
    # limit is always n-2, since first two posts are pinned
    if '[WP]' in post.title:
        postsList.append(post.id)
        titlesList.append(post.title)

for id in postsList:
    post = reddit.submission(id=id)
    commentList = []
    for comment in post.comments:
        if 'Welcome to the Prompt!' not in comment.body:
            topComments = comment.body
            commentList.append(topComments)

    mainComments.append(commentList)

master_list = zip(titlesList, mainComments)
super_list = [list(a) for a in master_list]


app = Flask(__name__)
app.config["DEBUG"] = True

json = []

for i in super_list:
    a = i[0]
    b = [item for item in i[1]]
    c = [val for sublist in b for val in sublist]

    entry = {
     'title': ''.join(a),
     'comments': b,
     }
    json.append(entry)


@app.route('/')
def hello_world():
    return jsonify(json)


if __name__ == '__main__':
    app.run()
