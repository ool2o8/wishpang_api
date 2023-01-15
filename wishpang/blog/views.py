from account.serializer import UserSerializer
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from requests import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from account.models import Coupang
from blog.models import Post, Comment, Product, ProductData 
from blog.serializer import PostSerializer, LikeUserSerializer, LikeSerializer, ProductSerializer, ProductDataSerializer, ProductDataListSerializer
from blog.serializer import CommentSerializer
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from django.db.models import Max, Min
from config.utils import secret
import json

secrets=secret()


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.auth_id == request.user


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer


class UserPostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = PostSerializer

    def get(self, request):
        queryset = Post.objects.filter(auth=User.objects.get(id=request.user.id))
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


class CommentViewSet(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer
    def get(self, request, pk):
        queryset = Comment.objects.select_related('auth').filter(post_id=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
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
    serializer_class = LikeSerializer

    def get(self, request, post_pk):
        if request.user.is_authenticated:
            serializer_class = LikeSerializer
            post = Post.objects.get(id=post_pk)
            queryset=User.objects
            serializer = LikeSerializer(post)
            if post.liker.filter(id=request.user.id).exists():
                post.liker.remove(User.objects.get(id=request.user.id))
            else:
                post.liker.add(User.objects.get(id=request.user.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return redirect('http://127.0.0.1/blog/{post_pk}/post/like-list/')


class PostLikeListView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [SessionAuthentication]
    def get(self, request, post_pk):
        queryset = User.objects.prefetch_related('like_post').filter(like_post=post_pk)
        serializer = LikeUserSerializer(queryset, many=True)
        # if post.liker.filter(pk=request.user.pk).exists():
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    def get(self, request):
        queryset=Product.objects.prefetch_related('wisher').all()
        serializer=ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProductUpdate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductDataSerializer
    def get(self, request):
        coupang=Coupang.objects.get(user=request.user)
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
        driver.find_element(By.ID, 'login-email-input').send_keys(coupang.username)
        driver.find_element(By.ID, 'login-password-input').send_keys(coupang.password)

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
                    product_link = el.find_element(
                        By.XPATH, 'td[@class="product-box"]/div[@class="product-name-part"]/a').get_attribute('href')
                    
                    res,_ = Product.objects.update_or_create(id=id, name=product_name, url=product_link)
                    res.wisher.add(User.objects.get(id=request.user.id))
        queryset = Product.objects.all()
        serializer=ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProductDataUpdateView(APIView):
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductDataSerializer
    def get(self, request):
        from cron import main
        main()
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProductDataView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductDataSerializer
    def get(self, request):
        queryset = ProductData.objects.filter(wisher=request.user.id)
        serializer=ProductDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDataView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class=ProductDataListSerializer
    queryset=ProductData.objects.all()
    def list(self, request, product_id):
        queryset=ProductData.objects.filter(product_id=product_id).order_by('time').all()
        serializer=ProductDataListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def GetBucket(self, request):
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
                product_link = el.find_element(
                    By.XPATH, 'td[@class="product-box"]/div[@class="product-name-part"]/a').get_attribute('href')
                
                res,_ = Product.objects.get_or_create(id=id, name=product_name, url=product_link)
                res.wisher.add(User.objects.get(id=request.user.id))


def Update_ProductData(self, request):
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

        products=Product.objects.all()
        for product in products:
            driver.get(product.url)
            driver.implicitly_wait(2) 
            elements=driver.find_elements(By.XPATH, '[@id="contents"]')
            print(elements)