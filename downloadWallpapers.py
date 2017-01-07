import bs4,sys,requests,os,webbrowser,ctypes,random

#ask the user about which type of wallpaper

baseUrl = "http://www.hdwallpapers.in"
def topWallpapers():
  pageCount = 1
  dirName = "Top_wallpapers"

  if not os.path.exists(dirName):
    os.makedirs(dirName)

  #now time to kickin the req module
  while pageCount <= 1:
    url = "http://www.hdwallpapers.in/top_download_wallpapers/page/"+str(pageCount)

    htmllayout = requests.get(url)
    htmllayout.raise_for_status()

    #kickin beautiful soup
    soupper = bs4.BeautifulSoup(htmllayout.text,"html.parser")

    #its not possible to get the src of the image because its been wrapped into the img tags
    #so go form .thumb to a then to img
    thumbElem = soupper.select(".thumb a img")
    for imgIter in thumbElem:

      #next is to save check the url
      imgUrl = baseUrl+imgIter.get("src")

      imgBase =  os.path.basename(imgUrl)
      print "Downloading %s" %imgBase

      imageFile = open(os.path.join(dirName,imgBase),"wb")

      res = requests.get(imgUrl)
      res.raise_for_status()

      for chunk in res.iter_content(10000):
        imageFile.write(chunk)

    pageCount = pageCount+1
    print "Downloading page %s" %pageCount

  filename = random.choice(os.listdir("C:\Python27\scarpers\\"+dirName))

  SPI_SETDESKWALLPAPER = 20 # According to http://support.microsoft.com/default.aspx?scid=97142

  ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "C:\Python27\scarpers\\"+dirName+"\\"+filename, 120)
  print "%s has been set as the wallpaper" %filename
  imageFile.close()

def searchWallpapers(queryName):
  pageCount = 1

  dirName = queryName
  if not os.path.exists(dirName):
    os.makedirs(dirName)

  while pageCount <= 1:
    url ="http://www.hdwallpapers.in/search/page/"+str(pageCount)+"?q="+queryName

    htmllayout = requests.get(url)
    htmllayout.raise_for_status()

    #kickin beautiful soup
    soupper = bs4.BeautifulSoup(htmllayout.text,"html.parser")

    #its not possible to get the src of the image because its been wrapped into the img tags
    #so go form .thumb to a then to img
    thumbElem = soupper.select(".thumb a img")
    if len(thumbElem) < 2:
      print "There are only %s number of pages" %int(pageCount)-1
      sys.exit()
    else:
      for imgIter in thumbElem:

        #next is to save check the url
        imgUrl = baseUrl+imgIter.get("src")

        imgBase =  os.path.basename(imgUrl)
        print "Downloading %s" %imgBase

        imageFile = open(os.path.join(dirName,imgBase),"wb")

        res = requests.get(imgUrl)
        res.raise_for_status()

        for chunk in res.iter_content(10000):
          imageFile.write(chunk)

      pageCount = pageCount+1
      print "Downloading page %s" %pageCount

    filename = random.choice(os.listdir("C:\Python27\scarpers\\"+dirName))

    SPI_SETDESKWALLPAPER = 20 # According to http://support.microsoft.com/default.aspx?scid=97142

    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "C:\Python27\scarpers\\"+dirName+"\\"+filename, 120)
    print "%s has been set as the wallpaper" %filename
    imageFile.close()

print "Do you want only the top 10 wallpapers or do you want to search"
print "1 for top or press 0 for search"
desc = raw_input(">>")

if desc  == "1":
  print "Downloading the first 10 top wallpapers for you it may take some time"
  topWallpapers()
else:
  print "Enter the wallpaper you want to search"
  query = raw_input(">>")
  print "downloading the %s wallapers" %query
  searchWallpapers(query)

