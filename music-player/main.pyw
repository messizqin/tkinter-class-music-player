import os
import json

# python 3 support
try:
    from tkinter.constants import *
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    from Tkinter.constants import *
    from Tkinter import *
    from Tkinter import messagebox
import pygame

try:
    basestring
except NameError:
    basestring = str

from random import shuffle

# pass in two array of same elements in different order, return how second one can be gained from first
def change(initial, after):
    pc = []
    for i in after:
        pc.append(initial.index(i))
    return pc

# global constant 
class Module:
    def __init__(self):
        # switch between music tags and dummy tags
        self.switched = False
        # whether restart from beginning or not
        self.resorted = False
        # Labels and music file names
        self.label_tags = []
        self.label_nams = []
        # stop music and start music
        self.paused = False
        self.started = False
        # files never change, it is the file collected at once from directory as the player start
        self.files = []
        # finds never change, it is a list of index of from 0 to the length of files minus 1
        self.finds = []
        # current playing file name
        self.current = None
        # previous playing file name
        self.previous = None
        # inds is a list of number that have same element as finds, but it have different order
        self.inds = None
        # indicator is only true when json exist and the player is started
        self.indicator = True
        # confessor is only true when json exist, and it's the first time that user drag and drop
        self.confessor = True
        # temp is the last assigned index
        self.temp = []
        # this is assigned when user first switch to dummy mode, used later to work out change in dummy mode
        self.dummy = []
        # volume
        self.val = 70
        # continue to play one song
        self.locked = False

    # if json exist and music has been added or deleted
    def comparison(self):
        cd = c.data
        if len(cd) == 0:
            return
        indir, inind = Module.get_init_files()
        for indices, f in enumerate(r.sample):
            if f not in indir:
                # f is deleted
                this_ind = r.sample.index(f)
                self.remove_one(f, this_ind)

        for indices, f in enumerate(indir):
            if f not in r.sample:
                # f is added
                this_ind = indir.index(f)
                self.add_one(f, this_ind)

    def add_one(self, f, this_ind):
        rei = [i for i in self.inds]
        r.sample.insert(0, f)
        self.inds = [this_ind]
        for i in rei:
            if i < this_ind:
                self.inds.append(i)
            else:
                self.inds.append(i + 1)

    def remove_one(self, f, this_ind):
        rei = [i for i in self.inds]
        r.sample.remove(f)
        self.inds = []
        rei.remove(this_ind)
        for i in rei:
            if i > this_ind:
                self.inds.append(i - 1)
            else:
                self.inds.append(i)

    def switch_false(self):
        self.switched = False

    def switch_true(self):
        self.switched = True

    def resort_false(self):
        self.resorted = False

    def resort_true(self):
        self.resorted = True

    def push_label_tags(self, arg):
        self.label_tags.append(arg)

    def push_label_nams(self, arg):
        self.label_nams.append(arg)

    def range_label_tags(self):
        for i in self.label_tags:
            yield i

    def range_label_nams(self):
        for i in self.label_nams:
            yield i

    def pause_false(self):
        self.paused = False

    def pause_true(self):
        self.paused = True

    def start_false(self):
        self.started = False

    def start_true(self):
        self.started = True

    @staticmethod
    def get_init_files():

        # file split error only occurs in MacOS due to .DS_store
        # pass in os path splitext object
        # return whether it's a music file
        # therefore use -1 instead of 1
        files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].split('.')[-1] in ['mp3', 'flac', 'wav', 'aif', 'aiff']]
        finds = [i for i in range(len(files))]
        return files, finds

    def init_files(self):
        self.files, self.finds = Module.get_init_files()

    @property
    def is_switched(self):
        return self.switched

    @property
    def is_resorted(self):
        return self.resorted

    @property
    def label_length(self):
        return len(self.label_tags)

    @property
    def get_label_nams(self):
        return self.label_nams

    @property
    def is_paused(self):
        return self.paused

    @property
    def is_started(self):
        return self.started

    @property
    def filing(self):
        arr = []
        for ind in self.finds:
            arr.append(self.files[ind])
        return arr

    def assign_current(self, filename):
        self.previous = self.current
        self.current = filename

    @property
    def get_current(self):
        return self.current

    @property
    def get_previous(self):
        return self.previous

    def get_label(self, labelname):
        return self.label_tags[self.label_nams.index(labelname)]

    def auto_labeling(self):
        if self.get_current is None and self.get_previous is None:
            return
        elif self.get_previous is None:
            cl = self.get_label(self.get_current)
            cl.config(bg='#40E0D0')
        else:
            pl = self.get_label(self.get_previous)
            cl = self.get_label(self.get_current)
            pl.config(bg='#F0F0ED')
            cl.config(bg='#40E0D0')

    @property
    def get_finds(self):
        return self.finds

    def assign_inds(self, ind):
        self.inds = [int(i) for i in ind]

    @property
    def get_inds(self):
        return self.inds

    @property
    def get_sample(self):
        return r.get_sample

    def indicator_false(self):
        self.indicator = False

    def indicator_true(self):
        self.indicator = True

    @property
    def get_indicator(self):
        return self.indicator

    @property
    def get_confessor(self):
        return self.confessor

    def confessor_false(self):
        self.confessor = False

    def confessor_true(self):
        self.confessor = True

    # label position from left top conner can be gained from winfo.rootx() and winfo.rooty()
    @property
    def sorted_label(self):
        arr = [x for x in self.label_tags]
        miarr = []
        while len(miarr) != len(self.label_tags):
            mi = arr[0]
            crr = arr[1:]
            for i in crr:
                if i.winfo_rooty() < mi.winfo_rooty():
                    mi = i
            arr.remove(mi)
            miarr.append(mi)
        return miarr

    # tkinter.cget fetches the property of widget
    @property
    def label_text(self):
        txt = []
        for i in self.sorted_label:
            txt.append(i.cget('text'))
        return txt

    # return change of initial to current after drag and drop
    @property
    def advanced_inds(self):
        arr = []
        if self.label_text[0] in self.get_dummy:
            for i in change(self.get_dummy, self.label_text):
                arr.append(c.past[i])
        else:
            for i in self.label_text:
                arr.append(self.filing.index(i))
        return arr

    def assign_temp(self, arr):
        self.temp = [x for x in arr]

    @property
    def get_temp(self):
        return self.temp

    def assign_dummy(self, arr):
        self.dummy = [x for x in arr]

    @property
    def get_dummy(self):
        return self.dummy

    def increase_val(self):
        if self.val >= 100:
            return
        self.val += 10
        set_volume(self.val)

    def decrease_val(self):
        if self.val <= 0:
            return
        self.val -= 10
        set_volume(self.val)

    @property
    def get_val(self):
        return self.val

    def lock_true(self):
        self.locked = True

    def lock_false(self):
        self.locked = False

    @property
    def get_lock(self):
        return self.locked

    def destroy_labels(self):
        self.label_tags = []
        self.label_nams = []

