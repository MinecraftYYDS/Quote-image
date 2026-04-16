import io
import base64
import urllib.request
from PIL import Image, ImageFont
from pilmoji import Pilmoji
import time
import sys

# Some environments (e.g., IDLE/embedded consoles) lack reconfigure; guard it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")




def gen_quote_img_base64(qq: str, text: str, name: str) -> str:
    """Generate quote image and return base64-encoded PNG."""

    # 字体路径写死（你之后自己填）
    FONT_PATH = "TsukuA.ttc"          # 例如 "/root/fonts/SourceHanSansCN-Regular.otf"
    BASE_IMG_PATH = "quote_base.png"      # 例如 "/root/assets/quote_base.png"

    text = text.replace("\n", " ")

    img_width, img_height = 1200, 640
    font_size = 42
    name_font_size = 24

    font = ImageFont.truetype(FONT_PATH, font_size)
    name_font = ImageFont.truetype(FONT_PATH, name_font_size)
    base_img = Image.open(BASE_IMG_PATH)
    
    # 通过QQ号获取头像图片
    avatar_url = f"http://q2.qlogo.cn/headimg_dl?dst_uin={qq}&spec=5"
    try:
        with urllib.request.urlopen(avatar_url, timeout=10) as response:
            avatar_img = Image.open(io.BytesIO(response.read()))
    except Exception as e:
        print(f"Failed to fetch avatar: {e}")
        # 如果获取失败，使用默认头像
        avatar_img = Image.new("RGBA", (200, 200), (200, 200, 200, 255))
    # 检测头像尺寸，不足 640 则按比例放大
    min_size = 640
    w, h = avatar_img.size

    if w < min_size or h < min_size:
        scale = max(min_size / w, min_size / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        avatar_img = avatar_img.resize((new_w, new_h), Image.LANCZOS)

    # base canvas
    img = Image.new("RGBA", (img_width, img_height), (255, 255, 255, 0))
    img.paste(avatar_img, (0, 0))
    img.paste(base_img, (0, 0), base_img)

    # text layout
    text_list = [text[i:i + 18] for i in range(0, len(text), 18)]
    new_text_height = font_size * len(text_list)
    new_text_width = max(font.getbbox(x)[2] - font.getbbox(x)[0] for x in text_list)
    text_x = 540 + int((560 - new_text_width) / 2)
    text_y = int((img_height - new_text_height) / 2)

    with Pilmoji(img) as pilmoji:
        for i, v in enumerate(text_list):
            pilmoji.text(
                (text_x, text_y + i * font_size),
                text=v,
                font=font,
                align="center",
            )

    # name layout
    left, top, right, bottom = name_font.getbbox(name)
    name_width = right - left
    name_height = bottom - top
    name_x = 600 + int((560 - name_width) / 2)
    name_y = int(img_height - name_height - 20)

    with Pilmoji(img) as pilmoji:
        pilmoji.text(
            (name_x, name_y),
            text=name,
            font=name_font,
            align="center",
        )

    # output as base64
    buffer = io.BytesIO()
    img = img.convert("RGB")
    img.save(buffer, format="PNG")
    buffer.seek(0)
    #保存到本地
    #生成时间戳    
    timestamp = int(time.time())
    with open(f"qtppng/q_{timestamp}.png", "wb") as f:
        f.write(buffer.getvalue())

    return base64.b64encode(buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    import sys
    import json

    qq = sys.argv[1]
    text = sys.argv[2]
    name = sys.argv[3]

    result = gen_quote_img_base64(qq, text, name)
    print(result)

