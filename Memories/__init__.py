import matplotlib.pyplot as plt
import heapq
from MyAnimeList import ordinals
import matplotlib.font_manager as fm

class Yandere:
  """
  Yandere Object
  Main purpose is to get information
  from download url
  """

  def __init__(self, post):
    self.url = post
    self.filter = "".join(self.url.split(".")[:-1]).replace("%28","(").replace("%29",")").replace("_"," ").replace("%3A",":").replace("%27","'").replace("%21","!").replace("%40","@").title().split("%20")
  
  def post(self):
    tags = "\n".join(["• "+i.title() for i in self.filter[2:]])
    url = f"https://yande.re/post/show/{self.filter[1]}"
    sample = f"https://files.yande.re/sample/{'/'.join(self.url.split('/')[4:])}"
    return {
            'tags': tags,
            'post_url': url,
            'sample': sample
           }



def data_chart(
        table: str,
        data : dict,
        size : tuple
        ):
  """
  Create a bar chart from a dictionary
  Main purpose is for
  'recount' and 'cate' commands
  """
  fprop = fm.FontProperties(fname='Memories/font.otf')

                
  chara = [key for key,value in data.items()]
  total = [value for key,value in data.items()]
  
  fig, ax = plt.subplots(figsize=size)
  
  ax.bar(chara, total)
  ax.set_title(table.capitalize())
  ax.set_xlabel("Character's Names")
  ax.set_ylabel("Total Posts")
  ax.set_xticks(range(len(chara)), fontproperties=fprop)
  ax.set_xticklabels(chara, rotation=-90)
  plt.subplots_adjust(wspace=0.5)
  fig.tight_layout()
  fig.savefig("Memories/Chart.png",
              bbox_inches='tight')




def top(
        data : dict,
        top  : int
       ):
  """
  A function to get the n highest value
  from a dictionary and return it as a list
  """
         
  top_tags = heapq.nlargest(top,
             data.items(),
             key=lambda x: x[1])
  top_list = [f"• {ordinals(i+1)} Place\n「**{k}**」\nConsisting **{v} Posts**\n" for i,(k,v) in enumerate(top_tags)]
  return top_list