# generate a cache.json in hide mode to record playing sequence
class Cache:
    def __init__(self):
        self.cache = 'cache.json'

    @property
    def exist(self):
        try:
            with open(self.cache, 'r') as f:
                dt = json.load(f)
            return True
        except (IOError, json.decoder.JSONDecodeError) as e:
            return False

    def pre(self):
        try:
            file = open(self.cache, 'r')
            file.close()
        except IOError:
            file = open(self.cache, 'w')
            self.write({'seq': [x for x in range(r.length)]})
            os.system(f"attrib +h {self.cache}")
            file.close()

    # return data loaded from json file. if json is empty, excepted from if len(c.data) == 0
    @property
    def data(self):
        try:
            self.pre()
            with open(self.cache, 'r') as file:
                dt = json.load(file)
            return dt
        except json.decoder.JSONDecodeError:
            return {}

    # return label text before drag and drop
    @property
    def past(self):
        a = self.data
        if len(a) == 0:
            return [x for x in range(len(m.get_dummy))]
        else:
            return [x for x in c.data['seq']]

    # write json by pass in seq=[1, 3...]
    def assign(self, **kwargs):
        dt = self.data
        for key, value in kwargs.items():
            dt[key] = value
        self.write(dt)

    def mess(self):
        arr = [x for x in range(r.length)]
        shuffle(arr)
        self.write({"seq": arr})

    def write(self, data):
        os.system(f"attrib -h {self.cache}")
        with open(self.cache, 'w') as file:
            json.dump(data, file)
        os.system(f"attrib +h {self.cache}")

