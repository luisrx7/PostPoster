from facebook.storie.storie import Storie
from facebook.post.photo_post import Photo_post

class Photo_storie(Storie):
    def __init__(self, media_path:str = ""):
        super().__init__(media_path=media_path)


    def _upload(self,api,page_id):
        photo_post = Photo_post(media_path=self.media_path, published=False)
        ret, post_id = photo_post.publish(api, page_id)
        if ret:
            self.uploaded_photo_id = post_id
            return True
        return False
        



    
    def publish(self,api,page_id):
        #Step 2. Publish a photo story
        # To publish your photo story to your Page, you will send a POST to the /page_id/photo_stories endpoint with the following parameters:

        # photo_id set to the ID for your uploaded photo
        # Example request
        # curl -X POST "https://graph.facebook.com/v19.0/page_id/photo_stories" \
        #       -d '{
        #            "photo_id": "photo_id"
        #          }'
        # On success, your app receives a JSON response that contains the following key-value pairs:

        # success set to true
        # post_id set to the ID for your story post
        # Example response
        # {
        # "success": true,
        # "post_id": 1234
        # }

        self._upload(api,page_id)
        if self.uploaded_photo_id is None:
            return False, None
        
        data = {"photo_id": self.uploaded_photo_id}

        ret = api.post_object(object_id=page_id,
                connection="photo_stories",
                data=data)
        
        if ret.get("post_id", None) is not None:
            print(f"Storie published with success id: {ret['post_id']}"  )
            return True , ret["post_id"]
        else:
            print("Storie failed to publish, error: ", ret)
            return False , None