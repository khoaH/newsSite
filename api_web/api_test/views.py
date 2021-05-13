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

def admin(request):
    value = request.COOKIES.get('Authorization')
    response = redirect('/test/login.html')
    logged_in_url = 'https://apithaytru.herokuapp.com/login'
    if value != None:
        bearer = 'Bearer ' + value
        headers = {'Authorization' : bearer}
        r = requests.get(logged_in_url, headers=headers)
        if r.status_code == 200:
            result = r.json()
            result.pop('status')
            dashboard_response = render(request, 'admin.html', {'user_info' : result})
            # dashboard_response.set_cookie('user_info', result)
            return dashboard_response
    refresh_token = request.COOKIES.get('refresh_token')
    if(refresh_token != None):
        new_authorization = refresh_authorization(refresh_token)
        if 'access_token' in new_authorization:
            new_bearer = 'Bearer ' + new_authorization['access_token']
            new_headers = {'Authorization' : new_bearer}
            r = requests.get(logged_in_url, headers=new_headers)
            if r.status_code == 200:
                result = r.json()
                result.pop('status')
                dashboard_response = render(request, 'admin.html', {'user_info' : result})
                # dashboard_response.set_cookie('user_info', result)
                dashboard_response.set_cookie('Authorization', new_authorization['access_token'], max_age=1800)
                return dashboard_response
    response.delete_cookie('Authorization')
    response.delete_cookie('refresh_token')
    return response

def newsController(request):
    status, user_info, extra = checkCookie(request)
    if status:
        print(user_info)
        
        result = None
        if user_info['role'] == 1:
            url = 'https://apithaytru.herokuapp.com/post?sort=create_time,desc'
            r = requests.get(url)
            result = r.json()
        else:
            url = 'https://apithaytru.herokuapp.com/post?state=create_by=' + str(user_info['idaccount'])+ '&sort=create_time,desc'
            r = requests.get(url)
            result = r.json()
        # print(result)
        response = render(request, 'pages-post.html', {'user_info' : user_info, 'posts' : result})

        if extra != None:
            response.set_cookie('Authorization', extra, max_age=1800)
        return response
    else:
        return extra
    # value = request.COOKIES.get('Authorization')
    # response = redirect('/test/login.html')
    # logged_in_url = 'https://apithaytru.herokuapp.com/login'
    # if value != None:
    #     bearer = 'Bearer ' + value
    #     headers = {'Authorization' : bearer}
    #     r = requests.get(logged_in_url, headers=headers)
    #     if r.status_code == 200:
    #         result = r.json()
    #         result.pop('status')
    #         dashboard_response = render(request, 'pages-post.html', {'user_info' : result})
    #         # dashboard_response.set_cookie('user_info', result)
    #         return dashboard_response
    # refresh_token = request.COOKIES.get('refresh_token')
    # if(refresh_token != None):
    #     new_authorization = refresh_authorization(refresh_token)
    #     if 'access_token' in new_authorization:
    #         new_bearer = 'Bearer ' + new_authorization['access_token']
    #         new_headers = {'Authorization' : new_bearer}
    #         r = requests.get(logged_in_url, headers=new_headers)
    #         if r.status_code == 200:
    #             result = r.json()
    #             result.pop('status')
    #             dashboard_response = render(request, 'pages-post.html', {'user_info' : result})
    #             # dashboard_response.set_cookie('user_info', result)
    #             dashboard_response.set_cookie('Authorization', new_authorization['access_token'], max_age=1800)
    #             return dashboard_response
    # response.delete_cookie('Authorization')
    # response.delete_cookie('refresh_token')
    # return response

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

    url_category = 'https://apithaytru.herokuapp.com/category'
    category_response = requests.get(url_category)
    categories = category_response.json()

    for item in all_post:
        if re.search(keyword, item['title']):
            item['preview'] = item['content'].split('\n')[0]
            result.append(item)
    return render(request, 'search.html', { 'result' : result, 'categories' : categories})

