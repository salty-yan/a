"""并发下载经典 Rider-Waite-Smith 塔罗牌图片"""
import urllib.request, json, os, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

MAJOR = ['Fool','Magician','High_Priestess','Empress','Emperor',
         'Hierophant','Lovers','Chariot','Strength','Hermit',
         'Wheel_of_Fortune','Justice','Hanged_Man','Death','Temperance',
         'Devil','Tower','Star','Moon','Sun','Judgement','World']
SUITS = ['Wands','Cups','Swords','Pentacles']
RANKS = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14']

os.makedirs('assets/cards', exist_ok=True)

def download_one(cid):
    if 0 <= cid <= 21:
        fname = f'RWS_Tarot_{cid:02d}_{MAJOR[cid]}.jpg'
    else:
        lid = cid - 22
        fname = f'{SUITS[lid//14]}{RANKS[lid%14]}.jpg'
    
    out = f'assets/cards/{cid}.png'
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        return cid, True, "exists"
    
    # Step 1: get image URL from Wikimedia API
    api = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:{urllib.request.quote(fname)}&prop=imageinfo&iiprop=url"
    try:
        req = urllib.request.Request(api, headers={'User-Agent': 'TarotInsight/1.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            data = json.loads(r.read())
        url = None
        for p in data.get('query', {}).get('pages', {}).values():
            ii = p.get('imageinfo', [])
            if ii:
                url = ii[0]['url']
                break
        if not url:
            return cid, False, "no_url"
    except Exception as e:
        return cid, False, f"api_err:{e}"
    
    # Step 2: download image
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TarotInsight/1.0'})
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            img = Image.open(BytesIO(r.read()))
            img.save(out, 'PNG', optimize=True)
            return cid, True, f"{img.size[0]}x{img.size[1]}"
    except Exception as e:
        return cid, False, f"dl_err:{e}"

if __name__ == '__main__':
    total = 78
    ok = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(download_one, cid): cid for cid in range(total)}
        for f in as_completed(futures):
            cid, success, info = f.result()
            status = "OK" if success else "FAIL"
            print(f"[{cid+1:2d}/78] {status} {info}")
            if success:
                ok += 1
    print(f"\nDone: {ok}/{total}")
