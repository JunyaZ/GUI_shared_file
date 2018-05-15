from tkinter import *
from tkinter import messagebox
import os.path
import threading

class Application:

    def __init__(self, form):
        # Creates the size of the window
        form.resizable(0, 0)
        form.minsize(200, 200)
        form.title('Instant Messaging')

        # Labels the entry for username
        UsernameLabel = Label(form, text="Username: ")
        UsernameLabel.grid(row=0, column=0)
        AnonymousLabel = Label(form, text="(If Username not specified, the message "
                                          "will be marked as anonymous.)")
        AnonymousLabel.grid(row=1, column=0, columnspan=2)

        # Area where the user types in their username
        UsernameEntry = Entry(form)
        self.UsernameEntry = UsernameEntry
        UsernameEntry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Button that loads all messages sent to the specified username
        LoadMessagesButton = Button(form, text='Load Messages', command=self.loadMessages)
        LoadMessagesButton.grid(row=0, column=2, padx=5, pady=5, sticky=W)


        # Displays all messages to user
        ListOfMessages = Text(form, width=40, height=10, wrap=WORD)
        self.ListOfMessages = ListOfMessages  # see above
        ListOfMessages.grid(row=2, column=1, padx=5, pady=4, sticky=W)

        # Labels the entry for the recipient of the message
        RecipientLabel = Label(form, text="Recipient: ")
        RecipientLabel.grid(row=3, column=0)

        # Area where the user specifies the recipient
        RecipientEntry = Entry(form)
        self.RecipientEntry = RecipientEntry
        RecipientEntry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Labels the entry for the message
        MessageLabel = Label(form, text="Message: ")
        MessageLabel.grid(row=4, column=0)

        # Area where the user writes the messages
        MessageEntry = Entry(form, width=54)
        self.MessageEntry = MessageEntry
        MessageEntry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # The button used to send the message to the desired user
        SendMessageButton = Button(form, text='Send Message', command=self.addchat)
        SendMessageButton.grid(row=4, column=2, padx=5, pady=5, sticky=W)

        # Adds the ability to scroll through your messages
        scrollbar1 = Scrollbar(form)
        scrollbar1.config(command=ListOfMessages.yview)
        scrollbar1.grid(row=2, column=2, padx=5, pady=5, sticky=W)
        ListOfMessages.config(yscrollcommand=scrollbar1.set)

        form.mainloop()


    def addchat(self):
        # Pulls the message, the recipient, username, and the recipient from the textboxes
        message = self.MessageEntry.get()
        username = self.UsernameEntry.get()
        recipient = self.RecipientEntry.get() + ".txt"
        self.ListOfMessages.config(state="normal")
        # If no username is specified, the message they send is marked as anonymous
        if username == "":
            username = "Anonymous"
        # If no recipient is specified, a message appears saying to enter a recipient
        if recipient == ".txt":
            self.ListOfMessages.delete(1.0, END)
            self.ListOfMessages.insert(END, "Please enter a recipient.")
        # If a recipient is selected, a message is appended to their textfile of messages
        # If the recipient doesn't have an existing textfile, one is made for them
        else:
            with open(recipient, "a") as user_messages:
                user_messages.write(username + ": " + message + "\n\n")
                #The following is an optional feature to confirm message has been sent.
				#messagebox.showinfo("Confirmation", "Your message has been sent.")
            self.MessageEntry.delete(0, END)
        self.ListOfMessages.config(state=DISABLED)

    def loadMessages(self):
        username = self.UsernameEntry.get() + ".txt"
        self.ListOfMessages.config(state="normal")
        # If no username is specified, a message will appear that will ask for one
        if username == ".txt":
            self.ListOfMessages.delete(1.0, END)
            self.ListOfMessages.insert(END, "Please enter a username")
        else:
            if os.path.isfile(username):
                # If the file exists, it displays the messages
                with open(username, 'r') as user_messages:
                    messages = user_messages.read()
                self.ListOfMessages.delete(1.0, END)
                self.ListOfMessages.insert(END, messages + "\n")
                self.ListOfMessages.update()
                self.ListOfMessages.yview_moveto(1)
            else:
                # If the file doesn't exist, that means they have no messages
                self.ListOfMessages.delete(1.0, END)
                self.ListOfMessages.insert(END, "You have no messages")
        self.ListOfMessages.config(state=DISABLED)
        root.after(10000, self.loadMessages) #auto reloads messages every 10 seconds.



root = Tk()
Application(root)

