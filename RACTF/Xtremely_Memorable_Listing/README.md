# Xtremely Memorable Listing:Web:200pts
Challenge instance ready at 95.216.233.106:37379.  
We've been asked to test a web application, and we suspect there's a file they used to provide to search engines, but we can't remember what it used to be called. Can you have a look and see what you can find?  

# Solution
アクセスするとログインフォームが見える。  
Login  
[site.png](../Entrypoint/site/site.png)  
サーチエンジン用のファイルを見つければいいようだ。  
XMLが問題名なのでsitemap.xmlを見に行く。  
```xml:sitemap.xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://fake.site/</loc>
      <lastmod>2019-12-12</lastmod>
      <changefreq>always</changefreq>
   </url>
   <!--Backup version at sitemap.xml.bak-->
</urlset> 
```
sitemap.xml.bakがあるようなので見に行く。  
```xml:sitemap.xml.bak
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://fake.site/</loc>
      <lastmod>2019-12-12</lastmod>
      <changefreq>always</changefreq>
   </url>
   <url>
      <loc>https://fake.site/_journal.txt</loc>
      <lastmod>2019-12-12</lastmod>
      <changefreq>always</changefreq>
   </url>
</urlset> 
```
_journal.txtがあるようなので見に行くとflagが書かれていた。  

## ractf{4l13n1nv4s1on?}