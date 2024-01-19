
#a post is a generic post that can be either a photo or a video post on a feed page

class Post:
    def __init__(self,message:str = "", media_path:str = "", scheduled_publish_time:int = 0, hashtags:list = [], link:str = "",published:bool = True):
        self.message = message
        self.hashtags = hashtags
        self.link = link
        self.media_path = media_path
        self.schedule_publish_time = scheduled_publish_time
        self.hashtags = hashtags
        self.published = published



    def publish(self,api,page_id):
        assert self.message != "" or self.link != "" or self.hashtags != [], "Post must have a message, a link or a hashtag"

        data={}
        

        if len(self.hashtags) > 0:
            for hashtag in self.hashtags:
                self.message += " #" + hashtag

        if self.message != "":
            data["message"] = self.message

        if self.link != "":
            data["link"] = self.link
        
        if self.schedule_publish_time > 0 :
            data["scheduled_publish_time"] = str(self.schedule_publish_time)
            data["published"] = "false"
        else:
            data["published"] = "true"



        ret = api.post_object(object_id=page_id,
                connection="feed",
                data=data)

        if ret["id"]:
            print("Post published successfully with id: ", ret["id"] )
            return True , ret["id"]
        else:
            print("Post failed, error: ", ret)
            return False , None
        
