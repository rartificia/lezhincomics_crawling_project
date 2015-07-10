# -*- coding: utf-8 -*-
import urllib2
import os
import sys
import time
import datetime
import re

COMICS_NAME = sys.argv[1]
ACCESS_TOKEN = sys.argv[2]



def get_episodes_info():
	page_cut_list = []
	page_id_list = []

	json = open("%s.json"%(COMICS_NAME), 'r')
	line = json.readline() 
	content_list = line.split(",{")
	max_range = len(content_list)

	for i in range(0, max_range):
		page_id_list.append(content_list[i].split(",")[3][8:-1])
		page_cut_list.append(content_list[i].split(",")[11][6:])
	return {'id':page_id_list, 'cut':page_cut_list}

def get_image_links():
	info = get_episodes_info()
	cut_list = info['cut']
	id_list = info['id']
	max_range = len(cut_list)

	for episodes in range(0,max_range):
		img_list=[]
		for img in range(1, int(cut_list[episodes])+1):
			url = "http://2cdn.lezhin.com/episodes/%s/%s/contents/%d?access_token=%s" %(COMICS_NAME, id_list[episodes], img, ACCESS_TOKEN)
			img_list.append(url)
		print img_list
		download_images(id_list[episodes], img_list)


def download_images(title, img_list):
    inittime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    print "Downloading images..."
    for link in img_list:
        os.system('wget --content-disposition "%s" -P "%s/"'%(link,inittime))
    print "Image Downloading Complete."
    print "%d images fetched."%(len(img_list))
    os.system('mv "%s/" "%s/"'%(inittime, title))
    os.system('7z a "%s.zip" "%s/"'%(title, title))
    print "File zip archiving completed."
    os.system('rm -r "%s/"'%(title))
    print "Temporal folder erased."
    print "Done!"

get_image_links()
