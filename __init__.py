# -*- coding: utf-8 -*-

from tgspiders.lib.sch import JobScheduler
from tgspiders.jobs import init_jobs
from tgspiders.lib.log import Log

__version__ = '0.0.2'


def main():
    Log().logger.info('Spiders started, Press Ctrl + C to exit')
    init_jobs()
    JobScheduler().scheduler.start()


if __name__ == '__main__':
    main()