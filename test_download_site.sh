
QT_QPA_PLATFORM=offscreen phantomjs resources/get_redirection_url_phantomjs.js http://www.google.com
wget -kEpnp -l 1 --max-redirect=100 -e robots=off -P temp_wget --user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" http://www.google.com


#new approach -> get all resources
phantomjs save_page.js http://example.com >> page.html#