# hover effect to show text 
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Route class manage playing sequence of indices
class Route:
    def __init__(self, array):
        self.length = len(array)
        self.ind = 0

    def __iadd__(self, other):
        self.ind += other
        if self.ind == self.length:
            self.ind = 0
        return self

    def __isub__(self, other):
        self.ind -= other
        if self.ind < 0:
            self.ind = self.length - other
        return self

    def assign(self, value):
        self.ind = value

    @property
    def index(self):
        return self.ind

# Music class manage playing sequence of filenames
class Music:
    def __init__(self, total):
        self.total = total
        self.sample = [x for x in total]
        self.route = Route(total)

    @property
    def length(self):
        return len(self.total)

    @property
    def reverse(self):
        brr = []
        for i in self.total:
            brr.append(self.sample.index(i))
        return brr

    # four circumstance to call assi()   
    def assi(self, inds):
        if c.exist:
            # 1. json exist and the music player is first loaded
            if m.get_indicator:
                m.indicator_false()
                m.assign_inds(self.reverse)
                self.sample = []
                m.assign_inds(inds)
                for i in inds:
                    # except deletion
                    try:
                        self.sample.append(self.total[i])
                    except IndexError:
                        pass
                # handle potential file changes
                m.comparison()
            else:
                # 2. json exist and it's the first time the user drag and drop
                if m.get_confessor:
                    m.confessor_false()
                    arr = []
                    for i in change(m.get_finds, inds):
                        arr.append(self.sample[i])
                    self.sample = arr
                    m.assign_inds(self.reverse)
                    m.assign_temp(inds)
                else:
                    # 3. json exist and it's the second or more time the user drag and drop
                    arr = []
                    for i in change(m.get_temp, inds):
                        arr.append(self.sample[i])
                    self.sample = arr
                    m.assign_inds(self.reverse)
                    m.assign_temp(inds)
        else:
            # json doesn't exist
            self.sample = []
            m.assign_inds(inds)
            for i in inds:
                self.sample.append(self.total[i])
                
    # return filename
    def _prev(self):
        self.route -= 1
        f = self.sample[self.route.index]
        m.assign_current(f)
        m.auto_labeling()
        return f

    def _this(self):
        return self.sample[self.route.index]

    def _next(self, init=False):
        if init:
            self.route.assign(0)
        else:
            self.route += 1
        f = self.sample[self.route.index]
        m.assign_current(f)
        m.auto_labeling()
        return f

    @property
    def get_sample(self):
        return self.sample

# return a list of dummy text, only call once each time loading
def study_tools(num):
    array = [
    'Khan Academy', 'Wikipedia', 'Oxford Dictionary', 'Merriam-Webster Dictionary',
    'Bilingual Dictionary', 'Cambridge Dictionary', 'Literary Dictionary',
    'Collins French Dictionary', 'Routine', 'Snip Screen', 'Sticky Note', 'Screenshot',
    'Reminder', 'Todays Tasks', 'Calculator', 'Quick Note', 'Upcoming Events',
    'Homework', 'Screen Record', 'Empty Rycle Bin', 'Math Graph', 'Themometer',
    'Math Equation', 'Chemistry Periodic Table', 'Physics Common Constant',
    'Physics Common Equation', 'Calculus', 'TED Talk', 'Tomorrow Plan','Lessons',
    'Gradient Calc', 'Integral Calc', 'Triangle Solve', 'Organic Molecule', 'Sugar',
    'Fatty Acids', 'pH Calc', 'Length Contraction Calc', 'Lens Calc', 'Finished Task', 'History',
    ]
    arr = []
    if num < len(array):
        for i in range(num):
            arr.append(array[i])
    elif num == len(array):
        arr = [x for x in array]
    else:
        for i in range(num):
            if i > len(array) - 1:
                arr.append(array[i - len(array)])
            else:
                arr.append(array[i])
    m.assign_dummy(arr)
    return arr

