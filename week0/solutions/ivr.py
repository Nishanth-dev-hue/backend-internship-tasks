def ivr(start_menu):
    stack = []
    current_menu = start_menu

    while True:
        print("\n" + current_menu["title"])
        for key, value in current_menu["options"].items():
            print(f"{key}. {value['label']}")

        choice = input("Enter choice: ")

        if choice not in current_menu["options"]:
            print("Invalid choice")
            continue

        selected = current_menu["options"][choice]

        if selected["type"] == "exit":
            print("Thank you for using IVR")
            break

        elif selected["type"] == "action":
            print(selected["message"])

        elif selected["type"] == "menu":
            stack.append(current_menu)
            current_menu = selected["menu"]

        elif selected["type"] == "back":
            if stack:
                current_menu = stack.pop()
            else:
                print("Already at Main Menu")


prepaid_menu = {
    "title": "Prepaid Menu",
    "options": {
        "1": {"label": "Balance Inquiry", "type": "action", "message": "Your balance is Rs. 120"},
        "2": {"label": "Recharge", "type": "action", "message": "Recharge successful"},
        "3": {"label": "Data Plans", "type": "action", "message": "1GB/day | 2GB/day | Unlimited"},
        "4": {"label": "Back", "type": "back"}
    }
}

postpaid_menu = {
    "title": "Postpaid Menu",
    "options": {
        "1": {"label": "Current Bill", "type": "action", "message": "Your bill amount is Rs. 499"},
        "2": {"label": "Bill Payment", "type": "action", "message": "Payment completed"},
        "3": {"label": "Plan Upgrade", "type": "action", "message": "Plan upgraded successfully"},
        "4": {"label": "Back", "type": "back"}
    }
}

mobile_menu = {
    "title": "Mobile Services",
    "options": {
        "1": {"label": "Prepaid", "type": "menu", "menu": prepaid_menu},
        "2": {"label": "Postpaid", "type": "menu", "menu": postpaid_menu},
        "3": {"label": "Back", "type": "back"}
    }
}

internet_menu = {
    "title": "Internet Services",
    "options": {
        "1": {"label": "Broadband", "type": "action", "message": "Broadband usage details shown"},
        "2": {"label": "Fiber", "type": "action", "message": "Fiber service options shown"},
        "3": {"label": "Back", "type": "back"}
    }
}

tv_menu = {
    "title": "TV & OTT Services",
    "options": {
        "1": {"label": "Channel Packs", "type": "action", "message": "Sports | Movies | All-in-One"},
        "2": {"label": "Recharge", "type": "action", "message": "Recharge completed"},
        "3": {"label": "Complaint", "type": "action", "message": "Complaint registered"},
        "4": {"label": "Back", "type": "back"}
    }
}

main_menu = {
    "title": "Main Menu",
    "options": {
        "1": {"label": "Mobile Services", "type": "menu", "menu": mobile_menu},
        "2": {"label": "Internet Services", "type": "menu", "menu": internet_menu},
        "3": {"label": "TV & OTT Services", "type": "menu", "menu": tv_menu},
        "4": {"label": "Talk to Customer Support", "type": "action", "message": "Connecting to customer support"},
        "5": {"label": "Exit", "type": "exit"}
    }
}

ivr(main_menu)