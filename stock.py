import urllib.request
import json
import time

def get_content(url):
  try:
    opener = urllib.request.urlopen(url, timeout=10)
    all = opener.read()
    all = str(all.decode("gb2312", "ignore"))

    file_name = time.strftime("%Y-%m-%d", time.localtime())
    f = open(file_name + ".txt", mode='w')
    f.write(all)
    f.close()
  except Exception as e:
    print(e)

def main():
  url = 'http://quote.tool.hexun.com/hqzx/quote.aspx?type=2&market=0&sorttype=3&updown=up&page=1&count=5000&time=160000'

  while True:
    week = int(time.strftime("%w"))
    hour = int(time.strftime("%H"))

    if week >= 6:
      time.sleep(60*60*24)
    elif hour == 16:
      get_content(url)
    else:
      time.sleep(30*60)

if __name__ == '__main__':
  main()