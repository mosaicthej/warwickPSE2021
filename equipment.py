FULL_DICT = {
    '1':"Data Projector",
    '2':"Fixed Computer",
    '3':"Laptop Input",
    '4':"Plasma/ LCD Screen",
    '5':"Black board",
    '6':"White board",
    '7':"Lapel Microphone",
    '8':"Induction Loop",
    '9':"Document Camera",
    '10':"Bluray Player",
    '11':"Lecture Capture",
    '12':"Solstice Wireless Casting",
    '13':"Lecture Capture Camera",
    '14':"Touch Screen Monitor",
    '15':"Audio and Video Conferencing",
    '16':"Catchbox",
    '17':"Clevertouch",
    '18':"Dual Projection",
    '19':"Laptop Input (HDMI)",
    '20':"MS Teams Wireless Microphone",
    '21':"MS Teams Video Camera",
    '22':"MS Teams Enhanced AV",
}

FULL_SET = set(FULL_DICT.values())

def add_to_set(keys:list[str], current:set = {}) -> set:
    """adding one or more equipment to the current set
    Args:
        keys (list[str]): list of keys of the dictionary
        current (set, optional): current equipment in the set. Defaults to {}.
    Returns:
        set: updated set of equipment.
    """
    for k in keys:
        try:
            current = current.union(FULL_DICT[k])
        except KeyError:
            print(f"key {k} not valid!")
    return current