from appJar import gui
import crypt as cr

app = gui("Chatter", "300x380")
lists = []
def press(btn):

    if btn == "Send" or btn == "Return":
        note = app.getEntry("e1")
        if note == "":
            pass
        else:
            lists.append(note)
            app.updateListBox("list", lists, False, False)
            app.clearEntry("e1", callFunction=False)
        
    elif btn == "Leave":
        app.stop()

def chatbox():
    

    app.startFrame("TOP", row=0, column=0) 
    app.setFont(20)
    app.setPadding([10,0])
    app.setSticky('news')
    app.addLabel("title", " Welcome to Chatroom ")
    app.setLabelHeight("title", 2)
    app.stopFrame()

    app.startFrame("MID", row=1, column=0)
    app.startScrollPane("PANE")
    app.setPadding([10,10])
    app.addListBox("list", lists)
    app.setListBoxWidth("list", 30)
    app.setListBoxHeight("list", 10)
    app.stopScrollPane()
    app.stopFrame()

    app.startFrame("MID_mess", row=2, column=0) 
    app.setFont(13)
    app.setPadding([5,5])
    app.addEntry("e1", 2, 0)
    app.setEntryDefault("e1", "Type message here")
    
    app.addButton("Send", press, 2 , 1)
    app.setButtonHeight("Send", 1)
    app.setButtonBg("Send", "#035AA6")
    app.setButtonFg("Send", "White")

    app.enableEnter(press)
    app.stopFrame()

    app.startFrame("BOTTOM", row=3, column=0)
    app.setFrameHeight("BOTTOM", 10)
    app.setPadding([5, 5])
    app.addButtons(["Add" ,"Leave"], press, 2, 0, 2)
    app.setButtonWidth("Add", 6)
    app.setButtonWidth("Leave", 6)
    app.setButtonBg("Add", "#4b8e8d")
    app.setButtonFg("Add", "White")
    app.setButtonBg("Leave", "#D32626")
    app.setButtonFg("Leave", "White")
    app.stopFrame()
    app.go()

def cree():
    affine = cr.Affine()
    passw = "sdqwdas123"
    enpass = affine.encrypt(passw)
    print(affine.encrypt(passw))
    print(affine.decrypt(enpass))

cree()