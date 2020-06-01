import scrapy
import warnings
from queuelib import PriorityQueue
from scrapy.utils.misc import load_object, create_instance
from scrapy.utils.deprecate import ScrapyDeprecationWarning
from scrapy.utils.job import job_dir
from scrapy.core.scheduler import Scheduler

# dupefilterにspiderを公開する為の継承
class CustomScheduler(Scheduler):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = create_instance(dupefilter_cls, settings, crawler)
        dupefilter.spider = crawler.spider # dupefilterからspiderを見えるように
        pqclass = load_object(settings['SCHEDULER_PRIORITY_QUEUE'])
        if pqclass is PriorityQueue:
            warnings.warn("SCHEDULER_PRIORITY_QUEUE='queuelib.PriorityQueue'"
                          " is no longer supported because of API changes; "
                          "please use 'scrapy.pqueues.ScrapyPriorityQueue'",
                          ScrapyDeprecationWarning)
            from scrapy.pqueues import ScrapyPriorityQueue
            pqclass = ScrapyPriorityQueue

        dqclass = load_object(settings['SCHEDULER_DISK_QUEUE'])
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        logunser = settings.getbool('SCHEDULER_DEBUG')
        return cls(dupefilter, jobdir=job_dir(settings), logunser=logunser,
                   stats=crawler.stats, pqclass=pqclass, dqclass=dqclass,
                   mqclass=mqclass, crawler=crawler)
