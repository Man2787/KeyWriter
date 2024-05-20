import customtkinter
from threading import Thread
from pynput.keyboard import Controller, Listener
from time import sleep
from random import uniform

UNIX_LINE_ENDING = "\n"
WINDOWS_LINE_ENDING = "\r\n"
MAC_OS_OLD_LINE_ENDING = "\r"
MAC_OS_NEW_LINE_ENDING = "\n"

WLE = "Windows Line Endings (\\r\\n)"
ULE = "Unix Line Endings (\\n)"
MOLE = "Mac Old Line Ending(\\r)"
MNLE = "Mac New Line Ending(\\n)"

VERSION = "1.1.1"

# keys = "Esse laboris deserunt aute commodo do culpa cillum adipisicing aliqua quis officia nostrud."


typing = False
quitting = False
stopWriting = False

listening: bool = False
setStart: bool = True

startCode: int = None
endCode: int = None

stopCodeLable = None
startCodeLable = None

timeBetweenLettersDefault = .06
letterTimeVarinceDefault = .05

timeBetweenSpacesDefault = .5
spaceTimeVarinceDefault = .2

keyboard = Controller()


def abs(a):
    if (a < 0):
        return a * -1
    return a


def Write():
    global typing, stopWriting

    typing = True

    sleep(8)

    # region input setting

    endingStyle = lineEndingMenu.get()

    text = entryText._textbox.get("0.0", customtkinter.END)

    if (endingStyle == WLE):
        text = text.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)
    elif (endingStyle == ULE):
        text = text.replace(UNIX_LINE_ENDING, UNIX_LINE_ENDING)
    elif (endingStyle == MOLE):
        text = text.replace(UNIX_LINE_ENDING, MAC_OS_OLD_LINE_ENDING)
    elif (endingStyle == MNLE):
        text = text.replace(UNIX_LINE_ENDING, MAC_OS_NEW_LINE_ENDING)
    else:
        print("endingStyle not recegonised")

    try:
        timeBetweenLetters: float = float(
            entryTimeBetweenLetters.get()
        )
    except Exception as e:
        print(e)
        timeBetweenLetters: float = timeBetweenLettersDefault

    try:
        letterTimeVarince: float = float(
            entryLetterTimeVarince.get()
        )
    except Exception as e:
        print(e)
        letterTimeVarince: float = letterTimeVarinceDefault

    try:
        timeBetweenSpaces: float = float(
            entryTimeBetweenSpaces.get()
        )
    except Exception as e:
        print(e)
        timeBetweenSpaces: float = timeBetweenSpacesDefault

    try:
        spaceTimeVarince: float = float(
            entrySpaceTimeVarince.get()
        )
    except Exception as e:
        print(e)
        spaceTimeVarince: float = spaceTimeVarinceDefault

    # endregion

    keysWrote: int = 0

    while (keysWrote < text.__len__()):
        if (quitting or stopWriting):
            break

        if (text[keysWrote] == ' '):
            keyboard.press(text[keysWrote])
            sleep(abs(uniform(timeBetweenSpaces - spaceTimeVarince,
                  timeBetweenSpaces + spaceTimeVarince)))
        else:
            keyboard.press(text[keysWrote])
            sleep(abs(uniform(timeBetweenLetters - letterTimeVarince,
                  timeBetweenLetters + letterTimeVarince)))
        keysWrote += 1

    stopWriting = False
    typing = False


def CreateWriteThread():
    print("Creating Write Thread")
    if (not typing):
        thread = Thread(target=Write, args=())
        thread.start()
    # thread.join()


def StopWriting():
    print("Stoping Write Thread")
    global stopWriting
    if (typing):
        stopWriting = True
    else:
        stopWriting = False


