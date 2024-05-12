def formatMessages(messages):
    res = ""
    for index, message in enumerate(messages):
        res += f"From User: {message[1]}\n"
        res += f"Message {index + 1} {message[2].strftime('%H:%M %d/%m/%Y')} : {message[0]}\n"
        res += "--------------------------\n"

    return res

def formatChannelMessages(messages):
    res = ""
    for message in messages:
        res += f"{message[1]} {message[2]}: {message[0]}\n"
        res += "--------------------------\n"

    return res