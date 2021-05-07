from django.shortcuts import render, redirect
import re, base64

# Create your views here.
from django.http import HttpResponse
import os
import requests, json
from flask import jsonify


# def index(request):
#     url = 'https://apisimpleapp.herokuapp.com/post/1'
#     r = requests.get(url)
#     data = r.json()
#     print(data)
#     # return HttpResponse("Title is " + data[0]['title'])
#     return HttpResponse(data)

def index(request):

    url = 'https://apithaytru.herokuapp.com/post?state=id_category=2,status=1&limit=4&sort=create_time,desc'
    r = requests.get(url)
    soccer_feed = r.json()
    
    url_category = 'https://apithaytru.herokuapp.com/category'
    category_response = requests.get(url_category)
    categories = category_response.json()

    url_lastest = 'https://apithaytru.herokuapp.com/post?state=status=1&limit=5&sort=create_time,desc'
    lastest_response = requests.get(url_lastest)
    lastest_post = lastest_response.json()

    url_popular = 'https://apithaytru.herokuapp.com/post?state=status=1&limit=8&sort=rating,desc'
    popular_response = requests.get(url_popular)
    popular_post = popular_response.json()

    simple_category = dict(zip([item['id_category'] for item in categories], [item['name'] for item in categories]))

    for i in range(len(soccer_feed)):
        soccer_feed[i]['category_name'] = simple_category[soccer_feed[i]['id_category']]

    for i in range(len(lastest_post)):
        lastest_post[i]['category_name'] = simple_category[lastest_post[i]['id_category']]

    for i in range(len(popular_post)):
        popular_post[i]['category_name'] = simple_category[popular_post[i]['id_category']]

    preview = lastest_post[0]['content'].split('\n')[0]


    return render(request, 'index.html', { 'soccer_feed' : soccer_feed, 'categories' : categories, 'lastest_post' : lastest_post, 'popular_post' : popular_post, 'preview' : preview})

def search(request):
    url = 'https://apithaytru.herokuapp.com/post'
    r = requests.get(url)
    all_post = r.json()
    keyword = request.POST.get('search', False)
    print(keyword)
    result = []
    for item in all_post:
        if re.search(keyword, item['title']):
            item['preview'] = item['content'].split('\n')[0]
            result.append(item)
    print(result)
    return render(request, 'search.html', { 'result' : result})

def contact(request):
    return render(request, 'contact.html')

def login(request):
    if request.method == 'GET':
        value = request.COOKIES.get('Authorization')
        response = render(request, 'login.html')
        index_response = redirect('/test/index.html')
        logged_in_url = 'http://127.0.0.1:5000/index'
        if value != None:
            bearer = 'Bearer ' + value
            headers = {'Authorization' : bearer}
            r = requests.get(logged_in_url, headers=headers)
            result = r.json()
            if 'Logged' in result:
                return index_response
        refresh_token = request.COOKIES.get('refresh_token')
        if(refresh_token != None):
            new_authorization = refresh_authorization(refresh_token)
            if 'access_token' in new_authorization:
                new_bearer = 'Bearer ' + new_authorization['access_token']
                new_headers = {'Authorization' : new_bearer}
                r = requests.get(logged_in_url, headers=new_headers)
                new_result = r.json()
                if 'Logged' in new_result:
                    index_response.set_cookie('Authorization', new_authorization['access_token'])
                    return index_response
        return response
    else:
        sign_in_url = 'http://127.0.0.1:5000/login'
        headers = {'email' : request.POST.get('email', False), 'password' : request.POST.get('password', False)}
        r = requests.get(sign_in_url, headers=headers)
        try:
            tokens = r.json()
            success_response = redirect('/test/index.html')
            success_response.set_cookie('Authorization', tokens['access_token'])
            success_response.set_cookie('refresh_token', tokens['refresh_token'])
            return success_response
        except Exception as er:
            print(er)
            fail_response = render(request, 'login.html', { 'error' : er })
            return fail_response


def register(request):
    return render(request, 'register.html')

def post(request, post_id):
    url_post = 'http://127.0.0.1:5000/post/' + str(post_id)
    r = requests.get(url_post)
    if len(r.json()) < 0:
        return render(request, 'page.html', {'content' : 'Bài viết không tồn tại'})
    data = r.json()[0]
    content = data['content'].split('\n')
    data['content'] = content
    return render(request, 'page.html', data)

def page(request):
    return render(request, 'page.html')

def addPost(request):
    if request.method == 'GET':
        url_category = 'http://127.0.0.1:5000/category'
        category_response = requests.get(url_category)
        categories = category_response.json()
        #simple_category = dict(zip([item['id_category'] for item in categories], [item['name'] for item in categories]))
        return render(request, 'insert_news.html', { 'categories' : categories })
    else:
        title = request.POST.get('title', True)
        content = request.POST.get('content', True)
        id_category = request.POST.get('id_category', True)
        img = request.FILES.get('img', True)
        imgStream = img.read()
        imgstr = base64.b64encode(imgStream)
        imgstr_decoded = imgstr.decode('ascii')
        # newImgStream = base64.b64decode(imgstr)
        # with open('newfile.txt', 'w') as destination:
        #     destination.write(imgstr_decoded)
        #     destination.close()

        url_addPost = 'http://127.0.0.1:5000/post/add'
        data = {"title" : title, "content" : content, "category" : id_category, "img" : imgstr_decoded}
        token = request.COOKIES.get('Authorization')
        bearer = 'Bearer ' + token
        headers = {'Authorization' : bearer}
        data_json = json.dumps(data)
        result = requests.post(url_addPost, json=data_json, headers=headers)
        print(data_json)
        print(type(data_json))
        print(type(data))
        # print(result.json())
        return HttpResponse('<p>success</p>')


def category(request):
    return render(request, 'category.html')

def refresh_authorization(refresh_token):
    # print('refreshing token')
    refresh_url = 'http://127.0.0.1:5000/refresh'
    refresh_bearer = 'Bearer ' + refresh_token
    # print('Refresh bearer: ' + refresh_bearer)
    refresh_header = {'Authorization' : refresh_bearer}
    refresh_response = requests.post(refresh_url, headers=refresh_header)

    refreshed_token = refresh_response.json()
    return refreshed_token
    # print('Token after refresh:')
    # print(refreshed_token)