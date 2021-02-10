BOT_NAME = 'cdp'

SPIDER_MODULES = ['cdp.spiders']
NEWSPIDER_MODULE = 'cdp.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'cdp.pipelines.CdpPipeline': 100,

}