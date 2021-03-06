# Scrapy settings for dianping project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dianping'

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'iamspider (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'dianping.spiders.rotateAgent.RotateUserAgentMiddleware' :400
    }
# SPIDER_MIDDLEWARES = {}

ITEM_PIPELINES = {'dianping.pipelines.DianpingPipeline': 1}
DOWNLOAD_DELAY = 0.50 #250ms
COOKIES_ENABLED = False
# DepthMiddleware.  The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
DEPTH_LIMIT = 2  #just spider clothes
HTTPERROR_ALLOWED_CODES=[403] #spider was forbidden
CRAWLSPIDER_FOLLOW_LINKS=True