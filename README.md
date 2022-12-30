# 自定义导航网站（customize the navigation site）


## 1、依赖环境 Dependent environment

python3.5+

## 2、配置文件 config file

[config.ini](config.ini)

```text
#简单的配置，自己试一下就知道了。so easy config，just try it by yourself.
# 站点配置模块 site info
[site]
#站点的名称 site title
title=秦城季de站点
#站点的图标 site icon
icon=./resource/favicon.png

#用户相关配置模块  user info
[user]
#左边用户头像 left avatar
avatar=./resource/avatar.webp
avatar_href=https://github.com/xhunmon
name=秦城季
desc=收录或自建站点头像
location=中国·广州

#菜单相关配置  menu info
[menu]
#菜单路径，必须是json格式，否者解析失败  only support json file
path=./resource/nav_menu.json
#使用ping检查站点是否可用，true才会检测，false不检测。会覆盖原json文件，所以备份好。use ping to check every site, and set true to open. but back up  
check_enable=false
``` 

## 3、生成站点  build site file

1）运行[main.py](main.py) 脚本  just run [main.py](main.py)

2）生成网页 output index.html

[index.html](public/index.html)


## 4、体验  test site

[foryoutoy](http://www.foryoutoy.com)


------------------
建议部署到vercel静态网站   It is recommended to deploy to the Vercel static website