def label_to_origin():
    origin = m.get_label_nams
    for i, lb in enumerate(m.range_label_tags()):
        lb.config(text=origin[i])
        lb.text = origin[i]

def label_to_dummy():
    dummy = study_tools(m.label_length)
    for i, lb in enumerate(m.range_label_tags()):
        lb.config(text=dummy[i])
        lb.text = dummy[i]

def fix():
    if m.get_lock:
        switchBTN.config(image=img_fix)
    else:
        switchBTN.config(image=img_switch)

# switch imgs
def switch():
    if m.is_switched:
        label_to_origin()
        m.switch_false()
        playBTN.config(image=img_play_btn)
        playBTN.image = img_play_btn
        stopBTN.config(image=img_stop_btn)
        stopBTN.image = img_stop_btn
        prevBTN.config(image=img_prev_btn)
        prevBTN.image = img_prev_btn
        nextBTN.config(image=img_next_btn)
        nextBTN.image = img_next_btn
    else:
        label_to_dummy()
        m.switch_true()
        playBTN.config(image=img_play_fkr)
        playBTN.image = img_play_fkr
        stopBTN.config(image=img_stop_fkr)
        stopBTN.image = img_stop_fkr
        prevBTN.config(image=img_prev_fkr)
        prevBTN.image = img_prev_fkr
        nextBTN.config(image=img_next_fkr)
        nextBTN.image = img_next_fkr

def lock():
    if m.get_lock:
        m.lock_false()
    else:
        m.lock_true()
    fix()

# support auto-play 
def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            if m.get_lock:
                this_music()
            else:
                next_music()

    root.after(1000, check_event)

# trigger by whitespace press and playBTN
def play_music():
    m.start_true()
    if m.is_resorted:
        m.resort_false()
        pygame.mixer.music.load(r._next(init=True))
        pygame.mixer.music.play()
    elif pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.load(r._next(init=True))
        pygame.mixer.music.play()

# trigger by whitespace press and stopBTN
def stop_music():
    pygame.mixer.music.pause()

# trigger by l press or lock button
def this_music():
    if m.get_lock:
        pygame.mixer.music.load(r._this())
        pygame.mixer.music.play()
    if m.is_paused:
        stop_music()

# trigger by right-arrow press or nextBTN
def next_music():
    if m.is_resorted:
        m.resort_false()
        pygame.mixer.music.load(r._next(init=True))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load(r._next())
        pygame.mixer.music.play()
    if m.is_paused:
        stop_music()

# trigger by left-arrow press or prevBTN
def prev_music():
    if m.is_resorted:
        m.resort_false()
        pygame.mixer.music.load(r._next(init=True))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load(r._prev())
        pygame.mixer.music.play()
    if m.is_paused:
        stop_music()

def shortcuts_info():
    return "`whitespace`: play\\pause\n`left-arrow`: play previous song\n`right-arrow`: play next song\n`up-arrow`: increase volumne\n`down-arrow`: decrease volume\n`r`: shuffle\n`m`: switch to dummy study tool tags\n`ctrl+s`: save current playing sequence\n`i`: show shortcuts information"

# trigger by i press or help->info
def user_guide():
    messagebox.showinfo('Shortcuts', shortcuts_info())

# trigger by ctrl+s or file->save
def save_files(e):
    if m.get_inds is None or len(m.get_inds) == 0:
        return
    c.assign(seq=m.advanced_inds)

