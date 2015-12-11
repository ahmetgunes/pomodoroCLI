import sched
import time
from optparse import OptionParser
import subprocess
import notify2


def send_message(message):
    notify2.init('Pomodoro')
    nf = notify2.Notification('POMODORO', message)
    nf.set_urgency(notify2.URGENCY_CRITICAL)
    nf.show()


def start_long_break(long_break, short_break, work, cycle_time):
    send_message("Have a nice long break")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(long_break, 1, start_work, argument=(long_break, short_break, work, cycle_time))
    scheduler.run()


def start_short_break(long_break, short_break, work, cycle_time):
    send_message("Have a nice short break")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(short_break, 1, start_work, argument=(long_break, short_break, work, cycle_time))
    scheduler.run()


def start_work(long_break, short_break, work, cycle_time):
    send_message("Work harder")
    scheduler = sched.scheduler(time.time, time.sleep)
    if cycle_time % 3 == 0:
        cycle_time += 1
        scheduler.enter(work, 1, start_long_break, argument=(long_break, short_break, work, cycle_time))
    else:
        cycle_time += 1
        scheduler.enter(work, 1, start_short_break, argument=(long_break, short_break, work, cycle_time))
    scheduler.run()


def start_pomodoro(options):
    long_break = options.long_break * 60
    short_break = options.short_break * 60
    work = options.work * 60
    cycle = options.cycle
    start_work(long_break, short_break, work, cycle)

DEFAULT_LONG_BREAK = 15
DEFAULT_SHORT_BREAK = 5
DEFAULT_WORK = 40
DEFAULT_CYCLE = 3

parser = OptionParser()
parser.add_option("--longbreak", "--lb",  dest="long_break", type="int", default=DEFAULT_LONG_BREAK,
                  help="Defines long break in minutes. [default: %default]")
parser.add_option("--shortbreak", "--sb",  dest="short_break", type="int", default=DEFAULT_SHORT_BREAK,
                  help="Defines short break in minutes. [default: %default]")
parser.add_option("--work", "-w",  dest="work", type="int", default=DEFAULT_WORK,
                  help="Defines work in minutes. [default: %default]")
parser.add_option("--cycle", "-c",  dest="cycle", type="int", default=DEFAULT_CYCLE,
                  help="Defines long break cycles. [default: %default]")

(options, args) = parser.parse_args()
start_pomodoro(options)



