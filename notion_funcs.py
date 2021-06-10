import requests, json, os

class Notion_funcs:
    def __init__(self, token_id, habits_db, habits_backend_db):
        #self.token_id = token_id
        self.habits_db = habits_db
        self.habits_backend_db = habits_backend_db
        self.headers = {'Authorization': 'Bearer '+token_id+'',
                  'Content-Type':'application/json',
                  'Notion-Version':'2021-05-13'}

    def get_total_days(self):
        post_location = 'https://api.notion.com/v1/databases/'+self.habits_backend_db+'/query'
        return len(json.loads(requests.post(post_location,headers=self.headers).content)['results'])

    def get_habits(self):
      post_location = 'https://api.notion.com/v1/databases/'+self.habits_db+'/query'

      habit_data = requests.post(post_location,headers=self.headers)
      habit_tree = json.loads(habit_data.content)

      id_list = {}
      check_list = {}
      streak_list = {}
      best_streak_list = {}
      misses_list = {}
      cnt = 0
      for i in habit_tree['results']:
        id_list[cnt] = i['id']
        check_list[cnt] = i['properties']['Done']['checkbox']
        streak_list[cnt] = i['properties']['Current Streak']['number']
        best_streak_list[cnt] = i['properties']['Best Streak']['number']
        if len(i['properties']['Current Misses']['rich_text'])>0:
            misses_list[cnt] = i['properties']['Current Misses']['rich_text'][0]['text']['content']
        else:
            misses_list[cnt] = None


        cnt = cnt+1
      return id_list, check_list, streak_list, best_streak_list, misses_list

    def update_habit_streak(self, page_id, streak, best, misses, total_days):
        post_location = 'https://api.notion.com/v1/pages/'+ page_id

        data = json.dumps(
        {"properties":
          {
          "Current Streak": {"number": streak},
          "Best Streak": {"number": best},
          "Current Misses": {"rich_text": [{"text": {"content": misses}}]},
          "Done": {"checkbox": False},
          "Total Days": {"number": total_days}
          }
        })

        r = requests.patch(post_location,headers=self.headers, data=data)
        returned_data = json.loads(r.content)

        return returned_data

    def update_backend(self, habits_list, date):
        post_location = 'https://api.notion.com/v1/pages'

        data = json.dumps({
            'parent':{'database_id':self.habits_backend_db},
            'properties': {
                'Habits done': {'relation': habits_list},
                "Day":{"title":[{"text":{"content":str(date)}}]}
            }
        })

        r = requests.post(post_location,headers=self.headers,data=data)

        return r.content
