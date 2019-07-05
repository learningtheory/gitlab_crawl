from scan_group.git_lab import GroupCrawl, ProjectCrawl, GitLabSource
from scan_group.constant import GITLAB_INDEX

if __name__ == '__main__':

    # 获取组
    group_names = GroupCrawl.get_group_list()
    git_list = []
    for group in group_names:
        # 获取组下的可见项目
        project_list = ProjectCrawl.get_project_list(group_name=group)
        for p in project_list:
            git_list.append(f'{GITLAB_INDEX}/{p}.git')

    # 总项目数
    print(len(git_list))

    # print(git_list)

    from multiprocessing.pool import Pool

    pool = Pool(10)
    # 多线程执行

    # 下载文件zip，无需其他配置
    pool.map(GitLabSource.down_file, [i for i in git_list])

    # 下载源码，需要本地配置本人的git配置 若是https的配置 无需修改域名 GITLAB_INDEX，若是 git的配置需要修改下
    # pool.map(GitLabSource.down, [i for i in git_list])
