

# SocialPlatform class is the base class for all social media platforms
# It is responsible for handling the API calls for all social media platforms
# It is also responsible for handling the scheduling of posts
# It is also responsible for handling the uploading of posts



class SocialPlatform:
    def __init__(self, page_id,access_token= None, app_id = None, app_secret = None):
        self.access_token = access_token
        self.page_id = page_id
        self.app_id = app_id
        self.app_secret = app_secret

    