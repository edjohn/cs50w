from django.test import TestCase
from .models import User, Post, Like, FollowerRelation;
from django.utils import timezone
from selenium import webdriver
from django.test import LiveServerTestCase
from django.urls import reverse

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username='testuser3')

    def test_user_count(self):
        self.assertEqual(User.objects.all().count(), 3)
        self.user2.delete()
        self.assertEqual(User.objects.all().count(), 2)
    
    def test_user_name(self):
        self.assertEqual(self.user1.username,'testuser1')
    
class FollowerRelationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username='testuser3')

        self.user1FollowsUser2 = FollowerRelation.objects.create(user=self.user1, followed_user=self.user2)
        self.user1FollowsUser3 = FollowerRelation.objects.create(user=self.user1, followed_user=self.user3)
        self.user3FollowsUser2 = FollowerRelation.objects.create(user=self.user3, followed_user=self.user2)
        self.user2FollowsUser2 = FollowerRelation.objects.create(user=self.user2, followed_user=self.user2)

    def test_follower_count(self):
        self.assertEqual(self.user1.followers.count(), 0)
        self.assertEqual(self.user2.followers.count(), 3)
        self.user1.delete()
        self.assertEqual(self.user2.followers.count(), 2)

    
    def test_followed_user_count(self):
        self.assertEqual(self.user1.followed_users.count(), 2)
        self.assertEqual(self.user2.followed_users.count(), 1)
        self.user2.delete()
        self.assertEqual(self.user1.followed_users.count(), 1)

    def test_follower_relation(self):
        self.assertEqual(self.user1FollowsUser2.followed_user, self.user2)
        self.assertEqual(self.user1FollowsUser3.followed_user, self.user3)

class PostTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username='testuser3')

        self.user1Post = Post.objects.create(user=self.user1, content="First Post", creation_date=timezone.now())
        self.user2Post = Post.objects.create(user=self.user2, content="First Post", creation_date=timezone.now())
        self.user3Post = Post.objects.create(user=self.user3, content="First Post", creation_date=timezone.now())
        self.user1SecondPost = Post.objects.create(user=self.user1, content="Second Post", creation_date=timezone.now())

        self.user1LikedUser1Post = Like.objects.create(user=self.user1, post=self.user1Post)
        self.user1LikedUser1SecondPost = Like.objects.create(user=self.user1, post=self.user1SecondPost)
        self.user1LikedUser2Post = Like.objects.create(user=self.user1, post=self.user2Post)
        self.user2LikedUser1Post = Like.objects.create(user=self.user2, post=self.user1Post)

    def test_post_likes(self):
        self.assertEqual(self.user2Post.post_likes.count(), 1)
        self.assertEqual(self.user1Post.post_likes.count(), 2)
        self.assertEqual(self.user3Post.post_likes.count(), 0)
        self.user1LikedUser1Post.delete()
        self.assertEqual(self.user1Post.post_likes.count(), 1)

    def test_user_likes(self):
        self.assertEqual(self.user1.user_likes.count(), 3)
        self.assertEqual(self.user2.user_likes.count(), 1)
        self.assertEqual(self.user3.user_likes.count(), 0)
        self.user1LikedUser1Post.delete()
        self.assertEqual(self.user1.user_likes.count(), 2)

    def test_post_count(self):
        self.assertEqual(self.user1.posts.count(), 2)
        self.assertEqual(self.user2.posts.count(), 1)
        self.user3Post.delete()
        self.assertEqual(self.user3.posts.count(), 0)

class CreatePostTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.get(self.live_server_url + '/register')
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')
        password_confirmation_input = self.driver.find_element_by_name('confirmation')
        register_btn = self.driver.find_element_by_class_name('btn')
        username_input.send_keys('testuser')
        password_input.send_keys('testpass')
        password_confirmation_input.send_keys('testpass')
        register_btn.click()

    def test_create_post(self):
        self.driver.get(self.live_server_url + '/login')
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')
        login_btn = self.driver.find_element_by_class_name('btn')
        username_input.send_keys('testuser')
        password_input.send_keys('testpass')
        login_btn.click()

        create_post_btn = self.driver.find_element_by_class_name('btn')
        post_form = self.driver.find_element_by_name('content')
        post_form.send_keys('Some input for a post')
        create_post_btn.click()

        self.assertEqual(Post.objects.count(), 1)
        