def category(request, id_category):
    url = 'https://apithaytru.herokuapp.com/post?state=id_category=' + str(id_category) + ',status=1&sort=create_time,desc'
    r = requests.get(url)
    category_feed = r.json()

    url_category = 'https://apithaytru.herokuapp.com/category'
    category_response = requests.get(url_category)
    categories = category_response.json()


    if len(category_feed) < 1:
        return render(request, 'notFound.html', {'categories' : categories})
    else:
        for i in range(len(category_feed)):
            category_feed[i]['preview'] = category_feed[i]['content'].split('\n')[0]
        return render(request, 'category.html', { 'result' : category_feed, 'categories' : categories})

def contact(request):

    url_category = 'https://apithaytru.herokuapp.com/category'
    category_response = requests.get(url_category)
    categories = category_response.json()

    return render(request, 'contact.html', { 'categories' : categories })

def logout(request):
    response = redirect('/test/login.html')
    response.delete_cookie('Authorization')
    response.delete_cookie('refresh_token')
    # response.delete_cookie('user_info')
    return response

def login(request):
    if request.method == 'GET':
        value = request.COOKIES.get('Authorization')
        refresh_token = request.COOKIES.get('refresh_token')
        response = render(request, 'login.html')
        index_response = redirect('/test/admin.html')
        logged_in_url = 'https://apithaytru.herokuapp.com/login'
        if value != None or refresh_token != None:
            return index_response
        #     bearer = 'Bearer ' + value
        #     headers = {'Authorization' : bearer}
        #     r = requests.get(logged_in_url, headers=headers)
        #     if r.status_code == 200:
        #         result = r.json()
        #         result.pop('status')
        #         index_response.set_cookie('user_info', result)
        #         return index_response
        # refresh_token = request.COOKIES.get('refresh_token')
        # if(refresh_token != None):
        #     new_authorization = refresh_authorization(refresh_token)
        #     if 'access_token' in new_authorization:
        #         new_bearer = 'Bearer ' + new_authorization['access_token']
        #         new_headers = {'Authorization' : new_bearer}
        #         r = requests.get(logged_in_url, headers=new_headers)
        #         new_result = r.json()
        #         if r.status_code == 200:
        #             result = r.json()
        #             result.pop('status')
        #             index_response.set_cookie('user_info', result)
        #             index_response.set_cookie('Authorization', new_authorization['access_token'], max_age=1800)
        #             return index_response
        return response
    else:
        sign_in_url = 'https://apithaytru.herokuapp.com/login'
        headers = {'email' : request.POST.get('email', False), 'password' : request.POST.get('password', False)}
        r = requests.get(sign_in_url, headers=headers)
        er = 'Error'
        if r.status_code == 200:
            tokens = r.json()
            success_response = redirect('/test/admin.html')
            success_response.set_cookie('Authorization', tokens['access_token'], max_age=1800)
            success_response.set_cookie('refresh_token', tokens['refresh_token'], max_age=2592000)
            # tokens.pop('access_token')
            # tokens.pop('refresh_token')
            # tokens.pop('status')
            # success_response.set_cookie('user_info', tokens)
            return success_response
        else:
            er = 'Invalid Username or Password'
            fail_response = render(request, 'login.html', { 'error' : er })
            return fail_response

