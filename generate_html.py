import feedparser
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# 環境変数からAPIキーを読み込み
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")

def translate_text_with_gemini(text, target_lang="Japanese"):
    """
    Gemini APIを使用してテキストを翻訳します。
    """
    if not text:
        return ""
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Translate the following English text to {target_lang}. Please only provide the translated text.\n\nText: {text}")
        return response.text.strip()
    except Exception as e:
        print(f"翻訳中にエラーが発生しました: {e}")
        return f"[翻訳エラー: {e}]"

def generate_html_from_rss(feed_url):
    """
    指定されたRSSフィードから、翻訳済みのHTMLを生成します。
    """
    feed = feedparser.parse(feed_url)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Databricks Docs Updates</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 20px; color: #37352f; }
            .article { margin-bottom: 30px; padding: 20px; border-left: 4px solid #0070f3; background-color: #f7f7f5; border-radius: 4px; }
            .article-title { font-size: 1.5em; font-weight: 600; margin-bottom: 5px; }
            .translated-label { font-size: 0.8em; color: #999; font-style: italic; margin-top: 10px; }
            .date { font-size: 0.9em; color: #666; margin-bottom: 15px; }
            .content { margin-top: 10px; }
            .original-text, .translated-text { margin-bottom: 10px; }
            .original-text { font-style: normal; }
            .translated-text { font-weight: 400; color: #0070f3; }
            a { text-decoration: none; color: #0070f3; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Databricks Docs Updates</h1>
    """
    
    for entry in feed.entries[:5]:
        title = entry.title
        summary = entry.get("summary", "")
        link = entry.link
        
        translated_title = translate_text_with_gemini(title, target_lang="Japanese")
        translated_summary = translate_text_with_gemini(summary, target_lang="Japanese")

        if hasattr(entry, 'published_parsed'):
            date = datetime(*entry.published_parsed[:6]).strftime("%B %d, %Y")
        else:
            date = "日付不明"
        
        html_content += f"""
        <div class="article">
            <a href="{link}" target="_blank">
                <div class="article-title">{title}</div>
            </a>
            <div class="translated-label">&gt; {translated_title}</div>
            <div class="date">{date}</div>
            <div class="content">
                <div class="original-text">{summary}</div>
                <div class="translated-label">&gt; {translated_summary}</div>
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    rss_url = "https://docs.databricks.com/aws/en/feed.xml"
    html_output = generate_html_from_rss(rss_url)
    
    with open("feed.html", "w", encoding="utf-8") as f:
        f.write(html_output)