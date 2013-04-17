from pylibmodbus import ModbusTcp

# Example
mb = ModbusTcp("127.0.0.1", 1502)
mb.connect()
nb = 5

print("Write [0, 0, 0, 0, 0]")
data = [0] * nb
mb.write_registers(0, data)

print("Read")
data = mb.read_registers(0, nb)
for i, v in enumerate(data):
    print("%d: %d" % (i, v))

print("Write [0, 1, 2, 3, 4]")
data = list(range(nb))
mb.write_registers(0, data)

print("Read again")
data = mb.read_registers(0, nb)
for i, v in enumerate(data):
    print("%d: %d" % (i, v))

mb.close()
