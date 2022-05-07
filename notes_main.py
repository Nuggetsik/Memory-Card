#почни тут створювати додаток з розумними замітками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, QLabel, QVBoxLayout,
QHBoxLayout,QTextEdit, QLineEdit, QListWidget, QInputDialog, QMessageBox)
import json 

notes = {"Инструкция" : {
    "текст" : "Текст",
    "теги": []}}



def message_box(text):
    message_win = QMessageBox()
    message_win.setText(text)
    message_win.exec_()


def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[name]["теги"])


def save_notes():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True,ensure_ascii = False)
            

    else:
        text = "Заметка не выбрана"
        message_box(text)

def add_notes():
    note_name, result = QInputDialog.getText(
        win, "Добавить заметку", "Название заметки"
    )
    if result and note_name != '':
        notes[note_name] = {"текст":"", "теги":[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        
    
    
def del_notes():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w") as file:
            json.dump(notes, file, sort_keys = True,ensure_ascii = False)
            
    else:
       text = "Заметка не выбрана"
       message_box(text)

def add_tags():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = text_tegs.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            
            list_tags.addItem(tag)
            text_tegs.clear()
        with open("notes_data.json","w") as file:
            json.dump(notes, file, sort_keys = True,ensure_ascii = False)
            
    else:
        text = "Заметка не выбрана"
        message_box(text)
        
    

def del_tags():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_dara.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
       text = "Тег для удаления не выбран!"
       message_box(text)

def search_tags():
    
    tag = text_tegs.text()
    if find_tags.text() == "Искать заметки по тегу" and tag:
        
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        find_tags.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    
    elif find_tags.text() == "Сбросить поиск":
        text_tegs.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        find_tags.setText("Искать заметки по тегу")
    
    else:
        pass
    



app = QApplication([])
win = QWidget()
win.setWindowTitle("Умные заметки")
win.resize(900,700)

create_note = QPushButton("Создать заметку")
del_note = QPushButton("Удалить заметку")
save_note = QPushButton("Сохранить заметку")


create_tags = QPushButton("Добавить до заметки")
del_tag = QPushButton("Открепить от заметки")
find_tags = QPushButton("Искать заметки по тегу")

text_tegs = QLineEdit()
text_tegs.setPlaceholderText("Введите тег")
main_line = QHBoxLayout()

name_note = QLabel("Список заметок")
name_tag  = QLabel("Список тегов")

message_win = QMessageBox()

list_notes = QListWidget()
list_tags = QListWidget()

field_text = QTextEdit()
field_text.setText("Текст")

field_tags = QLineEdit()

v_layout1 = QVBoxLayout()
h_lay_textedit = QHBoxLayout()
h_lay_textedit.addWidget(field_text)
v_layout1.addLayout(h_lay_textedit)


v_layout2 = QVBoxLayout()
h_lay_listwidget1 = QHBoxLayout()
h_lay_button_widget1 = QHBoxLayout()
h_lay_button_widget2 = QHBoxLayout()


h_lay_listwidget1.addWidget(list_notes)
h_lay_button_widget1.addWidget(create_note)
h_lay_button_widget1.addWidget(del_note)
h_lay_button_widget2.addWidget(save_note)
v_layout2.addLayout(h_lay_listwidget1)
v_layout2.addLayout(h_lay_button_widget1)
v_layout2.addLayout(h_lay_button_widget2)


h_lay_listtags = QHBoxLayout()
h_lay_text_tegs = QHBoxLayout()
h_lay_button_tags1 = QHBoxLayout()
h_lay_button_tags2 = QHBoxLayout()


h_lay_listtags.addWidget(list_tags)
h_lay_text_tegs.addWidget(text_tegs)
h_lay_button_tags1.addWidget(create_tags)
h_lay_button_tags1.addWidget(del_tag)
h_lay_button_tags2.addWidget(find_tags)

v_layout2.addLayout(h_lay_listtags)
v_layout2.addLayout(h_lay_text_tegs)
v_layout2.addLayout(h_lay_button_tags1)
v_layout2.addLayout(h_lay_button_tags2)


create_note.clicked.connect(add_notes)
del_note.clicked.connect(del_notes)
save_note.clicked.connect(save_notes)


list_notes.itemClicked.connect(show_note)

create_tags.clicked.connect(add_tags)
del_tag.clicked.connect(del_tags)
find_tags.clicked.connect(search_tags)

main_line.addLayout(v_layout1)
main_line.addLayout(v_layout2)

win.setLayout(main_line)


win.show()
while True:
    try:
        with open("notes_data.json","r") as file:
            notes = json.load(file)
        list_notes.addItems(notes)
        break
        
    except:
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        list_notes.addItems(notes)
        break


app.exec_()