# draggabel list Item
class Item(Frame):
    def __init__(self, master, value, width, height, selection_handler=None, drag_handler = None, drop_handler=None, **kwargs):

        kwargs.setdefault("class_", "Item")
        Frame.__init__(self, master, **kwargs)

        self._x = None
        self._y = None

        self._width = width
        self._height = height

        self._tag = "item%s"%id(self)
        self._value = value

        self._selection_handler = selection_handler
        self._drag_handler = drag_handler
        self._drop_handler = drop_handler

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def value(self):
        return self._value

    def init(self, container, x, y):
        self._x = x
        self._y = y

        self.place(in_=container, x=x, y=y, width=self._width, height=self._height)

        self.bind_class(self._tag, "<ButtonPress-1>", self._on_selection)
        self.bind_class(self._tag, "<B1-Motion>", self._on_drag)
        self.bind_class(self._tag, "<ButtonRelease-1>", self._on_drop)

        self._add_bindtag(self)

        list_of_widgets = list(self.children.values())
        while len(list_of_widgets) != 0:
            widget = list_of_widgets.pop()
            list_of_widgets.extend(widget.children.values())

            self._add_bindtag(widget)

    def _add_bindtag(self, widget):
        bindtags = widget.bindtags()
        if self._tag not in bindtags:
            widget.bindtags((self._tag,) + bindtags)

    def _on_selection(self, event):
        self.tkraise()

        self._move_lastx = event.x_root
        self._move_lasty = event.y_root

        if self._selection_handler:
            self._selection_handler(self)

    def _on_drag(self, event):
        self.master.update_idletasks()

        cursor_x = self._x + event.x
        cursor_y = self._y + event.y

        self._x += event.x_root - self._move_lastx
        self._y += event.y_root - self._move_lasty

        self._move_lastx = event.x_root
        self._move_lasty = event.y_root

        self.place_configure(x=self._x, y=self._y)

        if self._drag_handler:
            self._drag_handler(cursor_x, cursor_y)

    def _on_drop(self, event):
        if self._drop_handler:
            self._drop_handler()

    def set_position(self, x,y):
        self._x = x
        self._y = y
        self.place_configure(x =x, y =y)

    def move(self, dx, dy):
        self._x += dx
        self._y += dy

        self.place_configure(x =self._x, y =self._y)

