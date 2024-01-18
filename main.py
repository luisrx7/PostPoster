
from facebook.facebook import Facebook
from creds import access_token, facebook_page_id


#load schedule yaml files



# from sheduler import SocialMediaManager


# SocialMediaManager('fb_access_token', 'ig_access_token').run()




fb = Facebook(access_token, facebook_page_id)

fb.create_post(message="Hello World")
                # media_path="https://pbs.twimg.com/profile_images/1359643195932557315/s9A68JRK_400x400.jpg",
                # scheduled_publish_time=0,
# )