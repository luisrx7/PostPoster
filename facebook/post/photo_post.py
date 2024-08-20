from facebook.post.post import Post
import os
class Photo_post(Post):
    def __init__(self,message:str = "", media_path:str = "", scheduled_publish_time:int = 0, hashtags:list = [], link:str = "",published:bool = True):
        super().__init__(message=message, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags, link=link, published=published)
        pass

    def publish(self,api,page_id):

        assert (self.message != "" or self.link != "" or self.hashtags != []) or self.media_path, "Post must have a message, a link , a hashtag or a media path"
        assert self.media_path.endswith('.jpeg') or self.media_path.endswith('.bmp') or self.media_path.endswith('.png') or self.media_path.endswith('.gif') or self.media_path.endswith('.tiff') or self.media_path.startswith('http'), "Media file must be a photo or an url"
        
        
        data={}
        files  = {}

        if self.media_path.startswith("http"):
            data["url"] = self.media_path
        else:
            if os.path.exists(self.media_path):
                files["source"] = open(self.media_path, "rb")
        
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
            data["published"] = "true" if self.published else "false"
            
        
        ret = api.post_object(object_id=page_id,
                connection="photos",
                data=data,
                files=files)
        
        #close the file if it was opened
        if data.get("source", None) is not None:
            data["source"].close()

        if ret.get("id", None) is not None:
            print(f"Photo post {'sheduled' if self.schedule_publish_time > 0 else ''  } with success id: {ret['id']}"  )
            return True , ret["id"]
        else:
            print("Photo post failed, error: ", ret)
            return False , None
        