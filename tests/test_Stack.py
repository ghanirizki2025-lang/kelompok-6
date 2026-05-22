import unittest

class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class CustomStack:
    def __init__(self):
        self.top_node = None
        self.count = 0

    def push(self, value):
        new_node = StackNode(value)
        new_node.next = self.top_node
        self.top_node = new_node
        self.count += 1

    def pop(self):
        if self.is_empty():
            print("[ERROR] Stack Underflow! Tumpukan kosong.")
            return None
        removed_value = self.top_node.value
        self.top_node = self.top_node.next
        self.count -= 1
        return removed_value

    def peek(self):
        if self.is_empty():
            return None
        return self.top_node.value

    def is_empty(self):
        return self.top_node is None

    def size(self):
        return self.count

    def display(self):
        if self.is_empty():
            print("[INFO] Stack is empty.")
            return
        current = self.top_node
        print("\n=== STACK VIEW (TOP -> BOTTOM) ===")
        while current:
            print(f"| {current.value} |")
            current = current.next
        print("==================================")

class TestCustomStackMurni(unittest.TestCase):
    def setUp(self):
        self.stack = CustomStack()

    def test_stack_operations(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertIsNone(self.stack.peek())
        
        self.stack.push("Buku A")
        self.stack.push("Buku B")
        self.stack.push("Buku C")
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.peek(), "Buku C")
        
        self.assertEqual(self.stack.pop(), "Buku C")
        self.assertEqual(self.stack.peek(), "Buku B")
        self.assertEqual(self.stack.size(), 2)
        
        self.assertEqual(self.stack.pop(), "Buku B")
        self.assertEqual(self.stack.pop(), "Buku A")
        
        self.assertTrue(self.stack.is_empty())
        self.assertIsNone(self.stack.pop())
        self.assertIsNone(self.stack.peek())

if __name__ == "__main__":
    unittest.main()