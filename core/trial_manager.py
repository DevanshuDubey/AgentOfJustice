



class TrialManager:
    judge_outputs = []
    def __init__(self, prosecution, defense, judge, plaintiff=None, defendant=None, witnesses=None):
        self.prosecution = prosecution
        self.defense = defense
        self.judge = judge
        self.plaintiff = plaintiff
        self.defendant = defendant
        self.witnesses = witnesses or []

    def run_opening_statements(self, case_background: str):
        #print("=== OPENING STATEMENTS ===\n")

        prosecutor_msg = self.prosecution.respond(
            f"Court: Present your opening statement. Case background:\n{case_background}"
        )
        #print("🧑‍⚖️ PROSECUTION:\n", prosecutor_msg, "\n")

        defense_msg = self.defense.respond(
            "Court: Respond with your opening statement."
        )
        #print("🛡️ DEFENSE:\n", defense_msg, "\n")

        if self.plaintiff:
            plaintiff_msg = self.plaintiff.respond(
                "Court: Present the opening statement for the Plaintiff."
            )
            #print("👩‍⚖️ PLAINTIFF:\n", plaintiff_msg, "\n")

        if self.defendant:
            defendant_msg = self.defendant.respond(
                "Court: Defendant may make a statement if desired."
            )
            #print("🧑‍⚖️ DEFENDANT:\n", defendant_msg, "\n")

    def run_witness_interrogation(self):
        #print("=== WITNESS TESTIMONY ===\n")

        for witness in self.witnesses:
            #print(f"👁️ WITNESS: {witness.name}\n")

            q1 = self.prosecution.respond(f"Court: Question witness {witness.name}.")
            #print("🧑‍⚖️ PROSECUTION:\n", q1)
            a1 = witness.respond(q1)
            #print("👁️ WITNESS:\n", a1, "\n")

            q2 = self.defense.respond(f"Court: Cross-examine witness {witness.name}.")
            #print("🛡️ DEFENSE:\n", q2)
            a2 = witness.respond(q2)
            #print("👁️ WITNESS:\n", a2, "\n")

            if self.plaintiff:
                q3 = self.plaintiff.respond(f"Court: Plaintiff cross-examines witness {witness.name}.")
                #print("👩‍⚖️ PLAINTIFF:\n", q3)
                a3 = witness.respond(q3)
                #print("👁️ WITNESS:\n", a3, "\n")

    def run_closing_statements(self):
        #print("=== CLOSING STATEMENTS ===\n")

        close_p = self.prosecution.respond("Court: Give your closing argument.")
        #print("🧑‍⚖️ PROSECUTION:\n", close_p, "\n")

        close_d = self.defense.respond("Court: Give your closing argument.")
        #print("🛡️ DEFENSE:\n", close_d, "\n")

        if self.plaintiff:
            close_p = self.plaintiff.respond("Court: Give your closing argument.")
            #print("👩‍⚖️ PLAINTIFF:\n", close_p, "\n")

    def run_judgement(self):
        #print("=== JUDGE'S VERDICT ===\n")

        combined_history = (
            self.prosecution.history +
            self.defense.history +
            (self.plaintiff.history if self.plaintiff else []) +
            (self.defendant.history if self.defendant else [])
        )

        summary = "\n\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in combined_history if m['role'] != "system"
        )

        verdict = self.judge.respond(
            f"Court: Based on this case transcript, issue your final verdict:\n{summary}"
        )
        #print("========THE FINAL VERDICT OF THE CASE IS: ==========\n"+verdict)
        return verdict
