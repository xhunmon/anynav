# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from utils import *
import sys
import os
import shutil


def check_config_init():
    print('站点配置信息.......................')
    print('站点标题：', Config().get_site_title())
    if not os.path.exists(Config().get_site_icon()):
        raise RuntimeError('站点图标不存在！')
    print('用户配置信息.......................')
    if not os.path.exists(Config().get_user_avatar()):
        raise RuntimeError('用户头像不存在！')
    print('点击用户头像链接：', Config().get_user_avatar_href())
    print('用户名称：', Config().get_user_name())
    print('用户描述：', Config().get_user_desc())
    print('用户位置：', Config().get_user_location())
    print('菜单配置信息.......................')
    if not os.path.exists(Config().get_menu_path()):
        raise RuntimeError('菜单文件不存在！')
    print('开启菜单检查？', Config().get_menu_check_enable())


def check_enable_site(menu_path):
    new_boxs = []
    menus = read_json(menu_path)
    boxs = menus['boxs']
    for box in boxs:
        box_name = box['name']
        new_tags = []
        new_box = {'name': box_name, 'tags': new_tags}
        new_boxs.append(new_box)
        tags = box['tags']
        for tag in tags:
            title = tag['title']
            url = tag['url']
            desc = tag['desc']
            if not site_ping(url):  # 不检查网站是否可用
                continue
            new_tag = {'title': title, 'url': url, 'desc': desc}
            new_tags.append(new_tag)
    new_json = {'boxs': new_boxs}
    print(new_json)
    write_json(new_json, menu_path)


if __name__ == '__main__':
    check_config_init()
    print('解析配置文件完毕......')
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(cur_dir, 'public')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    # 复制静态资源css等
    shutil.copytree(os.path.join(os.path.join(cur_dir, 'resource'), 'static'), os.path.join(target_dir, 'static'))
    site_title = Config().get_site_title()
    site_icon = Config().get_site_icon()
    user_avatar = Config().get_user_avatar()
    avatar_href = Config().get_user_avatar_href()
    user_name = Config().get_user_name()
    user_desc = Config().get_user_desc()
    user_location = Config().get_user_location()
    isCheck = Config().get_menu_check_enable()
    # 复制图片
    site_path = 'site_img' + os.path.splitext(site_icon)[-1]
    shutil.copyfile(site_icon, os.path.join(target_dir, site_path))
    avatar_path = 'avatar_img' + os.path.splitext(user_avatar)[-1]
    shutil.copyfile(user_avatar, os.path.join(target_dir, avatar_path))
    pages = []
    index_html = os.path.join(target_dir, 'index.html')
    pages.append(append_head(site_title, site_path, avatar_path, avatar_href, user_name, user_desc, user_location))
    menu_path = Config().get_menu_path()
    # 检查是否目标站点是否可用
    if isCheck == 'true':
        check_enable_site(menu_path)
    menus = read_json(menu_path)
    boxs = menus['boxs']
    # 输入
    for box_i in range(0, len(boxs)):
        box = boxs[box_i]
        if box_i < 10:
            pre_index = '0{}'.format(box_i)
        else:
            pre_index = '{}'.format(box_i)
        if box_i == 0:
            box_li = '''<li><a href="./#{}" class="active">{}-{}</a></li>'''.format(pre_index, pre_index, box['name'])
        else:
            box_li = '''<li><a href="./#{}">{}-{}</a></li>'''.format(pre_index, pre_index, box['name'])
        pages.append(box_li)
    box_li_end = '''
    </ul>
        </nav>
    </aside>
    <section class="main">
        <div id="mainContent">
    '''
    pages.append(box_li_end)
    for box_i in range(0, len(boxs)):
        box = boxs[box_i]
        if box_i < 10:
            pre_index = '0{}'.format(box_i)
        else:
            pre_index = '{}'.format(box_i)
        # box的开头
        pages.append('''<div class="box">
            <a href="./#{}" name="{}"></a>
            <div class="sub-category">
                <div>{}</div>
            </div>
            <div class="tag">'''.format(pre_index, pre_index, box['name']))
        tags = box['tags']
        for tag in tags:
            # 每一个跳转的条目
            pages.append(''' <a target="_blank" href="{}">
                <div class="item">
                    <div class="logo">
                        {}
                    </div>
                    <div class="desc">
                        {}
                    </div>
                </div>
            </a>'''.format(tag['url'], tag['title'], tag['desc']))
        # box的闭合
        pages.append('''    </div>
                            </div>''')

    # 最后结尾
    pages.append(get_tail())
    with open(index_html, mode='a', encoding="utf-8") as f:
        for page in pages:
            f.write(page + '\n')
        f.close()