def register(request):
    if request.method == 'GET':
        value = request.COOKIES.get('Authorization')
        refresh_token = request.COOKIES.get('refresh_token')
        if value != None or refresh_token != None:
            return redirect('/test/admin.html')
        return render(request, 'register.html')
    else:
        password = str(request.POST.get('password', False)).strip()
        email = str(request.POST.get('email', False)).strip()
        username = str(request.POST.get('username', False)).strip()
        if password == '':
            return render(request, 'register.html', {'error' : 'Password is empty'})
        elif email == '':
            return render(request, 'register.html', {'error' : 'Email is empty'})   
        elif username == '':
            return render(request, 'register.html', {'error' : 'Username is empty'})                   
        elif password != request.POST.get('password-repeat', False):
            return render(request, 'register.html', {'error' : 'Password dont match'})
        elif request.POST.get('agree', False) != 'on':
            return render(request, 'register.html', {'error' : 'We cant register you if you dont agree with our terms'})
        else:
            url = 'https://apithaytru.herokuapp.com/account/reg'
            headers = {'username' : username, 'email' : email, 'password' : password}
            r = requests.post(url, headers=headers)
            result = r.json()

            if(result['status'] == 4):
                return render(request, 'register.html', {'error' : 'Email existed'})
            elif(result['status'] != 0):
                return render(request, 'register.html', {'error' : 'Something went wrong'})
            else:
                return render(request, 'register.html', {'error' : 'Success'})

def post(request, post_id):
    url_post = 'https://apithaytru.herokuapp.com/post/' + str(post_id)
    r = requests.get(url_post)
    if len(r.json()) < 0:
        return render(request, 'page.html', {'content' : 'Bài viết không tồn tại'})
    data = r.json()[0]
    content = data['content'].split('\n')
    data['content'] = content
        
    url_category = 'https://apithaytru.herokuapp.com/category'
    category_response = requests.get(url_category)
    categories = category_response.json()

    data['categories'] = categories

    return render(request, 'page.html', data)

def page(request):
    return render(request, 'page.html')

def addPost(request):
    if request.method == 'GET':
        status, user_info, extra = checkCookie(request)
        if status:
            url_category = 'https://apithaytru.herokuapp.com/category'
            category_response = requests.get(url_category)
            categories = category_response.json()
            #simple_category = dict(zip([item['id_category'] for item in categories], [item['name'] for item in categories]))
            response =  render(request, 'insert_news.html', { 'categories' : categories , 'user_info' : user_info})
            if extra != None:
                response.set_cookie('Authorization', extra, max_age=1800)
            return response
        else:
            return extra
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

        url_addPost = 'https://apithaytru.herokuapp.com/post/add'
        data = {"title" : title, "content" : content, "category" : id_category, "img" : imgstr_decoded}
        token = request.COOKIES.get('Authorization')
        bearer = 'Bearer ' + token
        headers = {'Authorization' : bearer}
        data_json = json.dumps(data)
        result = requests.post(url_addPost, json=data_json, headers=headers)
        # print(data_json)
        # print(type(data_json))
        # print(type(data))
        print(result.status_code)
        return redirect('/test/pages-post.html')

def editPost(request, post_id):
    if request.method == 'GET':
        status, user_info, extra = checkCookie(request)
        if status:
            url_category = 'https://apithaytru.herokuapp.com/category'
            category_response = requests.get(url_category)
            categories = category_response.json()
            url_post = 'https://apithaytru.herokuapp.com/post/' + str(post_id)
            post_response = requests.get(url_post)
            post_data = post_response.json()
            #simple_category = dict(zip([item['id_category'] for item in categories], [item['name'] for item in categories]))
            response =  render(request, 'edit_news.html', { 'categories' : categories , 'user_info' : user_info, 'post' : post_data[0]})
            if extra != None:
                response.set_cookie('Authorization', extra, max_age=1800)
            return response
        else:
            return extra
    else:
        title = request.POST.get('title', True)
        content = request.POST.get('content', True)
        id_category = request.POST.get('id_category', True)
        imgstr_decoded = ''
        try :
            img = request.FILES.get('img', True)
            imgStream = img.read()
            imgstr = base64.b64encode(imgStream)
            imgstr_decoded = imgstr.decode('ascii')
        except:
            url_post = 'https://apithaytru.herokuapp.com/post/' + str(post_id)
            post_response = requests.get(url_post)
            post_data = post_response.json()
            post_data = post_data[0]
            img_link = post_data['img']
            r = requests.get(img_link)
            imgStream = r.content
            imgstr = base64.b64encode(imgStream)
            imgstr_decoded = imgstr.decode('ascii')


        # newImgStream = base64.b64decode(imgstr)
        # with open('newfile.txt', 'w') as destination:
        #     destination.write(imgstr_decoded)
        #     destination.close()

        url_editPost = 'http://127.0.0.1:5000/post/edit/' + str(post_id)
        data = {"title" : title, "content" : content, "category" : id_category, "img" : imgstr_decoded}
        if extra != None:
            token = extra
        else:
            token = request.COOKIES.get('Authorization')
        bearer = 'Bearer ' + token
        headers = {'Authorization' : bearer}
        data_json = json.dumps(data)
        result = requests.post(url_editPost, json=data_json, headers=headers)
        # print(data_json)
        # print(type(data_json))
        # print(type(data))
        print(result.status_code)
        return redirect('/test/pages-post.html')

