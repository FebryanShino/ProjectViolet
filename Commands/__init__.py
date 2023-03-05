class CommandCenter:
  """
  An algorithm to read Command Data
  from a .txt file
  """
  
  def datalist(self):
    data = []
    with open("Commands/command_data.txt", "r") as f:
      lines = f.readlines()
      for i in lines:
        data.append(i)
        
    content = []
    header = []
    data_formatted = "".join(data).split("\n\n")
    for i in data_formatted:
      header.append(i.split("\n")[0])
      content.append("\n".join(i.split("\n")[1:]))
    file = dict(zip(header, content))
    return file


