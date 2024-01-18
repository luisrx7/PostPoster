import unittest
import time
from facebook.facebook import Facebook
from creds import access_token, facebook_page_id, app_id, app_secret



posts = []

class TestFacebook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #this runs before all test case runs once
        cls.fb = Facebook(page_id=facebook_page_id,access_token=access_token, app_id = app_id, app_secret = app_secret)
        pass


    @classmethod
    def tearDownClass(cls):
        #this runs after all test case runs once
        print("tests are done, deleting posts created by tests")
        input("press enter to continue")
        #get all posts
        posts = cls.fb.get_feed_posts()
        for post in posts:
            print(f"deleting post [{post['id']}] created_at [{post['created_time']}] with message {post['message']}" )
            try:
                cls.fb.delete_post(post["id"])
            except Exception as e:
                print(e)
                print("failed to delete post: ", post["id"])
                pass
        pass

    def setUp(self):
        #this runs before every test case
        pass

    def tearDown(self):
        #this runs after every test case
        #check if post_id exists  
        if hasattr(self, "post_id"):
            posts.append(self.post_id)
        pass


    # def test_get_app_access_token(self):
    #     ret = self.fb.api.get_app_token(app_id=app_id, app_secret=app_secret)
    #     self.assertIsInstance(ret, dict)
    #     self.assertIn("access_token", ret)
    
    # def test_debug_token(self):
    #     ret = self.fb.api.debug_token(input_token=access_token)
    #     self.assertIsInstance(ret, dict)
    #     self.assertIn("data", ret)
    #     self.assertIn("app_id", ret["data"])
    #     self.assertIn("is_valid", ret["data"])
    #     self.assertIn("type", ret["data"])
    #     if ret["data"]["type"] == "USER":
    #         self.assertIn("user_id", ret["data"])
    #         self.assertIn("scopes", ret["data"])
    #         self.assertIn("expires_at", ret["data"])
    #         self.assertIn("data_access_expires_at", ret["data"])

    # def test_get_long_lived_token(self):
    #     ret_lltoken = self.fb.api.exchange_long_lived_user_access_token(access_token=access_token)
    #     self.assertIsInstance(ret_lltoken, dict)
    #     self.assertIn("access_token", ret_lltoken)
    #     self.assertIn("token_type", ret_lltoken)
    #     self.assertIn("expires_in", ret_lltoken)



    def test_delete_post(self):
        #this is a simple post without media
        ret , self.post_id = self.fb.create_post(message="Hello World")
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())
        #check if self.post_id contains only numbers
        ret = self.fb.delete_post(self.post_id)
        self.assertTrue(ret)

    def test_create_simple_post(self):
        #this is a simple post without media
        ret , self.post_id = self.fb.create_post(message="Hello World")
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())

    def test_create_simple_post_scheduled(self):
        #this is a simple post without media scheduled
        ret , self.post_id = self.fb.create_post(message="Hello World scheduled",scheduled_publish_time=int(time.time()+600))
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())


    def test_create_simple_post_scheduled_in_past(self):
        #this is a simple post without media scheduled in the past
        with self.assertRaises(AssertionError):
            ret , self.post_id = self.fb.create_post(message="Hello World scheduled to the past",scheduled_publish_time=int(time.time()-600))

    def test_create_simple_post_scheduled_in_future(self):
        #this is a simple post without media scheduled in the future more than 30 days
        with self.assertRaises(AssertionError):
            ret , self.post_id = self.fb.create_post(message="Hello World scheduled to more than 30 days",scheduled_publish_time=int(time.time()+60*24*60*60))

    def test_create_simple_post_scheduled_in_future_less_than_10_minutes(self):
        #this is a simple post without media scheduled in the future less than 10 minutes
        with self.assertRaises(AssertionError):
            ret , self.post_id = self.fb.create_post(message="Hello World scheduled to less than 10 minutes",scheduled_publish_time=int(time.time()+9*60))


    def test_create_simple_post_with_link(self):
        #this is a simple post without media
        ret , self.post_id = self.fb.create_post(message="Hello World with link",link="https://www.google.com")
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())



    def test_create_post_without_message(self):
        #this is a simple post without media
        with self.assertRaises(Exception):
            ret , self.post_id = self.fb.create_post()
        
    def test_create_post_with_photo(self):
        #this is a simple post with photo from url
        ret , self.post_id = self.fb.create_post(message="test",
                            media_path="https://pbs.twimg.com/profile_images/1359643195932557315/s9A68JRK_400x400.jpg",hashtags=["test"])
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())


    def test_create_post_with_photo_wrong_url(self):
        #this is a simple post with photo from url
        with self.assertRaises(Exception):
            ret , self.post_id = self.fb.create_post(message="test",
                            media_path="https://p557315/s9A68JRK_400x400.jp",hashtags=["test","test2"])


    def test_create_post_with_video_local(self):
        #this is a simple post with video from local
        ret , self.post_id = self.fb.create_post(message="test",
                            media_path=r"../assets/tests/Teste.mp4",hashtags=["test","test2"])
        self.assertTrue(ret)
        self.assertIsNotNone(self.post_id)
        # self.assertTrue(str(self.post_id).isdigit())

    def test_create_post_with_remote_video(self):
        #this is a simple post with video from web
        ret , self.post_id = self.fb.create_post(message="test video",
                            media_path="https://edisciplinas.usp.br/pluginfile.php/5196097/mod_resource/content/1/Teste.mp4",hashtags=["test","test2"])


    def test_get_all_feed_posts(self):
        #create a post first 
        ret , self.post_id = self.fb.create_post(message="test")
        ret = self.fb.get_feed_posts()
        
        #example_ret = [
        #     {
        #       "created_time": "2019-01-02T18:31:28+0000",
        #       "message": "This is my test post on my Page.",
        #       "id": "page_post_id"
        #     }
        #   ]

        self.assertIsInstance(ret, list)
        if len(ret) > 0:
            self.assertIsInstance(ret[0], dict)
            self.assertIn("created_time", ret[0])
            self.assertIn("message", ret[0])
            self.assertIn("id", ret[0])

    
    def test_delete_all_posts(self):
        #create a post
        ret , _ = self.fb.create_post(message="test")

        ret = self.fb.delete_all_posts()

        self.assertIsInstance(ret, dict)

        for key, value in ret.items():
            self.assertTrue(value)


    def test_create_post_with_video_local_wrong_path(self):
        #this is a simple post with video from local
        with self.assertRaises(AssertionError):
            ret , self.post_id = self.fb.create_post(message="test",
                                media_path=r"nonexisting.mp4",hashtags=["test","test2"]) 
            

if __name__ == '__main__':
    unittest.main()