def Start():
    global entryTimeBetweenLetters, entryLetterTimeVarince, entryTimeBetweenSpaces, entrySpaceTimeVarince, entryText, lineEndingMenu, stopCodeLable, startCodeLable

    # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_appearance_mode("dark")
    # Themes: "blue" (standard), "green", "dark-blue"
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()

    def close():
        global quitting
        quitting = True
        app.destroy()

    def SetKey(key, start: bool = True):
        global startCode, endCode

        if (start):
            try:
                startCode = key.char
            except AttributeError:
                startCode = key

            if (startCode == keyboard._Key.esc):
                startCode = None

            if (startCodeLable != None):
                if (startCode == None):
                    startCodeLable.configure(
                        require_redraw=True,
                        text="None"
                    )
                else:
                    startCodeLable.configure(
                        require_redraw=True,
                        text=startCode
                    )
        else:
            try:
                endCode = key.char
            except AttributeError:
                endCode = key

            if (endCode == keyboard._Key.esc):
                endCode = None

            if (endCodeLable != None):
                if (endCode == None):
                    endCodeLable.configure(
                        require_redraw=True,
                        text="None"
                    )
                else:
                    endCodeLable.configure(
                        require_redraw=True,
                        text=endCode
                    )

    def keyDown(key):
        global listening

        if (listening):
            SetKey(key, setStart)
            listening = False
        else:
            if (not typing):
                if (key == startCode):
                    CreateWriteThread()

            if (key == endCode):
                StopWriting()

    def SetStartVar():
        global setStart, listening
        setStart = True
        listening = True

    def SetEndVar():
        global setStart, listening
        setStart = False
        listening = True

    listener = Listener(on_press=keyDown)
    listener.start()

    # app.bind("<KeyPress>", keyDown)
    # app.bind("<KeyRelease>", keyUp)

    app.protocol("WM_DELETE_WINDOW", close)

    app.geometry("700x450")
    app.resizable(False, False)
    app.title("writer")

    # region Frames

    sidebar_frame = customtkinter.CTkFrame(
        master=app,
        width=200,
        corner_radius=5
    )
    sidebar_frame.pack(pady=10, padx=10, fill="y", side="left")

    frameOne = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameOne.pack(pady=(10, 3), padx=10, fill="x", side="top")

    frameTwo = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameTwo.pack(pady=3, padx=10, fill="x", side="top")

    frameThree = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameThree.pack(pady=3, padx=10, fill="x", side="top")

    frameFour = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameFour.pack(pady=3, padx=10, fill="x", side="top")

    frameFive = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameFive.pack(pady=(30, 3), padx=10, fill="x", side="top")

    frameSix = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameSix.pack(pady=3, padx=10, fill="x", side="top")

    frameSeven = customtkinter.CTkFrame(
        master=sidebar_frame,
        width=180,
        height=34,
        corner_radius=5
    )
    frameSeven.pack(pady=3, padx=10, fill="x", side="bottom")

    # endregion

    # region customization lables

    entryTimeBetweenLettersLable = customtkinter.CTkLabel(
        master=frameOne,
        text="Time Between Letters"
    )
    entryTimeBetweenLettersLable.pack(pady=0, padx=4, side="left")

    entryLetterTimeVarinceLable = customtkinter.CTkLabel(
        master=frameTwo,
        text="Letter Time Varince"
    )
    entryLetterTimeVarinceLable.pack(pady=0, padx=4, side="left")

    entryTimeBetweenSpacesLable = customtkinter.CTkLabel(
        master=frameThree,
        text="Time Between Spaces"
    )
    entryTimeBetweenSpacesLable.pack(pady=0, padx=4, side="left")

    entrySpaceTimeVarinceLable = customtkinter.CTkLabel(
        master=frameFour,
        text="Space Time Varince"
    )
    entrySpaceTimeVarinceLable.pack(pady=0, padx=4, side="left")

    startCodeLable = customtkinter.CTkLabel(
        master=frameFive,
        text="Start Key Bind"
    )
    startCodeLable.pack(pady=0, padx=4, side="left")

    stopCodeLable = customtkinter.CTkLabel(
        master=frameSix,
        text="End Key Bind"
    )
    stopCodeLable.pack(pady=0, padx=4, side="left")

    startCodeLable = customtkinter.CTkLabel(
        master=frameFive,
        text="None"
    )
    startCodeLable.pack(pady=3, padx=5, side="right")

    endCodeLable = customtkinter.CTkLabel(
        master=frameSix,
        text="None"
    )
    endCodeLable.pack(pady=3, padx=5, side="right")

    # endregion

    # region customization entrys

    entryTimeBetweenLetters = customtkinter.CTkEntry(
        master=frameOne,
        width=40,
        placeholder_text="Time Between Letters",
        textvariable=customtkinter.StringVar(master=app, value="0.06")
    )
    entryTimeBetweenLetters.pack(pady=3, padx=5, side="right")

    entryLetterTimeVarince = customtkinter.CTkEntry(
        master=frameTwo,
        width=40,
        placeholder_text="Letter Time Varince",
        textvariable=customtkinter.StringVar(master=app, value="0.05")
    )
    entryLetterTimeVarince.pack(pady=3, padx=5, side="right")

    entryTimeBetweenSpaces = customtkinter.CTkEntry(
        master=frameThree,
        width=40,
        placeholder_text="Time Between Spaces",
        textvariable=customtkinter.StringVar(master=app, value="0.5")
    )
    entryTimeBetweenSpaces.pack(pady=3, padx=5, side="right")

    entrySpaceTimeVarince = customtkinter.CTkEntry(
        master=frameFour,
        width=40,
        placeholder_text="Space Time Varince",
        textvariable=customtkinter.StringVar(master=app, value="0.2")
    )
    entrySpaceTimeVarince.pack(pady=3, padx=5, side="right")

    # endregion

    # region buttons

    startButton = customtkinter.CTkButton(
        master=frameSeven,
        command=CreateWriteThread,
        text="Start Writing",
        width=80
    )
    startButton.pack(pady=3, padx=3, side="left")

    stopButton = customtkinter.CTkButton(
        master=frameSeven,
        command=StopWriting,
        text="Stop Writing",
        width=80
    )
    stopButton.pack(pady=3, padx=3, side="right")

    lineEndingMenu = customtkinter.CTkOptionMenu(
        master=sidebar_frame,
        values=[WLE, ULE, MOLE, MNLE]
    )
    lineEndingMenu.pack(pady=10, padx=10, side="bottom")

    setStartButton = customtkinter.CTkButton(
        master=frameFive,
        command=SetStartVar,
        text="Set",
        width=20
    )
    setStartButton.pack(pady=3, padx=3, side="left")

    setEndButton = customtkinter.CTkButton(
        master=frameSix,
        command=SetEndVar,
        text="Set",
        width=20
    )
    setEndButton.pack(pady=3, padx=3, side="left")

    # endregion

    lable = customtkinter.CTkLabel(
        master=app,
        text=f"Text Writer\nversion {VERSION}"
    )
    lable.pack(pady=(3, 10), padx=10, side="bottom")

    entryText = customtkinter.CTkTextbox(
        master=app,
        width=460,
        height=390,
        border_width=2,
        corner_radius=5
    )
    entryText.pack(pady=10, padx=(0, 10), fill="y")

    app.mainloop()


Start()
