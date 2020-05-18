import sysv_ipc as ipc

def main():
    path = "/tmp"
    key = ipc.ftok(path, 2333)
    shm = ipc.SharedMemory(key, ipc.IPC_CREAT, 0600, 1024)  
    shm.write("12343 t2", 0)
    shm.write("01010101", 8)
    buf = shm.read(8, 0)
    print("Text: " + buf);
    print("LEDS: " + shm.read(8, 8))
    print("Buttons: " + shm.read(8, 16))
    shm.detach()
    pass

if __name__ == '__main__':
    main()