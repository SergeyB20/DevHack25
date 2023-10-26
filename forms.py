from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
  category = State()
  TeachPass = State()
  NumGroup = State()
  Mailing = State()
  FullName = State()
  Meny = State()
  AddNote = State()
  notification = State()