# Draggable list frame
class DDList(Frame):
    def __init__(self, master, item_width, item_height, item_relief=None, item_background=None, item_borderwidth=None, offset_x=0, offset_y=0, gap=0, **kwargs):
        kwargs["width"] = item_width+offset_x*2
        kwargs["height"] = offset_y*2

        Frame.__init__(self, master, **kwargs)

        self._item_borderwidth = item_borderwidth
        self._item_relief = item_relief
        self._item_background = item_background
        self._item_width = item_width
        self._item_height = item_height

        self._offset_x = offset_x
        self._offset_y = offset_y

        self._left = offset_x
        self._top = offset_y
        self._right = self._offset_x + self._item_width
        self._bottom = self._offset_y

        self._gap = gap

        self._index_of_selected_item = None
        self._index_of_empty_container = None

        self._list_of_items = []
        self._position = {}

        self._new_y_coord_of_selected_item = None

    # trigger Music.assi(), which change playing sequence by changing inds (indices) then changing sample (filenames)
    def puts(self, _r):
        arr = []
        for i in self._list_of_items:
            arr.append(i._value)
        _r.assi(arr)

    def create_item(self, value=None, **kwargs):

        if self._item_relief is not None:
            kwargs.setdefault("relief", self._item_relief)

        if self._item_borderwidth is not None:
            kwargs.setdefault("borderwidth", self._item_borderwidth)

        if self._item_background is not None:
            kwargs.setdefault("background", self._item_background)

        item = Item(self.master, value, self._item_width, self._item_height, self._on_item_selected, self._on_item_dragged, self._on_item_dropped, **kwargs)
        return item

    def add_item(self, item, index=None):
        if index is None:
            index = len(self._list_of_items)
        else:
            if not -len(self._list_of_items) < index < len(self._list_of_items):
                raise ValueError("Item index out of range")

            for i in range(index, len(self._list_of_items)):
                _item = self._list_of_items[i]
                _item.move(0,  self._item_height + self._gap)

                self._position[_item] += 1

        x = self._offset_x
        y = self._offset_y + index * (self._item_height + self._gap)

        self._list_of_items.insert(index, item)
        self._position[item] = index

        item.init(self, x,y)

        if len(self._list_of_items) == 1:
            self._bottom += self._item_height
        else:
            self._bottom += self._item_height + self._gap

        self.configure(height=self._bottom + self._offset_y)

        return item

    def get_item(self, index):
        return self._list_of_items[index]

    def get_value(self, index):
        return self._list_of_items[index].value

    def _on_item_selected(self, item):
        self._index_of_selected_item = self._position[item]
        self._index_of_empty_container = self._index_of_selected_item

    def _on_item_dragged(self, x, y):

        if self._left < x < self._right and self._top < y < self._bottom:

            quotient, remainder = divmod(y-self._offset_y, self._item_height + self._gap)

            if remainder < self._item_height:

                new_container = quotient

                if new_container != self._index_of_empty_container:
                    if new_container > self._index_of_empty_container:
                        for index in range(self._index_of_empty_container+1, new_container+1, 1):
                            item = self._get_item_of_virtual_list(index)

                            item.move(0,-(self._item_height+self._gap))
                    else:
                        for index in range(self._index_of_empty_container-1, new_container-1, -1):
                            item = self._get_item_of_virtual_list(index)

                            item.move(0,self._item_height+self._gap)

                    self._index_of_empty_container = new_container

    def _get_item_of_virtual_list(self, index):
        if self._index_of_empty_container == index:
            raise Exception("No item in index: %s"%index)
        else:
            if self._index_of_empty_container != self._index_of_selected_item:
                if index > self._index_of_empty_container:
                    index -= 1

                if index >= self._index_of_selected_item:
                    index += 1
            item = self._list_of_items[index]
            return item

    def _on_item_dropped(self):
        item = self._list_of_items.pop(self._index_of_selected_item)
        self._list_of_items.insert(self._index_of_empty_container, item)

        x = self._offset_x
        y = self._offset_y + self._index_of_empty_container *(self._item_height + self._gap)

        item.set_position(x,y)

        for i in range(min(self._index_of_selected_item, self._index_of_empty_container),max(self._index_of_selected_item, self._index_of_empty_container)+1):
            item = self._list_of_items[i]
            self._position[item] = i

        self._index_of_empty_container = None
        self._index_of_selected_item = None
        # each time drop an item, restart playing sequence from top
        # change inds (indices) hence sample (filename) by puts => Music.assi()
        self.puts(r)
        m.resort_true()

class Tags:
    def __init__(self):
        self.sortable_list = DDList(root, 200, 35, offset_x=10, offset_y=10, gap =10, item_borderwidth=5, item_relief="groove")
        self.sortable_list.pack(expand=True, fill=BOTH)

    def reinit(self):
        self.sortable_list = DDList(root, 200, 35, offset_x=10, offset_y=10, gap =10, item_borderwidth=5, item_relief="groove")
        self.sortable_list.pack(expand=True, fill=BOTH)

    def trash(self):
        self.sortable_list.destroy()

    def tags_assign(self):
        for i, d in enumerate(m.get_sample):
            item = self.sortable_list.create_item(value=i)
            label = Label(item, text=d, cursor='fleur')
            label.config(font=("Arial", 14))
            label.config(bg='#F0F0ED')
            label.pack(anchor=W, padx= (4,0), pady= (4,0))
            # create tooltop to show text as hovering
            CreateToolTip(label, text=d)
            self.sortable_list.add_item(item)
            # make a copy of collected label tags and label names
            m.push_label_tags(label)
            m.push_label_nams(d)

    def tags_reassign(self):
        m.resort_true()
        c.mess()
        m.indicator_true()
        m.confessor_true()
        r.assi([int(i) for i in c.data['seq']])
        m.destroy_labels()
        self.trash()
        self.reinit()
        self.tags_assign()

