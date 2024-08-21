# Bilibili_crawler 基于bilibili-api爬取b站动态，视频的评论区

>基于bilibili-api爬取b站动态，视频的评论区。  
动态评论，视频评论均能爬取。  
必须进行去重，爬取评论有重复的。  
制作的比较简陋，希望大家提提意见。  
失效时间未知！  

Froked from：[linyuye/Bilibili_crawler](https://github.com/linyuye/Bilibili_crawler)

**现在使用的API为旧版翻页加载API，使用懒加载API的爬虫还在写。**

**爬取下来的uid和rpid由于数字过长，当你保存时，excel会自动省略掉后面位数/采用科学计数法，导致数据失效，百度一下怎么解决**

# 使用方法
1.安装所需要的库，`pip install -r requirements.txt`  
2.将config.json.example重命名为config.json  
3.在你自己的浏览器中打开B站任意一个视频或者动态，按F12打开开发者工具，等待某个视频/动态加载完全，点击Network选项，向下滑动评论区，直到加载出一个main?oid开头的东西，复制其中的cookie的全部内容，粘贴到config.json的cookies_str后面。  
4.将你需要爬取的视频/动态的链接中的BV号/动态id(链接中的那一串数字)粘贴到config.json的BV后面。  
5.对应你想要保存的文件夹，修改json内容（file1：主评论；file2：子评论；file3：全部评论）  
6.运行`python Bilibili_crawler.py`
