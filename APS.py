from apscheduler.schedulers.blocking import BlockingScheduler
import timer

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    print('This job is run every 30 seconds.')

    timer.time_function()


sched.start()