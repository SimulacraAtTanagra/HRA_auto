# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:39:08 2020

@author: shane
"""

"""For automated actions in HR-Assist"""

from src.seltools import mydriver, main
from time import sleep
from src.admin import newest,colclean
import pandas as pd

class hra(mydriver, main):
    def __init__(self,download_dir):
        self.download_dir=download_dir
        self.driver=self.setupbrowser()
        
    loginurl="https://sota.york.cuny.edu/HrAssist/HrLogon.aspx"
    unfield="ctl00_ContentPlaceHolder1_txtLoginID"
    pwfield="ctl00_ContentPlaceHolder1_txtPwd"
    submit="ctl00_ContentPlaceHolder1_ButContinue"
    un=USERNAME
    pw=PASSWORD
    
    def login(self):    #consider moving this to seltools and usising data_dist
        self.driver.get(self.loginurl)
        self.waitfillid(self.unfield,self.un)
        self.waitfillid(self.pwfield,self.pw)
        self.main_window = self.driver.current_window_handle
        self.waitid(self.submit)
        
class payroll(main):
    def __init__(self,driver):
        self.driver=driver
        if 'ctl00_ContentPlaceHolder1_LinkButton3' in driver.page_source:
            self.waitid('ctl00_ContentPlaceHolder1_LinkButton3')
        else:
            self.nav(0)
            self.waitid('ctl00_ContentPlaceHolder1_LinkButton3')
    def nav(self,num):
        self.waitlink(self.menu[num])
    menu=['Home','Employee Information','Daily Transactions',
          'Timesheet Entry Control','Leave Requests','Year-End Processing',
          'Reports','Logoff']
    def search(self,emplid):
        self.waitfillid('ctl00_ContentPlaceHolder1_txtID',emplid)
        self.waitid("ctl00_ContentPlaceHolder1_lnkSearch")
        sleep(1)
        self.waitlink('Select')
    def tablesearch(self,emplid):
        self.waitfillid('ctl00_ContentPlaceHolder1_txtID',emplid)
        self.waitid("ctl00_ContentPlaceHolder1_lbSearch")
        return(self.grab_table("ctl00_ContentPlaceHolder1_grdHRTS" ))
    def modify_emp(self):
        self.waitid('ctl00_ContentPlaceHolder1_butModify')
    def refresh_field(self,fieldid):
        x=self.dropdownitembyid(fieldid)
        self.dropdownselector(fieldid,'')
        self.dropdownselector(fieldid,x)
    def refresh_rate(self):
        self.waitid('ctl00_ContentPlaceHolder1_butRate')
    def save(self):
        self.waitid('ctl00_ContentPlaceHolder1_butSave')
    def refresh_and_go(self,emplid):
        self.nav(1)
        self.search(emplid)
        self.modify_emp()
        self.refresh_rate()
        self.save()
        sleep(1)
        self.nav(1)
    def missing_ts(self,emplid):
        self.nav(3)
        self.waitlink('Review Timesheets')
        this=self.tablesearch(emplid)
        current=[i.text for i in this if i.text.isdigit() and emplid not in i.text]
        self.nav(3)
        self.waitlink("Review Posted Timesheets")
        this=self.tablesearch(emplid)
        posted=[i.text for i in this if i.text.isdigit() and emplid not in i.text]
        posted.extend(current)
        final=list(set([str(i) for i in range(14,22)])-set(posted))
        return((emplid,final))
    def scrape_posted(self):
        self.nav(3)
        self.waitlink("Review Posted Timesheets")
        num=2
        pagelist=[]
        posted=[]
        while True:
            try:
                this=self.grab_table("ctl00_ContentPlaceHolder1_grdHRTS")
                posted=[i.text for i in this]
                pagelist.extend(posted)
                newpage=f"javascript:__doPostBack('ctl00$ContentPlaceHolder1$grdHRTS','Page${num}')"
                num+=1
                self.driver.execute_script(newpage)
                posted=[]
            except:
                break
                return(pagelist)
        return(pagelist)

if __name__ == "__main__":
    download_dir="C:\\Users\\shane\\desktop\\records"
    home=hra(download_dir)
    home.login()
    pr=payroll((home.driver))
    
    #this=pr.scrape_posted()
