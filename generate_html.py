import feedparser
from anthropic import Anthropic
from datetime import datetime
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカルテスト用）
load_dotenv()
anthropic_client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def translate_text_with_claude(text, target_lang="Japanese"):
    """
    Claude APIを使用してテキストを翻訳します。
    """
    if not text:
        return ""
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",  # または別の適切なClaudeモデル
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Translate the following English text to {target_lang}. Please only provide the translated text.\n\nText: {text}"}
            ]
        )
        return response.content[0].text.strip()
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
    
    for entry in feed.entries[:5]: # 最新5件の記事を処理
        title = entry.title
        summary = entry.get("summary", "") # 要約を取得。なければ空文字列
        link = entry.link
        
        translated_title = translate_text_with_claude(title, target_lang="Japanese")
        translated_summary = translate_text_with_claude(summary, target_lang="Japanese")

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