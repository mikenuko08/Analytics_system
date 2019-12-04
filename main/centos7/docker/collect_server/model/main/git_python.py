# -*- coding: utf-8 -*-
from git import *
import time


def show_blob(b, indent):
    """
    Blobの情報を出力
    """
    print('%s---------------' % (indent))
    print('%shexsha:%s' % (indent, b.hexsha))
    print('%smime_type:%s' % (indent, b.mime_type))
    print('%spath:%s' % (indent, b.path))
    print('%sabspath:%s' % (indent, b.abspath))


def show_tree(tree, indent):
    """
    Treeの情報を出力
    """
    print('%shexsha :%s' % (indent, tree.hexsha))
    print('%spath :%s' % (indent, tree.path))
    print('%sabspath :%s' % (indent, tree.abspath))
    print('%smode :%s' % (indent, tree.mode))
    for t in tree.trees:
        show_tree(t, indent + '  ')

    print('%s[blobs]' % indent)
    for b in tree.blobs:
        show_blob(b, indent + '  ')


def show_commitlog(item):
    """
    Commitの情報を出力
    """
    print("hexsha %s" % item.hexsha)
    print(item.author)
    print(item.author_tz_offset)
    print(time.strftime("%a, %d %b %Y %H:%M", time.gmtime(item.committed_date)))
    print(item.committer)
    print(item.committer_tz_offset)
    print(item.encoding)
    print(item.message)
    print(item.name_rev)
    print(item.summary)


repo = Repo("/root/log/00/file_edit/001/1575431343/git")
for item in repo.iter_commits('master', max_count=100):
    print('================================')
    print(item.hexsha)
    print(item.committed_date)
