from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import math
import sys


# Check whether browser control is succeeded or not
def isSucceed(start, end):
    if start == end:
        return False
    else:
        return True


# Sign in
def signIn(user="root", password="r00t"):
    driver.get(giturl+'signout')
    driver.get(giturl+"signin?redirect=%2F")
    stitle = driver.title
    print(stitle, flush=True)
    entry = driver.find_element_by_id("userName")
    entry.send_keys(user)
    entry = driver.find_element_by_id("password")
    entry.send_keys(password)
    btn = driver.find_element_by_class_name('btn-success')
    btn.click()
    # driver.implicitly_wait(0.5)
    time.sleep(1)
    if isSucceed(stitle, driver.title) == False:
        sys.exit()
    print(user+" signIn:"+str(isSucceed(stitle, driver.title)), flush=True)


# Create repository (requires signIn)
def createRepo(reponame, isPublic=False):
    driver.get(giturl+'new')
    repotitle = driver.title
    print(repotitle, flush=True)
    entRepo = driver.find_element_by_id("name")
    entRepo.send_keys(reponame)

    if isPublic == True:
        # public
        entRepoRadio = driver.find_element_by_xpath(
            '//*[@id="form"]/fieldset[3]/label[1]/input')
    else:
        # private
        entRepoRadio = driver.find_element_by_xpath(
            '//*[@id="form"]/fieldset[3]/label[2]/input')
    entRepoRadio.click()
    entRepoBtn = driver.find_element_by_xpath(
        '//*[@id="form"]/fieldset[5]/input')
    entRepoBtn.click()
    time.sleep(1)
    print(isSucceed(repotitle, driver.title), flush=True)


# add Collaborator (requires signIn(root,root) or signIn(name,pass))
def addCollaborator(name, repo, collaborator):
    driver.get(giturl + str(name) + '/' +
               str(repo) + '/settings/collaborators')
    atitle = driver.title
    print(atitle, flush=True)
    entry = driver.find_element_by_id("userName-collaborator")
    entry.send_keys(collaborator)
    driver.find_element_by_id("addCollaborator").click()
    driver.find_element_by_xpath(
        '//*[@id="form"]/div[3]/input[2]').click()  # apply Changes
    time.sleep(0.5)


# setup repository(createRepo and addCollaborator)
# deprecate
def setupRepo(username, password, reponame, repoIsPublic, collaborator):
    signIn(username, password)
    createRepo(reponame, repoIsPublic)
    addCollaborator(username, reponame, collaborator)


# setup multiple repositories by file
# if index is specified, signIn process is executed after index.
def setupReposByFile(csv, index=0):
    df = pd.read_csv(csv)
    for i, row in df.iterrows():
        if i < index:
            continue
        print(i, flush=True)
        signIn(row['username'], row['password'])
        createRepo(row['reponame'], row['repoIsPublic'])


giturl = 'http://gitbucket:8080/'
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(
    executable_path='/usr/local/bin/geckodriver', options=options)


def main(args):
    # If signIn is terminated, add index value as argv(ex. python createUandR.py 5)
    if len(args) == 1:
        index = 0
    elif len(args) == 2:
        index = int(args[1])
    setupReposByFile('makeRepos.csv', index)

    #df = pd.read_csv('makeRepos.csv')
    # for i,row in df.iterrows():
    # print(i,flush=True)
    # if len(args) == 1 or i >= int(args[1]):
    # signIn(row['username'],row['password'])

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main(sys.argv)