def set_volume(val):
    pygame.mixer.music.set_volume(int(val)/100.0)

# keypress handle
def handle(event):
    if event.keysym == "space":
        if m.is_started:
            if not m.is_paused:
                m.pause_true()
                stop_music()
            else:
                m.pause_false()
                play_music()
        else:
            play_music()
    elif event.keysym == 'm':
        switch()
    elif event.keysym == 'l':
        lock()
    elif event.keysym == 'r':
        # shuffle
        t.tags_reassign()
    elif event.keysym == "Right":
        next_music()
    elif event.keysym == "Left":
        prev_music()
    elif event.keysym == 'Up':
        m.increase_val()
    elif event.keysym == 'Down':
        m.decrease_val()
    elif event.keysym == 'i':
        user_guide()

# ----- main -----
root = Tk()
root.title('Study Tools')
root.geometry("%dx%d%+d%+d"%(220, 1000, 0, 0))


# get absolute path of current directory
def abs_wrapper(rel):
    return os.getcwd() + '/' + rel


root.iconbitmap(abs_wrapper('img/icon.ico'))
# init class
m = Module()
c = Cache()

img_play_btn = PhotoImage(file=abs_wrapper('img/play-btn.png')).subsample(14)
img_stop_btn = PhotoImage(file=abs_wrapper('img/stop-btn.png')).subsample(14)
img_prev_btn = PhotoImage(file=abs_wrapper('img/prev-btn.png')).subsample(14)
img_next_btn = PhotoImage(file=abs_wrapper('img/next-btn.png')).subsample(14)

img_play_fkr = PhotoImage(file=abs_wrapper('img/note.png')).subsample(14)
img_stop_fkr = PhotoImage(file=abs_wrapper('img/mail.png')).subsample(14)
img_prev_fkr = PhotoImage(file=abs_wrapper('img/file.png')).subsample(14)
img_next_fkr = PhotoImage(file=abs_wrapper('img/pen.png')).subsample(14)

img_fix = PhotoImage(file=abs_wrapper('img/infinite.png')).subsample(14)
img_switch = PhotoImage(file=abs_wrapper('img/arrow.png')).subsample(14)

# init Module by directory default files
m.init_files()

if len(m.filing) > 18:
    messagebox.showerror('Too much music', f'Maximum number of music: 18\ncurrent files: {len(m.filing)}')
    exit()

# init Music module by Module recorded directory default files 
r = Music(m.filing)

# attempt to get data from json file
if len(c.data) != 0:
    r.assi([int(i) for i in c.data['seq']])

# init pygame (or mixer)
pygame.init()
# auto-play event
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

# tkinter window menu
# file -> save: save playing sequence
# help -> info: user guide shortcuts
menubar = Menu(root)
root.config(menu=menubar)

file = Menu(menubar)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Save', command=save_files)

help = Menu(menubar)
menubar.add_cascade(label='Help', menu=help)
help.add_command(label='Info', command=user_guide)

# Control Butttons should be above DDList frame
fra = Frame(root)

playBTN = Button(fra, image=img_play_btn, command=play_music)
playBTN.grid(row=0, column=2)
stopBTN = Button(fra, image=img_stop_btn, command=stop_music)
stopBTN.grid(row=0, column=3)
prevBTN = Button(fra, image=img_prev_btn, command=prev_music)
prevBTN.grid(row=0, column=4)
nextBTN = Button(fra, image=img_next_btn, command=next_music)
nextBTN.grid(row=0, column=5)

switchBTN = Button(fra, image=img_switch, command=lock)
switchBTN.grid(row=0, column=6)

fra.pack(fill=X, pady=(0, 10))

t = Tags()
t.tags_assign()

# control+s should be binded separated
# be aware that as press ctrl+s, ctrl press is triggered, since we can't have both 
root.bind_all("<KeyPress>", handle)
root.bind('<Control-s>', save_files)

# check if there is any music playing
check_event()

# show shortcuts in CLI
print(shortcuts_info())

root.mainloop()
# close pygame if tkinter is terminated
pygame.quit()
