from doubly_linked_list import DoublyLinkedList

angka = DoublyLinkedList[int]()

angka.append(10)
angka.append(20)
angka.append(30)

# Kesalahan tipe data yang disengaja
angka.append("INI TEKS")