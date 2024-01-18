from social_platform import SocialPlatform
from pyfacebook import GraphAPI
from facebook.post.photo_post import Photo_post
from facebook.post.video_post import Video_post
from facebook.post.post import Post

import os
import time
#class Facebook is the class that will handle all the Facebook API calls
#It is a subclass of SocialPlatform

class Facebook(SocialPlatform):

    def __init__(self, page_id,access_token= None, app_id = None, app_secret = None):
        super().__init__(page_id,access_token, app_id, app_secret)

        self.api = GraphAPI(version="v18.0", app_secret=app_secret, app_id=app_id,access_token=access_token)

    
    def create_post(self,message:str = "", media_path:str = "", scheduled_publish_time:int = 0, hashtags:list = [], link:str = ""):

        # detect if the post is a photo or a video post
        # if it is a photo post, then create a photo post object
        # if it is a video post, then create a video post object
        # if it is neither, then create a generic post object (text)

        if scheduled_publish_time > 0:
            assert scheduled_publish_time > 0, "Scheduled publish time must be in the future"
            assert scheduled_publish_time < int(time.time() + 30*24*60*60), "Scheduled publish time must be less than 30 days from now"
            assert scheduled_publish_time >= int(time.time() + 10*60), "Scheduled publish time must be at least 10 minutes from now"


        if media_path is not None and media_path != "":
            if media_path.endswith('.mp4'):
                post = Video_post(message=message, link=link, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags)
            else:
                post = Photo_post(message=message, link=link, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags)

        else:
            post = Post(message=message, link=link, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags)

        
        ret, post_id = post.publish(self.api, self.page_id)

        return ret, post_id
        

    def delete_post(self, post_id):
        ret = self.api.delete_object(object_id=post_id,connection="feed")
        if ret.get("success", False):
            print(f"Post [{post_id}] deleted successfully")
            return True
        else:
            print(f"Post [{post_id}] failed to delete, error: ", ret)
            return False
        

    def get_feed_posts(self):
        #Get Posts
        # To get a list of Page posts, send a GET request to the /page_id/feed endpoint.

        # Example Request
        # Formatted for readability. Replace bold, italics values, such as page_id, with your values.
        # curl -i -X GET "https://graph.facebook.com/v18.0/page_id/feed"
        # On success, your app receives the following JSON response with an array of objects that include the post ID, the time the post was created, and the content for the post, for each post on your Page:

        # {
        # "data": [
        #     {
        #     "created_time": "2019-01-02T18:31:28+0000",
        #     "message": "This is my test post on my Page.",
        #     "id": "page_post_id"
        #     }
        # ],
        # ...
        # }

        ret = self.api.get_object(object_id=self.page_id, fields="feed")
        return ret["feed"]["data"]
    

    def delete_all_posts(self):
        posts = self.get_feed_posts()
        ret_val = {}
        #return a dict of all the posts ids deleted and if they were successful or not
        for post in posts:
            ret = self.delete_post(post["id"])
            if ret is True:
                ret_val[post["id"]] = True
            else:
                ret_val[post["id"]] = False
        
        return ret_val
    

        