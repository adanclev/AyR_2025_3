class Node:
    def __init__(self, cost):
        self.cost = cost
        self.closed = False

    def toggle_closed_state(self):
        self.closed = not self.closed

    def __str__(self):
        return f"Node(cost={self.cost}, closed={self.closed})"