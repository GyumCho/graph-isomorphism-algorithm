"""
Module for working with doubly linked lists.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687


class Node:
    """
    Node with data and references to next and previous nodes.
    """

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List with a head node and length attribute.
    """

    def __init__(self):
        self.head = None
        self.length = 0

    def insert(self, node):
        """
        Inserts a Node in the Doubly Linked List and increments its length by 1.
        """
        self.length += 1
        node.prev = None
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node

    def delete(self, node):
        """
        Deletes a Node from the Doubly Linked List and decrements its length by 1.
        """
        if self.head is None or node is None:
            return
        self.length -= 1
        if self.head == node:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if node.prev is not None:
            node.prev.next = node.next
