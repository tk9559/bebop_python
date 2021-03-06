import socket
from pyparrot.Bebop import Bebop

s = socket.socket()

port = 8080
s.bind(('', port))  # socketに名前をつける

print("listening")
s.listen(5)  # 接続待ち
c, addr = s.accept()  # 接続要求の取り出し
c.settimeout(10)

bebop = Bebop(drone_type="Bebop2")

print("connecting to Bebop2")
success = bebop.connect(10)
print(success)

try:
    if (success):
        print("sleeping")
        bebop.smart_sleep(2)

    bebop.ask_for_state_update()

    # set safe indoor parameters
    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)

    # trying out the new hull protector parameters - set to 1 for a hull protection and 0 without protection
    bebop.set_hull_protection(1)

    while True:
        print("receiving")
        ch = c.recv(4096).decode()

        if ch == "t":
            print("take off")
            bebop.safe_takeoff(10)
            c.send(("controller received "+ch).encode('utf-8'))

        elif ch == "w":
            print("move front")
            bebop.fly_direct(roll=0, pitch=30, yaw=0,
                             vertical_movement=0, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "s":
            print("move back")
            bebop.fly_direct(roll=0, pitch=-30, yaw=0,
                             vertical_movement=0, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "a":
            print("move left")
            bebop.fly_direct(roll=-30, pitch=0, yaw=0,
                             vertical_movement=0, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "d":
            print("move right")
            bebop.fly_direct(roll=30, pitch=0, yaw=0,
                             vertical_movement=0, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))

        elif ch == "[A":
            print("move up")
            bebop.fly_direct(roll=0, pitch=0, yaw=0,
                             vertical_movement=10, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "[B":
            print("move down")
            bebop.fly_direct(roll=0, pitch=0, yaw=0,
                             vertical_movement=-10, duration=0.25)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "[C":
            print("move clockwise")
            bebop.fly_direct(roll=0, pitch=0, yaw=50,
                             vertical_movement=0, duration=0.1)
            c.send(("controller received "+ch).encode('utf-8'))
        elif ch == "[D":
            print("move conclockwise")
            bebop.fly_direct(roll=0, pitch=0, yaw=-50,
                             vertical_movement=0, duration=0.1)
            c.send(("controller received "+ch).encode('utf-8'))

        elif ch == "f":
            print("flip")
            bebop.flip(direction="front")
            c.send(("controller received "+ch).encode('utf-8'))

        elif ch == "l":
            print("land")
            bebop.safe_land(10)
            c.send(("controller received "+ch).encode('utf-8'))

        elif ch == "q" or len(ch) == 0:  # ソケットがSIGPIPEになったときも着地
            print("end")
            bebop.safe_land(10)
            c.send(("controller received "+ch).encode('utf-8'))
            c.close()
            break

    print("DONE - disconnecting")
    bebop.smart_sleep(5)
    print(bebop.sensors.battery)
    bebop.disconnect()

except:
    print("error!")
    bebop.safe_land(10)
    c.close()
    print("DONE - disconnecting")
    bebop.smart_sleep(5)
    print(bebop.sensors.battery)
    bebop.disconnect()
