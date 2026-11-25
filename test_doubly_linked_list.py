# 

import pytest
from doubly_linked_list import DoublyLinkedList


def test_append():
    dll = DoublyLinkedList[int]()
    dll.append(10)
    dll.append(20)

    assert len(dll) == 2
    assert dll.head.data == 10
    assert dll.tail.data == 20


def test_prepend():
    dll = DoublyLinkedList[int]()
    dll.prepend(20)
    dll.prepend(10)

    assert dll.head.data == 10
    assert dll.tail.data == 20


def test_insert_middle():
    dll = DoublyLinkedList[int]()

    dll.append(10)
    dll.append(30)
    dll.insert_at_index(1, 20)

    assert dll.find(20) == 1
    assert len(dll) == 3


def test_delete_middle():
    dll = DoublyLinkedList[int]()

    for value in [10, 20, 30]:
        dll.append(value)

    deleted = dll.delete_at_index(1)

    assert deleted == 20
    assert dll.find(20) == -1
    assert len(dll) == 2


def test_find():
    dll = DoublyLinkedList[int]()

    for value in [10, 20, 30]:
        dll.append(value)

    assert dll.find(20) == 1
    assert dll.find(99) == -1


def test_delete_first_and_last():
    dll = DoublyLinkedList[int]()

    for value in [10, 20, 30]:
        dll.append(value)

    assert dll.delete_at_index(0) == 10
    assert dll.delete_at_index(1) == 30

    assert dll.head.data == 20
    assert dll.tail.data == 20


def test_empty_list():
    dll = DoublyLinkedList[int]()

    assert dll.is_empty()
    assert len(dll) == 0


def test_invalid_index():
    dll = DoublyLinkedList[int]()

    with pytest.raises(IndexError):
        dll.delete_at_index(0)


def test_insert_invalid_index():
    dll = DoublyLinkedList[int]()

    with pytest.raises(IndexError):
        dll.insert_at_index(1, 10)
