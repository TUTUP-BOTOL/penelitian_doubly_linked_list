
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class Node(Generic[T]):
    __slots__ = ("data", "prev", "next")

    def __init__(self, data: T) -> None:
        self.data: T = data
        self.prev: Optional["Node[T]"] = None
        self.next: Optional["Node[T]"] = None


class DoublyLinkedList(Generic[T]):

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.size: int = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def append(self, data: T) -> None:
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None

            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, data: T) -> None:
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def _get_node(self, index: int) -> Node[T]:
        if index < 0 or index >= self.size:
            raise IndexError("Index di luar jangkauan")

        if index < self.size // 2:
            current = self.head

            for _ in range(index):
                assert current is not None
                current = current.next

        else:
            current = self.tail

            for _ in range(self.size - 1 - index):
                assert current is not None
                current = current.prev

        assert current is not None
        return current

    def insert_at_index(self, index: int, data: T) -> None:
        if index < 0 or index > self.size:
            raise IndexError("Index di luar jangkauan")

        if index == 0:
            self.prepend(data)
            return

        if index == self.size:
            self.append(data)
            return

        current = self._get_node(index)

        assert current.prev is not None

        new_node = Node(data)

        new_node.prev = current.prev
        new_node.next = current

        current.prev.next = new_node
        current.prev = new_node

        self.size += 1

    def delete_at_index(self, index: int) -> T:
        current = self._get_node(index)

        if current.prev is not None:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next is not None:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        self.size -= 1

        return current.data

    def find(self, value: T) -> int:
        current = self.head
        index = 0

        while current is not None:
            if current.data == value:
                return index

            current = current.next
            index += 1

        return -1
