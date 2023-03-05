
class FileNames:
  """
  FileNames class
  Solely purpose for checking the discord
  attachments file format
  """


  def __init__(self,file):
    self.check = str(file).split("filename='")[1].split("' ")[0]

  def format(self):
    format = self.check.split(".")[-1]
    return format
