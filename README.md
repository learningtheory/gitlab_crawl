# 使用方式

查看cookie 到cookie处修改
![image](https://github.com/learningtheory/gitlab_crawl/blob/feat_init/images/WechatIMG12.png)

```
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── images
│   └── WechatIMG12.png
├── main.py
└── scan_group
    ├── __init__.py  修改此处cookie
    ├── constant.py  修改gitlab域名
    └── git_lab.py



python version > 3.0

# 按照环境
pipenv install

# 进入环境
pipenv shell 

# 执行主程序
python main.py



```

# 背景
```
特征工程优化重构，对一些特征进行增减，但是这些裁剪的特征，对总体项目的影响。

需要将涉及的项目都拉取出来进行 grep "特征名字" ./ -r -n 定位影响的项目，对有影响的进行修正
```

# 功能

```
下载个人所属的所在组的所有项目，供检索关键词使用
```