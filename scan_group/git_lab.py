import subprocess, os
from subprocess import Popen

from scan_group import session
from pyquery import PyQuery as pq

from scan_group.constant import GITLAB_GROUP_INDEX, PROJECT_INDEX


class GroupCrawl:
    # 所属组首页
    index_url = GITLAB_GROUP_INDEX

    @classmethod
    def get_group_list(cls):
        """
        读取所属组
        :return:
        """
        rq = session.get(cls.index_url)
        if rq.status_code == 200:
            jquery_txt = pq(rq.text)
            group_urls = []
            group_names = jquery_txt('.group-name')
            for i in group_names:
                group_urls.append(pq(i).attr('href'))
            return set(group_urls)
        else:
            raise Exception(f'GroupCrawl get_group_list status {rq.status_code}')


class ProjectCrawl:
    # 组首页
    index_url = PROJECT_INDEX

    @classmethod
    def get_project_list(cls, group_name):
        """
        读取所属组的所有项目
        :return:
        """
        pg_names = []
        rq = session.get(cls.index_url.format(group_name))
        if rq.status_code == 200:
            jquery_txt = pq(rq.text)
            project_names = jquery_txt('.project-full-name')
            for i in project_names:
                pg_names.append(pq(i).text().replace(' / ', '/'))
            return pg_names
        else:
            print(f'ProjectCrawl ProjectCrawl status {rq.status_code}')


class ScriptExec:
    """
    脚本执行
    """
    # 切换目录并下载代码
    web_shell = 'cd {} && git clone {}'

    # 更新已存在的所有分支的代码
    web_fetch = 'cd {} && git fetch && git pull --all'
    curl = 'cd {} && curl -O {}'

    @staticmethod
    def down_zip_file_script(http_git, dir):
        """
        下载某代码到某个目录下
        :param http_git:
        :param dir:
        :return:
        """
        proc = Popen(args=[ScriptExec.curl.format(dir, http_git)], shell=True, stdout=subprocess.PIPE)
        return http_git, proc.stdout.read().decode('utf-8').split('\n')[:-1]

    @staticmethod
    def down_source_script(http_git, dir):
        """
        下载某代码到某个目录下
        :param http_git:
        :param dir:
        :return:
        """
        proc = Popen(args=[ScriptExec.web_shell.format(dir, http_git)], shell=True, stdout=subprocess.PIPE)
        return http_git, proc.stdout.read().decode('utf-8').split('\n')[:-1]

    @staticmethod
    def update_source_script(dir):
        """
        更新代码
        :param dir:
        :return:
        """
        proc = Popen(args=[ScriptExec.web_fetch.format(dir)], shell=True, stdout=subprocess.PIPE)
        return dir, proc.stdout.read().decode('utf-8').split('\n')[:-1]


class GitLabSource:

    @classmethod
    def down(cls, http_git):
        """
        下载git clone {} 或者更新
        :param http_git:
        :return:
        """
        split_name = http_git.split('/')
        source_group = split_name[-2]
        source_project_name = split_name[-1][:-4]
        path = os.path.join(os.getcwd(), source_group)
        abs_path = os.path.join(path, source_project_name)

        if os.path.exists(abs_path):
            # 更新改项目的代码
            sts = ScriptExec.update_source_script(abs_path)
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            sts = ScriptExec.down_source_script(http_git, path)
        print(sts)

    @classmethod
    def down_file(cls, http_git: str):
        """
        下载git clone {} 或者更新
        https://domin/group/view.git
        https://domin/group/view/repository/archive.zip
        :param http_git:
        :return:
        """

        http_git = http_git.replace('.git', '/repository/archive.zip')
        split = http_git.split('/')
        name = f"{split[-3]}.zip"

        path = os.path.join(os.getcwd(), split[-4])
        if not os.path.exists(path):
            os.makedirs(path)

        p = os.path.join(path, name)
        if os.path.exists(p):
            print('exit file ', name)
            return

        rs = session.get(http_git)
        with open(p, 'wb') as file:
            file.write(rs.content)
            print(name, 'ok')

    @classmethod
    def update(cls, dir):
        """
        更新所在目录的所有代码
        :param dir:
        :return:
        """
        if not os.path.exists(dir):
            return '目录不存在'
        dirs = os.listdir(dir)
        for i in dirs:
            path = os.path.join(dir, i)
            if os.path.isdir(path) and not i.startswith('.'):
                print(ScriptExec.update_source_script(path))
