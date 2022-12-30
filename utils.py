#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:工具类
@Date       :2021/08/16
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import threading
import configparser
import os
import re
import json

import requests
from my_fake_useragent import UserAgent
import subprocess

ua = UserAgent(family='chrome')


def site_enable(url):
    try:
        r = request_net(url)
        if r.status_code == 200:
            print('链接【%s】检查通过.^~^' % url)
            return True
        print('链接【%s】不可用，状态【%d】' % (url, r.status_code))
    except Exception as e:
        print('链接【{}】不可用，异常【{}】'.format(url, e))
    return False


def site_ping(url):
    try:
        domain = get_domain(url).replace('http://', '').replace('https://', '').replace('/', '')
        command = ['ping', '-c', '1', domain]
        result = subprocess.run(command, timeout=1.0)
        if result.returncode == 0:
            print('链接【%s】检查通过.^~^' % url)
            return True
    except Exception as e:
        # print('链接【{}】不可用，异常【{}】'.format(url, e))
        pass
    print('链接【%s】失败----------------' % url)
    return False


def request_net(url, allow_redirects=True, verify=False, timeout=20):
    """最终的请求实现"""
    requests.packages.urllib3.disable_warnings()
    return requests.get(url=url, allow_redirects=allow_redirects, verify=verify, timeout=timeout,
                        headers={'user-agent': ua.random()})


def get_domain(url: str = None):
    """
    获取链接地址的域名
    :param url:
    :return:
    """
    # http://youtube.com/watch
    return re.match(r"(http://|https://).*?\/", url, re.DOTALL).group(0)


def append_head(site_title, site_icon, avatar, href, name, desc, location):
    page = '''<!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <link rel="stylesheet" href="static/style.css">
        <link rel="stylesheet" href="static/life-style.css">
        <title>{}</title>
        <link rel="icon" href="{}" type="image/x-icon">

    <body class="main-center no-sidebar" itemscope="" itemtype="http://schema.org/WebPage">

    <main class="main" role="main">
        <article class="article archives-life article-type-normal" itemscope="">
            <div class="article-body">
                <div class="container" id="container">
                    <aside class="left-bar" id="leftBar" style="left: 0px;">
                        <div class="profile-block text-center">
                            <a id="avatar" href="{}" target="_blank">
                                <img class="img-circle img-rotate" src="{}" width="200" height="200">
                            </a>
                            <h2 id="name" class="hidden-xs hidden-sm">{}</h2>
                            <h3 id="title" class="hidden-xs hidden-sm hidden-md">{}</h3>
                            <small id="location" class="text-muted hidden-xs hidden-sm"><i class="icon icon-map-marker"></i>
                                {}</small>
                        </div>
                        <nav class="nav">
                        <div class="item active">
                            <a href="./">Top</a>
                            <i class="line"></i>
                        </div>
                        <ul class="nav-item" id="navItem">'''.format(site_title, site_icon, href, avatar, name, desc,
                                                                     location)
    return page


