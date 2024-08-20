from facebook.storie.storie import Storie
import json
import os
class Video_storie(Storie):
    def __init__(self, media_path: str = ""):
        super().__init__(media_path)

        self.video_id = None

        # Video stories
        # To publish a video story on a Facebook Page, you will initialize a video upload session with Meta servers, upload the video to Meta servers, then publish the video story.

        # Step 1: Initialize session
        # To initialize an upload session, send a POST request to the /page_id/video_stories endpoint, where page_id is the ID for your Facebook Page, with the upload_phase parameter set to start.

        # Example request
        # curl -X POST "https://graph.facebook.com/v19.0/page_id/video_stories" \
        #       -d '{
        #            "upload_phase":"start",
        #          }'
        # On success, your app receives a JSON response with the ID for the video and the Facebook URL where you will be uploading the video.

        # Example response
        # {
        #   "video_id": "video_id",
        #   "upload_url": "https://rupload.facebook.com/video-upload/v19.0/video_id",
        # }  


    def _initialize_video_upload_session(self,api,page_id):
        
        # Prepare the Facebook API endpoints
        upload_url = f"https://graph.facebook.com/{api.version}/{page_id}/video_stories"

        # Start the video upload process
        response = api._request(url=upload_url, verb="POST", args={"access_token": api.access_token, "upload_phase":"start"})

        response_data = json.loads(response.text)
        video_id = response_data["video_id"]
        upload_url = response_data["upload_url"]

        return video_id, upload_url
    

    def _upload(self,api,page_id):
        assert self.media_path is not None and self.media_path != "" and \
            (self.media_path.startswith("https") or self.media_path.endswith(".mp4")), "Media path must be a valid url or a valid file path"
        
        data = {}
        files = {}
        if self.media_path.startswith("http"):
            data["file_url"] = self.media_path
        
        elif self.media_path.endswith('.mp4') and os.path.exists(self.media_path):
            data["offset"] = "0"
            data["file_size"] = str(os.path.getsize(self.media_path))
            files["source"] = open(self.media_path, "rb")

        upload_url = self._initialize_video_upload_session(api,page_id)[1]
        response = api._request(url=upload_url, verb="POST",
                    args={"access_token": api.access_token,},
                    headers={"upload_phase": "start",
                                "offset": "0",
                                "file_size": str(os.path.getsize(self.media_path))}, 
                    files=files)
        
        # Close the file if it was opened
        if files.get("source", None) is not None:
            files["source"].close()
        
        response_data = json.loads(response.text)
        if response_data.get("success", False):
            print("Video uploaded with success")
            return True
        else:
            print("Video upload failed, error: ", response_data)
            return False

    
    def publish(self,api,page_id):
        # Step 3. Publish a video story
        # To publish your video story to your Page, you will send a POST to the /page_id/video_stories endpoint with the following parameters:

        # video_id set to the ID for your uploaded video
        # upload_phase set to finish
        # Example request
        # curl -X POST "https://graph.facebook.com/v19.0/page_id/video_stories" \
        #     -d '{
        #         "video_id": "video_id",
        #         "upload_phase": "finish"
        #         }'
        # On success, your app receives a JSON response that contains the following key-value pairs:

        # success set to true
        # post_id set to the ID for your story post
        # Example response
        # {
        # "success": true,
        # "post_id": 1234
        # }

        self._upload(api,page_id)
        if self.video_id is None:
            return False, None

        data = {"video_id": self.video_id, "upload_phase": "finish"}

        response = self.api._request(url=f"https://graph.facebook.com/{api.version}/{page_id}/video_stories",
                           verb="POST", args={"access_token": api.access_token}, post_args=data)        
        
        response_data = json.loads(response.text)
        if response_data.get("success", False):
            print(f"Storie published with success id: {response_data['post_id']}"  )
            return True , response_data["post_id"]
        else:
            print("Storie failed to publish, error: ", response_data)
            return False , None
