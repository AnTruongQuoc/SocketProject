from appJar import gui

app = gui("Chatter", "300x300")
lists = []
def press(btn):
    if btn == "Send":
        note = app.getEntry("e1")
        lists.append(note)
        app.updateListBox("list", lists, False, False)
    elif btn == "Leave":
        app.stop()

def chatbox():
    app.setFont(20)
    app.addLabel("title", " Welcome to Chatroom ") 
    app.startScrollPane("PANE")
    app.addListBox("list", lists)
    app.stopScrollPane()
    app.setFont(13)
    app.addEntry("e1")
    app.setEntryDefault("e1", "Type message here")
    app.addButtons(["Send", "Leave"], press) 
    app.go()

chatbox()