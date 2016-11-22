from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty

__author__ = 'Connor Barrett'


class ShoppingListApp(App):
    status_text = StringProperty()
    cost_text = StringProperty()

    def __init__(self, **kwargs):

        super(ShoppingListApp, self).__init__(**kwargs)
        item_file = open("items.csv", 'r')
        self.shoppinglist = [line.strip().split(',') for line in item_file.readlines()]
        print(self.shoppinglist)
        item_file.close()

    def on_stop(self):
        item_file = open("items.csv", "w")
        for line in range(len(self.shoppinglist)):
            item_line = str(
                "{},{},{},{}".format(self.shoppinglist[line][0], self.shoppinglist[line][1], self.shoppinglist[line][2],
                                     self.shoppinglist[line][3]))
            print(item_line, file=item_file)
        item_file.close()

    def build(self):
        self.title = "Connor Barrett A2 - Shopping List 2.0"
        self.root = Builder.load_file('app.kv')
        self.create_entry_buttons()
        return self.root

    def create_entry_buttons(self):
        self.root.ids.entriesBox.clear_widgets()
        self.shoppinglist.sort(key=lambda x: int(x[2]))
        sum_of_items = 0
        for name in range(len(self.shoppinglist)):

            if self.shoppinglist[name][3] == "r":
                temp_button = Button(text=self.shoppinglist[name][0])
                temp_button.bind(on_release=self.press_entry)
                sum_of_items += float(self.shoppinglist[name][1])
                if self.shoppinglist[name][2] == "1":
                    temp_button.background_color = (1.0, 0.0, 0.0, 1.0)
                elif self.shoppinglist[name][2] == "2":
                    temp_button.background_color = (0.0, 0.0, 1.0, 1.0)
                elif self.shoppinglist[name][2] == "3":
                    temp_button.background_color = (0.0, 1.0, 0.0, 1.0)
                self.root.ids.entriesBox.add_widget(temp_button)
                self.cost_text = "Total Price: ${}".format(sum_of_items)
            elif sum_of_items == 0:
                self.cost_text = "No items required"

    def press_entry(self, instance):
        name = instance.text
        i = 0
        found = 0
        while found == 0:
            if self.shoppinglist[i][0] == name:
                if self.shoppinglist[i][3] == "r":
                    self.status_text = "Completed: {}, ${}, priority {}".format(self.shoppinglist[i][0],
                                                                                self.shoppinglist[i][1],
                                                                                self.shoppinglist[i][2])
                    # set button state
                    instance.state = 'down'
                    self.shoppinglist[i][3] = "c"
                    self.create_entry_buttons()
                else:
                    self.status_text = "{}, ${}, priority {} (completed)".format(self.shoppinglist[i][0],
                                                                                 self.shoppinglist[i][1],
                                                                                 self.shoppinglist[i][2])
                found = 1
            else:
                i = i + 1

    def press_required(self):
        self.create_entry_buttons()

    def press_completed(self):
        self.root.ids.entriesBox.clear_widgets()
        self.shoppinglist.sort(key=lambda x: int(x[2]))
        self.cost_text = "Showing completed items"
        for name in range(len(self.shoppinglist)):
            if self.shoppinglist[name][3] == "c":
                temp_button = Button(text=self.shoppinglist[name][0])
                temp_button.bind(on_release=self.press_entry)
                self.root.ids.entriesBox.add_widget(temp_button)

    def press_clear(self):
        for instance in self.root.ids.entriesBox.children:
            instance.state = 'normal'
        self.status_text = ""
        self.clear_fields()

    def press_save(self, added_name, added_price, added_priority):
        if added_price == '' or added_name == '' or added_priority == '':
            self.status_text = 'All fields must be completed'
            return
        try:
            added_priority = eval(added_priority) * 1
            added_price = eval(added_price) * 1
            added_priority = str(added_priority)
            added_price = str(added_price)
        except NameError:
            self.status_text = 'Please enter a valid number'
            return
        if int(added_priority) <= 0 or int(added_priority) >= 4:
            self.status_text = 'Priority must be 1,2 or 3'
            return
        if float(added_price) < 0:
            self.status_text = 'Price must not be negative'
            return
        new_item = [added_name, added_price, added_priority, "r"]
        self.shoppinglist.append(new_item)
        temp_button = Button(text=added_name)
        temp_button.bind(on_release=self.press_entry)
        self.create_entry_buttons()
        self.clear_fields()

    def clear_fields(self):
        self.root.ids.addedName.text = ""
        self.root.ids.addedPrice.text = ""
        self.root.ids.addedPriority.text = ""


ShoppingListApp().run()
