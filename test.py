from barasingga import Barasingga

b = Barasingga()
b.print_board()
print(b.board)

a = b.available_actions(b.board, b.player)
print(a)
b.move(a[0])
a = b.available_actions(b.board, b.player)
print(a)
b.move(a[0])
