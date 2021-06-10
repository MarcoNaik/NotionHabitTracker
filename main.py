from notion_funcs import Notion_funcs
from datetime import datetime, date, timedelta, timezone

nf = Notion_funcs(input_data['token_id'], input_data['habits_db'], input_data['habits_backend_db'])

id, check, streak, best_streak, misses = nf.get_habits()
total_days = nf.get_total_days()+1
checked_habits_id = []

for i in range(len(id)):
    if check[i]:
        #Updating streaks and clearing misses
        current_streak = streak[i]+1
        if current_streak > best_streak[i]:
            nf.update_habit_streak(id[i], current_streak, current_streak, "", total_days)
        else:
            nf.update_habit_streak(id[i], current_streak, best_streak[i], "", total_days)
        checked_habits_id.append({'id': id[i]})
    else:
        #if misses clear streaks and add cross
        nf.update_habit_streak(id[i], 0, best_streak[i] , misses[i] + "❌", total_days)


#Current day
date = datetime.now(timezone(timedelta(hours= -4.0))).date() - timedelta(1)

#add page to backend with checked habits
nf.update_backend(checked_habits_id, date)
