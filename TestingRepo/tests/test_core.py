from complex_app.core.data_structures import LinkedList, Node, Graph
from complex_app.core.utils import generate_random_string, format_date, is_valid_email
import unittest , datetime

class TestCore(unittest.TestCase):
    def test_linked_list(self):
        my_list = LinkedList()
        my_list.append(1)
        my_list.append(2)
        my_list.append(3)
        self.assertEqual(str(my_list), "1 -> 2 -> 3")

        my_list.insert_at_index(4, 1)
        self.assertEqual(str(my_list), "1 -> 4 -> 2 -> 3")

    def test_graph(self):
        my_graph = Graph()
        my_graph.add_edge("A", "B")
        my_graph.add_edge("A", "C")
        my_graph.add_edge("B", "C")
        self.assertEqual(my_graph.neighbors("A"), ["B", "C"])

    def test_generate_random_string(self):
        random_string = generate_random_string(10)
        self.assertEqual(len(random_string), 10)

    def test_format_date(self):
        date_obj = datetime.datetime.now()
        formatted_date = format_date(date_obj)
        self.assertTrue(formatted_date.startswith(date_obj.strftime("%Y-%m-%d")))

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("john.doe@example.com"))
        self.assertFalse(is_valid_email("invalid-email"))

if __name__ == '__main__':
    unittest.main()