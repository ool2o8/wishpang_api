from account.serializer import UserSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from requests import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from blog.models import Post
from blog.models import Comment, Wish, Product
from blog.serializer import PostSerializer, LikeUserSerializer, LikeSerializer, ProductSerializer, WishSerializer, ProductPriceSerializer
from blog.serializer import CommentSerializer
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import time
import datetime
import schedule
from xml.dom.minidom import Element

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from django.db.models import Max, Min, Avg



class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.auth_id == request.user


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        queryset = Post.objects.filter(auth_id=request.user.id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        queryset = Post.objects.create(
            title=request.POST.get('title'),
            auth=User.objects.get(id=request.user.id),
            contents=request.POST.get('contents')
        )
        serializer = PostSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, pk):
        queryset = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk):
        queryset = Comment.objects.create(
            auth=User.objects.get(id=request.user.id),
            post=Post.objects.get(id=pk),
            contents=request.POST.get('contents')
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#좋아요 기능


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, post_pk):
        if request.user.is_authenticated:
            serializer_class = LikeSerializer
            post = Post.objects.get(id=post_pk)
            serializer = LikeSerializer(post)

            if post.liker.filter(pk=request.user.pk).exists():
                post.liker.remove(User.objects.get(id=request.user.id))
            else:
                post.liker.add(User.objects.get(id=request.user.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return redirect('http://127.0.0.1/blog/{post_pk}/post/like-list/')


class PostLikeListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    def list(self, request, post_pk):
        queryset = User.objects.filter(like_post=post_pk)
        serializer = LikeUserSerializer(queryset, many=True)
        # if post.liker.filter(pk=request.user.pk).exists():
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyWishUpdateView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    serializer_class=WishSerializer
    queryset=Wish.objects.all()
    def crawling(self, request):
        options = webdriver.ChromeOptions()
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "prefs", {"prfile.managed_default_content_setting.images": 2})

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                            "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
        driver.get(r"https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F")

        driver.implicitly_wait(2)
        driver.find_element(By.ID, 'login-email-input').send_keys('ncr7804@naver.com')
        driver.find_element(By.ID, 'login-password-input').send_keys('mijung1208!')

        driver.implicitly_wait(2)
        driver.find_element(
            By.CSS_SELECTOR, 'body > div.member-wrapper.member-wrapper--flex > div > div > form > div.login__content.login__content--trigger > button').click()

        driver.implicitly_wait(10)
        driver.find_element(
            By.XPATH, """//*[@id="header"]/section/div/ul/li[2]/a""").click()

        driver.implicitly_wait(3)

        elements = driver.find_elements(
            By.CSS_SELECTOR, '#cartTable-rocket-fresh > tr')
        for el in elements:
            if el.get_attribute('class') == 'cart-deal-item':
                if el.get_attribute('data-item-status') == 'MISSED':
                    product_name = el.find_element(
                        By.XPATH, 'td[@class="product-box relative"]/div[@class="product-name-part"]/a').text
                else:
                    id = el.find_element(
                        By.XPATH, 'td[@class="product-box"]/div[@id]').get_attribute('id')
                    product_name = el.find_element(
                        By.XPATH, 'td[@class="product-box"]/div[@class="product-name-part"]/a').text
                    
                    getprice = el.find_element(
                        By.XPATH, 'td[@class="unit-total-price"]/div[@class="unit-total-sale-price"]').text
                    price = 0
                    for i in getprice:
                        if i <= '9' and i >= '0':
                            price = price*10+int(i)
                    quantity = el.find_element(
                                    By.XPATH, 'td[@class="product-box"]/div[@id]/div[@class="option-price-part"]/span[@class="select-select"]/select[@class="quantity-select"]').get_attribute('data-quantity')
                    quantity = int(quantity)
                    image=el.find_element(By.XPATH, 'td/a/img').get_attribute('src')
                    res,_ = Product.objects.get_or_create(id=id, name=product_name, image=image)
                    wish = Wish.objects.create(
                        product=res, price=price/quantity, time=datetime.datetime.now())
                    wish.wisher.add(User.objects.get(id=request.user.id))
        driver.quit()
    def list(self, request):
        self.crawling(request)
        queryset = Product.objects.all()
        serializer=ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MyWishView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=WishSerializer
    queryset=Wish.objects.all()
   
    def list(self, request):
        queryset = Wish.objects.filter(wisher=request.user.id)
        serializer=WishSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WishProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductSerializer
    queryset=Wish.objects.all()
    def list(self, request):
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishPriceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=WishSerializer
    queryset=Wish.objects.all()
    def retrieve(self, request, product_id):
        queryset=Wish.objects.filter(product__id=product_id).order_by('-price').first()
        serializer=WishSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WishPriceListView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]
    serializer_class=WishSerializer
    queryset=Product.objects.all()
    def list(self, request):
        queryset=Wish.objects.all().values('product_id', 'product__name').annotate(min=Min('price'), max=Max('price'))
        serializer=WishSerializer(queryset, many=True)
        return Response(queryset, status=status.HTTP_200_OK)

def crawling(self, request):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "prefs", {"prfile.managed_default_content_setting.images": 2})

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                            "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
        driver.get(r"https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F")

        driver.implicitly_wait(2)
        driver.find_element(By.ID, 'login-email-input').send_keys('ncr7804@naver.com')
        driver.find_element(By.ID, 'login-password-input').send_keys('mijung1208!')

        driver.implicitly_wait(2)
        driver.find_element(
            By.CSS_SELECTOR, 'body > div.member-wrapper.member-wrapper--flex > div > div > form > div.login__content.login__content--trigger > button').click()

        driver.implicitly_wait(5)
        driver.find_element(
            By.XPATH, """//*[@id="header"]/section/div/ul/li[2]/a""").click()

        driver.implicitly_wait(3)

        elements = driver.find_elements(
            By.CSS_SELECTOR, '#cartTable-rocket-fresh > tr')

        for el in elements:
            if el.get_attribute('class') == 'cart-deal-item':
                if el.get_attribute('data-item-status') == 'MISSED':
                    product_name = el.find_element(
                        By.XPATH, 'td[@class="product-box relative"]/div[@class="product-name-part"]/a').text
                else:
                    id = el.find_element(
                        By.XPATH, 'td[@class="product-box"]/div[@id]').get_attribute('id')
                    product_name = el.find_element(
                        By.XPATH, 'td[@class="product-box"]/div[@class="product-name-part"]/a').text
                    
                    getprice = el.find_element(
                        By.XPATH, 'td[@class="unit-total-price"]/div[@class="unit-total-sale-price"]').text
                    price = 0
                    for i in getprice:
                        if i <= '9' and i >= '0':
                            price = price*10+int(i)
                    quantity = el.find_element(
                                    By.XPATH, 'td[@class="product-box"]/div[@id]/div[@class="option-price-part"]/span[@class="select-select"]/select[@class="quantity-select"]').get_attribute('data-quantity')
                    quantity = int(quantity)
                    res,_ = Product.objects.get_or_create(id=id, name=product_name)
                    wish = Wish.objects.create(
                        product=res, price=price/quantity, time=datetime.datetime.now())
                    wish.wisher.add(User.objects.get(id=request.user.id))
   