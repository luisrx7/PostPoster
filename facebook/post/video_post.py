from importlib.metadata import files
from facebook import post
from facebook.post.post import Post
import json
import os
class Video_post(Post):
    def __init__(self,message:str = "", media_path:str = "", scheduled_publish_time:int = 0, hashtags:list = [], link:str = "",published:bool = True):
        super().__init__(message=message, media_path=media_path, scheduled_publish_time=scheduled_publish_time, hashtags=hashtags, link=link, published=published)


    def publish(self,api,page_id):
        
        assert self.message != "" and  self.media_path, "Post must have a message, a link , a hashtag or a media path"
        assert self.media_path.endswith('.mp4') or self.media_path.startswith("http"), "Video post must be an mp4 file or an url to a video file"


        #limitations of video post 1GB max size, 20 minutes max length
        #https://developers.facebook.com/docs/video-api/guides/publishing#non-resumable-upload

        # Sample Local File Request
        # curl -X POST \
        # "https://graph-video.facebook.com/v18.0/1755847768034402/videos" \
        # -F "access_token=EAADd..." \
        # -F "source=@/Users/...incredible.mov"
        # Sample Hosted File Request
        # curl -X POST \
        # "https://graph-video.facebook.com/v18.0/1755847768034402/videos" \
        # -F "access_token=EAADd..." \
        # -F "file_url=https://socialsizz.../incredible.mov"
        # Upon success, the API will respond with the ID of the published Video.

        # Sample Response
        # {
        # "id":"287788272232962"  //ID of the published Video
        # }

        #         -F, --form <name=content>

        # (HTTP SMTP IMAP) For HTTP protocol family, this lets curl emulate a filled-in form in which a user has pressed the submit button. This causes curl to POST data using the Content-Type multipart/form-data according to RFC 2388.

        # For SMTP and IMAP protocols, this is the means to compose a multipart mail message to transmit.

        # This enables uploading of binary files etc. To force the 'content' part to be a file, prefix the file name with an @ sign. To just get the content part from a file, prefix the file name with the symbol <. The difference between @ and < is then that @ makes a file get attached in the post as a file upload, while the < makes a text field and just get the contents for that text field from a file.

        # Tell curl to read content from stdin instead of a file by using - as filename. This goes for both @ and < constructs. When stdin is used, the contents is buffered in memory first by curl to determine its size and allow a possible resend. Defining a part's data from a named non-regular file (such as a named pipe or similar) is not subject to buffering and is instead read at transmission time; since the full size is unknown before the transfer starts, such data is sent as chunks by HTTP and rejected by IMAP.

        # Example: send an image to an HTTP server, where 'profile' is the name of the form-field to which the file portrait.jpg is the input:

        #  curl -F profile=@portrait.jpg https://example.com/upload.cgi

        args = {"access_token": api.access_token}

        post_args = {}
        files   = {}

        if self.media_path.startswith("http"):
            post_args["file_url"] = self.media_path
        elif self.media_path.endswith('.mp4'):
            #check if file exists 
            assert os.path.exists(self.media_path), "Video file does not exist"

            files["source"] = open(self.media_path, "rb")

        if len(self.hashtags) > 0:
            for hashtag in self.hashtags:
                self.message += " #" + hashtag

        if self.message != "":
            args["description"] = self.message

        if self.link != "":
            post_args["link"] = self.link
        

        if self.schedule_publish_time > 0 :
            post_args["scheduled_publish_time"] = str(self.schedule_publish_time)
            post_args["published"] = "false"
        else:
            post_args["published"] = "true"
        try:
            ret = api._request(url=f"https://graph-video.facebook.com/v18.0/{page_id}/videos",
                                verb="POST",
                                args=args,
                                files=files,
                                post_args=post_args
                                )
            
            #close the file if it was opened
            if files.get("source", None) is not None:
                files["source"].close()

            response_data = json.loads(ret.text)
            print(response_data)

        

            if response_data.get("id", None) is not None:
                print("Video post success with id: ", response_data["id"] )

                # da = api._request(url=f"https://graph.facebook.com/v18.0/{response_data['id']}",
                #                 verb="GET",
                #                 args={"access_token": api.access_token,"fields": "id,description,created_time,from,post_id"},
                #                 )
                # print(json.loads(da.text))


                return True , response_data["id"]
            else:   
                print("Video post failed, error: ", response_data)
                return False , None

        except Exception as e:
            print(e)
        
            return False , None

        # video_id, upload_url = self._initialize_video_upload_session(api,page_id)
        # print(f" Video id: {video_id} \n Upload url: {upload_url}")

        # ret_upload = self._upload_video_file(api, page_id, upload_url, self.media_path)
        # print(f"Video upload status: {ret_upload}")
        # pass

        
    




    # def _initialize_video_upload_session(self,api,page_id):
        
    #     # Prepare the Facebook API endpoints
    #     upload_url = f"https://graph.facebook.com/{api.version}/{page_id}/video_stories"

    #     # Start the video upload process
    #     response = api._request(url=upload_url, verb="POST", args={"access_token": api.access_token, "upload_phase":"start"})

    #     response_data = json.loads(response.text)
    #     video_id = response_data["video_id"]
    #     upload_url = response_data["upload_url"]

    #     return video_id, upload_url
    

    # def _upload_video_file(self,api, page_id, upload_url,media_path):

    #     headers={"Content-Type": "application/json"}
    #     raw_file = None
    #     if media_path.startswith("http"):
    #         headers["file_url"] = media_path
    #     elif media_path is not None and media_path.endswith('.mp4') :
            
    #         with open(media_path, "rb") as f:
    #             raw_file = f.read()
    #             f.close()


    #         headers["offset"] = "0"
    #         headers["file_size"] = str(os.path.getsize(media_path))


    #     response = api._request(url=upload_url, args={"access_token": api.access_token, "upload_phase":"start"}, post_args = raw_file)
    #     response_data = json.loads(response.text)
    #     print(response_data)
    #     return True if response_data["success"] else False

