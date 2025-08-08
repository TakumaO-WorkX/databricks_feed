import feedparser

def generate_html_from_rss(feed_url):
    """
    指定されたRSSフィードからHTMLを生成します。
    """
    feed = feedparser.parse(feed_url)
    
    html_content = """
    <style>
        body { font-family: sans-serif; padding: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { margin-bottom: 10px; }
        a { color: #0070f3; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    <h2>Databricks Docs Updates</h2>
    <ul>
    """
    
    # 最新5件の記事を処理
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        html_content += f'<li><a href="{link}" target="_blank">{title}</a></li>'
    
    html_content += "</ul>"
    
    return html_content

if __name__ == "__main__":
    rss_url = "https://docs.databricks.com/aws/en/feed.xml"
    html_output = generate_html_from_rss(rss_url)
    
    # 生成したHTMLをファイルに保存
    with open("feed.html", "w", encoding="utf-8") as f:
        f.write(html_output)