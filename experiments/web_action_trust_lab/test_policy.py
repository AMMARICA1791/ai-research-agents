import unittest
from experiments.web_action_trust_lab.policy import Request, decide

class PolicyTests(unittest.TestCase):
    def req(self, action="read", origin="user", target="example.org", approved=False):
        return Request(action, origin, target, frozenset({"read","post","delete"}),
                       frozenset({"example.org"}), approved)

    def test_authorized_read(self):
        self.assertEqual(decide(self.req()), "ALLOW")

    def test_untrusted_web_instruction(self):
        self.assertEqual(decide(self.req(origin="webpage", action="post", approved=True)), "DENY")

    def test_social_instruction(self):
        self.assertEqual(decide(self.req(origin="social_post")), "DENY")

    def test_unapproved_post(self):
        self.assertEqual(decide(self.req(action="post")), "REVIEW")

    def test_approved_post(self):
        self.assertEqual(decide(self.req(action="post", approved=True)), "ALLOW")

    def test_out_of_scope_target(self):
        self.assertEqual(decide(self.req(target="attacker.example")), "DENY")

    def test_unknown_action(self):
        self.assertEqual(decide(self.req(action="execute", approved=True)), "DENY")

    def test_delete_requires_approval(self):
        self.assertEqual(decide(self.req(action="delete")), "REVIEW")

if __name__ == "__main__":
    unittest.main()