def deletePost(request, post_id):
    status, user_info, extra = checkCookie(request)
    if status:
        url_delPost = 'http://127.0.0.1:5000/post/del/' + str(post_id)
        if extra != None:
            token = extra
        else:
            token = request.COOKIES.get('Authorization')
        bearer = 'Bearer ' + token
        headers = {'Authorization' : bearer}
        r = requests.post(url_delPost, headers=headers)
        print(r.status_code)
        response =  redirect('/test/pages-post.html')
        if extra != None:
            response.set_cookie('Authorization', extra, max_age=1800)
        return response
    else:
        return extra

def userController(request):
    status, user_info, extra = checkCookie(request)
    if status:
        print(user_info)
        
        result = None
        if user_info['role'] == 1:
            url = 'https://apithaytru.herokuapp.com/account'
            if extra != None:
                token = extra
            else:
                token = request.COOKIES.get('Authorization')
            bearer = 'Bearer ' + token
            headers = {'Authorization' : bearer}
            r = requests.get(url, headers=headers)
            result = r.json()
        else:
            result = []
        # print(result)
        response = render(request, 'pages-users.html', {'user_info' : user_info, 'users' : result})

        if extra != None:
            response.set_cookie('Authorization', extra, max_age=1800)
        return response
    else:
        return extra


def checkCookie(request):
    value = request.COOKIES.get('Authorization')
    response = redirect('/test/login.html')
    logged_in_url = 'https://apithaytru.herokuapp.com/login'
    if value != None:
        bearer = 'Bearer ' + value
        headers = {'Authorization' : bearer}
        r = requests.get(logged_in_url, headers=headers)
        if r.status_code == 200:
            result = r.json()
            result.pop('status')
            # dashboard_response.set_cookie('user_info', result)
            return True, result, None
    refresh_token = request.COOKIES.get('refresh_token')
    if(refresh_token != None):
        new_authorization = refresh_authorization(refresh_token)
        if 'access_token' in new_authorization:
            new_bearer = 'Bearer ' + new_authorization['access_token']
            new_headers = {'Authorization' : new_bearer}
            r = requests.get(logged_in_url, headers=new_headers)
            if r.status_code == 200:
                result = r.json()
                result.pop('status')
                # dashboard_response.set_cookie('user_info', result)
                # dashboard_response.set_cookie('Authorization', new_authorization['access_token'], max_age=1800)
                return True, result, new_authorization['access_token']
    response.delete_cookie('Authorization')
    response.delete_cookie('refresh_token')
    return False, None, response

def refresh_authorization(refresh_token):
    # print('refreshing token: \n' + refresh_token)
    refresh_url = 'https://apithaytru.herokuapp.com/refresh'
    refresh_bearer = 'Bearer ' + refresh_token
    # print('Refresh bearer: ' + refresh_bearer)
    refresh_header = {'Authorization' : refresh_bearer}
    refresh_response = requests.get(refresh_url, headers=refresh_header)
    # print(refresh_response)
    refreshed_token = refresh_response.json()
    # print(refreshed_token)
    return refreshed_token
    # print('Token after refresh:')
    # print(refreshed_token)