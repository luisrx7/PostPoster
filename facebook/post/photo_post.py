from facebook.post.post import Post

class Photo_post(Post):
    def __init__(self,message:str = "", media_path:str = "", scheduled_publish_time:int = 0, hashtags:list = [], link:str = ""):
        super().__init__(message=message, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags, link=link)
        pass

    def publish(self,api,page_id):

        assert self.message != "" or self.link != "" or self.hashtags != [] or self.media_path, "Post must have a message, a link , a hashtag or a media path"

        data={
            "url": self.media_path,
            }
        
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
                connection="photos",
                data=data)

        if ret.get("id", None) is not None:
            print(f"Photo post {'sheduled' if self.schedule_publish_time > 0 else ''  } with success id: {ret['id']}"  )
            return True , ret["id"]
        else:
            print("Photo post failed, error: ", ret)
            return False , None
        