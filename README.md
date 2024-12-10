# Bilibili_crawler 基于bilibili-api爬取b站动态，视频的评论区

>基于bilibili-api爬取b站动态，视频的评论区。  
动态评论，视频评论均能爬取。  
必须进行去重，爬取评论有重复的。  
制作的比较简陋，希望大家提提意见。  
失效时间未知！  

Froked from：[linyuye/Bilibili_crawler](https://github.com/linyuye/Bilibili_crawler)

**Bilibili_crawler.py使用旧版懒加载API，Bilibili_crawler_wbi.py使用WBI鉴权的懒加载API，（在B站的某次更新后）这两个文件的翻页方式都有问题**

**Bilibili_crawler_wbi_offset.py适配了新版翻页API，请使用这个文件**

**periodically_get_video_details.py可以持续性统计视频的点赞投币收藏等状态，如有需要请自行修改执行间隔，默认为3分钟抓取一次**

**爬取下来的uid和rpid由于数字过长，当你保存时，excel会自动省略掉后面位数/采用科学计数法，导致数据失效，百度一下怎么解决**

# 使用方法
1.安装所需要的库，`pip install -r requirements.txt`  
2.将`config.json.example`重命名为`config.json ` 
3.在你自己的浏览器中打开B站任意一个视频或者动态，按F12打开开发者工具，等待某个视频/动态加载完全，点击Network选项，向下滑动评论区，直到加载出一个main?oid开头的东西，复制其中的cookie的全部内容，粘贴到`config.json`的cookies_str后面。  
4.将你需要爬取的视频/动态的链接中的BV号/动态id(链接中的那一串数字)粘贴到config.json的BV后面。  
5.评论文件的默认保存路径为/comments，可以自行修改config.json中的 "output_path" 。    
6.运行`python Bilibili_crawler_wbi_offset.py`
