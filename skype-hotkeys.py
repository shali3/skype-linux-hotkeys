#!/usr/bin/python2
import dbus
import time
bus = dbus.SessionBus()
skype = bus.get_object('com.Skype.API', '/com/Skype')
skype.Invoke('NAME Answering-Server')
skype.Invoke('PROTOCOL 8')
import sys
args = sys.argv[1:]
command = args[0]
if command == '-m':
    command = "MUTE ON"
    if skype.Invoke('GET MUTE') == "MUTE ON":
        command = "MUTE OFF"
    skype.Invoke(command)
elif command == '-c':
    print skype.Invoke(" ".join(args[1:]))
elif command == '-a':
    call_id = skype.Invoke("SEARCH ACTIVECALLS").split()[1]
    print skype.Invoke('ALTER CALL ' + call_id + ' ANSWER')
    time.sleep( 2 )
    print skype.Invoke('ALTER CALL ' + call_id + ' HOLD')
    time.sleep( 2 )
    print skype.Invoke('ALTER CALL ' + call_id + ' RESUME')
elif command == '-h':
    call_id = skype.Invoke("SEARCH ACTIVECALLS").split()[1]
    skype.Invoke('ALTER CALL ' + call_id + ' HANGUP')
elif command == '-c':
    import ConfigParser
    config = ConfigParser.ConfigParser()
    from os.path import join, expanduser, dirname
    hotkeys_dir = dirname(sys.argv[0])
    config.read(join(hotkeys_dir, 'skype-hotkeys.cfg'))
    (number, code) = config.get('skype-hotkeys', ' '.join(args[1:])).split()
    res = skype.Invoke('CALL ' + number).split()
    call_id = res[1]
    import time
    status = res[3]
    while status != 'INPROGRESS':
        time.sleep(1)
        res = skype.Invoke('GET CALL ' + call_id + ' STATUS').split()
        status = res[3]
    time.sleep(1)
    for c in code:
        time.sleep(0.3)
        skype.Invoke('SET CALL ' + call_id + ' DTMF ' + c)