def get_tail():
    return '''          <div id="fixedBarTop">
                            <svg title="回到顶部" fill="currentColor" viewBox="0 0 1024 1024" version="1.1"
                                 xmlns="http://www.w3.org/2000/svg" p-id="3245" width="64" height="64">
                                <path d="M76.8 480l422.4-422.4c6.4-6.4 19.2-6.4 25.6 0l422.4 422.4c6.4 6.4 12.8 6.4 19.2 6.4 6.4 0 12.8 0 19.2-6.4 12.8-12.8 12.8-25.6 0-38.4L556.8 19.2c-25.6-25.6-76.8-25.6-102.4 0L32 441.6C25.6 448 25.6 467.2 32 480S64 492.8 76.8 480z"
                                      p-id="3246" fill="#009688"></path>
                                <path d="M32 672 140.8 672 140.8 1017.6 192 1017.6 192 672 300.8 672 300.8 633.6 32 633.6Z"
                                      p-id="3247" fill="#009688"></path>
                                <path d="M499.2 627.2c-57.6 0-102.4 19.2-134.4 57.6-32 38.4-51.2 89.6-51.2 147.2 0 57.6 19.2 102.4 51.2 140.8C396.8 1004.8 441.6 1024 492.8 1024c57.6 0 102.4-19.2 134.4-57.6s51.2-89.6 51.2-147.2c0-57.6-19.2-102.4-51.2-140.8C601.6 640 556.8 627.2 499.2 627.2zM595.2 940.8c-25.6 25.6-57.6 38.4-96 38.4-38.4 0-70.4-12.8-96-44.8-25.6-25.6-38.4-64-38.4-115.2 0-44.8 12.8-83.2 38.4-115.2 25.6-25.6 57.6-44.8 96-44.8 38.4 0 70.4 12.8 96 38.4 25.6 25.6 32 64 32 115.2C627.2 876.8 614.4 908.8 595.2 940.8z"
                                      p-id="3248" fill="#009688"></path>
                                <path d="M960 659.2c-25.6-19.2-57.6-32-96-32l-108.8 0 0 384 51.2 0 0-147.2 51.2 0c38.4 0 76.8-12.8 102.4-32 25.6-25.6 38.4-51.2 38.4-89.6C998.4 710.4 985.6 678.4 960 659.2zM921.6 806.4c-12.8 12.8-38.4 19.2-70.4 19.2l-44.8 0 0-153.6 51.2 0c57.6 0 89.6 25.6 89.6 76.8C947.2 774.4 934.4 793.6 921.6 806.4z"
                                      p-id="3249" fill="#009688"></path>
                            </svg>
                        </div>
                    </div>
                </section>
                <script src="static/jquery.js"></script>
                <script>
                    var oLeftBar = document.getElementById('leftBar');
                    var menuFrom = document.getElementById('menu-form');
                    window.onresize = function () {
                        judgeWidth();
                    };

                    function judgeWidth() {
                        if (document.documentElement.clientWidth > 481) {
                            oLeftBar.style.left = 0;
                        } else {
                            oLeftBar.style.left = -249 + 'px';
                        }
                    }

                    var oNavItem = document.getElementById('navItem');
                    var aA = oNavItem.getElementsByTagName('a');
                    for (var i = 0; i < aA.length; i++) {
                        aA[i].onclick = function () {
                            for (var j = 0; j < aA.length; j++) {
                                aA[j].className = '';
                            }
                            this.className = 'active';
                            if (oLeftBar.offsetLeft == 0) {
                                if (document.documentElement.clientWidth <= 481) {
                                    oLeftBar.style.left = -249 + 'px';
                                    menuFrom.checked = false;
                                }
                            }
                        }
                    }
                    $(window).scroll(function () {
                        if ($(window).scrollTop() >= 200) {
                            $('#fixedBarTop').fadeIn(300);
                        } else {
                            $('#fixedBarTop').fadeOut(300);
                        }
                    });
                    $('#fixedBarTop').click(function () {
                        $('html,body').animate({scrollTop: '0px'}, 800);
                    })
                </script>
            </div>
        </div>
    </article>
</main>

<script src="static/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="js/jquery.min.js"><\/script>')</script>
<script src="static/plugin.min.js"></script>
<script src="static/application.js"></script>
<script src="static/insight.js"></script>
</body>
</html>'''


def write(content, file_path):
    '''写入txt文本内容'''
    path, file_name = os.path.split(file_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    with open(file_path, 'w') as f:
        f.write(content)
        f.close()


def read(file_path) -> str:
    '''读取txt文本内容'''
    content = None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            f.close()
    except Exception as e:
        print(e)
    return content


def write_json(content, file_path):
    '''写入json'''
    path, file_name = os.path.split(file_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    with open(file_path, 'w') as f:
        json.dump(content, f, ensure_ascii=False)
        f.close()


def read_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        json_file.close()
    return data


class Config(object):
    """
    配置文件的单例类
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.join(parent_dir, 'config.ini')
        self.conf = configparser.ConfigParser()
        self.conf.read(conf_path, encoding="utf-8")

    @classmethod
    def instance(cls, *args, **kwargs):
        with Config._instance_lock:
            if not hasattr(Config, "_instance"):
                Config._instance = Config(*args, **kwargs)
        return Config._instance

    def get_site_title(self):
        return self.conf.get("site", "title")

    def get_site_icon(self):
        return self.conf.get("site", "icon")

    def get_user_avatar(self):
        return self.conf.get("user", "avatar")

    def get_user_avatar_href(self):
        return self.conf.get("user", "avatar_href")

    def get_user_name(self):
        return self.conf.get("user", "name")

    def get_user_desc(self):
        return self.conf.get("user", "desc")

    def get_user_location(self):
        return self.conf.get("user", "location")

    def get_menu_path(self):
        return self.conf.get("menu", "path")

    def get_menu_check_enable(self):
        return self.conf.get("menu", "check_enable")
