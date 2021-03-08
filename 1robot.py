#https://www.alibabacloud.com/blog/develop-a-cart-application-with-django_594697
#https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react

import requests
import bs4
import random
import time
import re
from urllib.parse import urlparse
import psycopg2
from langdetect import detect


try:
 try:
  error_403 = []
  db_urls = ['bbb.org']


#urls from the original database
 


  conn = psycopg2.connect(
  host="localhost", port = 5432, database="nairobi", user="nairobiuser",     password="machayoephraimmokamba")

  cur = conn.cursor()

  cur.execute("""SELECT urls FROM naserian_universal""")
  db_ur = cur.fetchall()

  cur.execute("SELECT urls FROM naserian_universal1")
  db_ur1 = cur.fetchall()

  cur.execute("""SELECT rawurl FROM  naserian_raw """)
  db_url = cur.fetchall()
  
  cur.close()
  conn.close()


  db_us = db_ur + db_url + db_ur1
  db_urls = [item for t in db_us for item in t]
  


  all_urls =[]
  all_href =[]

  found_links = []
  found_proc = []

#getting urls from the second database and deleting them
  conn = psycopg2.connect(
  host="localhost", port = 5432, database="nairobi", user="nairobiuser",     password="machayoephraimmokamba")

  cur = conn.cursor()

  cur.execute("""SELECT * FROM  naserian_raw """)
  all_urs = cur.fetchall()


  all_us = []
  all_us = [item for t in all_urs for item in t]

  all_urls= [x for x in all_us if not isinstance(x,int)]
  time.sleep(5)

  new_all = []
  
  i = 1
  while i <= 75:
   q1 = random.choice(all_urls)
   q2 = all_urls.remove(q1)
   new_all.append(q1)

   cur.execute("DELETE FROM naserian_raw WHERE naserian_raw.rawurl = %s",(q1,))
   conn.commit()
   i += 1

  cur.close()
  conn.close()
#starting the while loop that loops according to the number of objects in all_urls 
  i = len(new_all)
  while i != 0:
   try:

    url2 = random.choice(new_all)
    shown = url2[8:]
    print(shown)
    new_all.remove(url2)
     
    req = requests.get(url2) 
    print(req.status_code)

#getting the content of the visited site
    if req.status_code == 200:

     srch = shown
     cont = req.content
     soup = bs4.BeautifulSoup(cont,'lxml')
     srch = soup.title.text
     meta = soup.find_all('meta')
     for tag in meta:
      if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
       search_results = srch
       search_results = tag.attrs['content']
    else:  
     pass 

    if len(search_results) == 0 or search_results is False:
     search_results = srch
    
    



   except Exception as arr:
    print(arr)
    print('in 1') 
    
#saving the visited urls to the database

   else:
    print(search_results)
    if search_results:
     lang = detect(search_results)
     print(lang)
    print('OK in 1')

    try:
     conn = psycopg2.connect(
     host="localhost", port = 5432, database="nairobi", user="nairobiuser",      password="machayoephraimmokamba")

     cur = conn.cursor()

     cur.execute("""SELECT numb FROM naserian_ephu""")
     db_ur = cur.fetchone()

     D = []
     for t in db_ur:
      D.append(t)

     b = D[0]

     cur.execute("DELETE FROM naserian_ephu WHERE naserian_ephu.numb = %s",(b,))
     conn.commit()
     print(b)
     
     cur.execute("INSERT INTO naserian_universal1 VALUES (%s,%s,%s,%s)", (b, url2 , search_results, shown))
     conn.commit()

    except Exception as arrr:
     cur.close()
     conn.close()
     print(arrr)
     print('in 1')

    else:
     srch = ''
     

     print('saved')

     


#getting all the urls that lead to the other pages on the internet
    all_lang = ['zh-cn','vi','ko','et','ja','de','ar','fr','no','sv','es','fr','so','tr','sv','te','th','id','fa','sl','bg','ca']
    if lang not in all_lang:
     if 'porn' not in search_results:
      if 'gay' not in search_results:
       if 'WN Network' not in search_results:
        if 'Porn' not in search_results:
         if 'Sex' not in search_results:
          cont = req.content
          soup = bs4.BeautifulSoup(cont,'html.parser')
          for link in soup.find_all('a',href = True):
           href =link.attrs.get('href')


#PROCESSING THE FOUND URLS

#HTTP and HTTPS puzzle
           process = urlparse(href)
           proced = process.scheme
           if proced == 'https':
            all_href.append(href)
           elif proced == 'http':
            href = proced + 's'+ '://' + process.netloc
            all_href.append(href)
           else:
            pass

     
#removing www from each link and ensuring its base url is not the one we crawled
          for new_link in all_href:
           re_word = re.sub('www.','',new_link)
           urefu = len(url2)
           new_word = re_word[:urefu]


#making the links base_urls
           proc_word = re_word
           data = proc_word 
           parsed_data = urlparse(data)
           formated = parsed_data.scheme + '://' + parsed_data.netloc

#finding the new uncrawled links and adding them to the list of words to be crawled  
           if url2 != new_word and formated not in all_urls:
            found_links.append(formated)
     
          for v in found_links:
           if v not in found_proc: 
            found_proc.append(v)
     #print('all links')
     #print(found_proc)
    
          doms_wanted = ['.com','.org','.net']

          for lnks in found_proc:

           if lnks not in db_urls:

      
            l1 = urlparse(lnks)
            l2 =  l1.netloc[0:-7:].split('.')
            if len(l2) < 2:
       #print('')
       #print('link not in database')
       #print(lnks)
             if lnks[-4:] in doms_wanted:
              lnk = []
              lnk.append(lnks)
        #print('')
        #print('approaved links')
         
              print(lnks)    
              ids = []
              for j in lnk:
               cur.execute("""SELECT rawnumb FROM naserian_mac""")
               db_ur = cur.fetchone()

               D = []
               for t in db_ur:
                D.append(t)

                b = D[0]

                cur.execute("DELETE FROM naserian_mac WHERE naserian_mac.rawnumb = %s",(b,))
                conn.commit()
         
                cur.execute("INSERT INTO naserian_raw VALUES (%s,%s)", (b, lnks))
                conn.commit()
         else:
          print('witty')
        else:
         print('witty')
       else:
        print('witty')
      else:
       print('witty')
     else:
      print('witty')
    else:
     print('diff language')

   finally: 
    cur.close()
    conn.close() 
    search_results = '' 
    all_href.clear()
    found_links.clear()   
    found_proc.clear()
    print(int(i) - 1)    

    i -= 1
    print('')
    print('continuing......./')
    print('')
    time.sleep(5)
     


 except Exception as err:
  print(err)
 
 else:
  print('ok in 2')

except Exception as er:
 print(er)

else:
 print('ok in 3')

finally:
 print('done..')




####what do you want to do on the internet??????????????????





















