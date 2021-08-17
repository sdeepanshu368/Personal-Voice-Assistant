import datetime
import winsound


def alarm(Timing):
    al_time = str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
    al_time = al_time[11:-3]
    print(al_time)
    ho = int(al_time[:2])
    mi = int(al_time[3:5])
    print(f'Done, Alarm is set for {Timing}')

    while True:
        if ho >= datetime.datetime.now().hour:
            if mi == datetime.datetime.now().minute:
                winsound.PlaySound('abc', winsound.SND_LOOP)

            elif mi < datetime.datetime.now().minute:
                break


if __name__ == '__main__':
    alarm('3:45 PM')
