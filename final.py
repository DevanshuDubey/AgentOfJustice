import pandas as pd
import math
import os
from groq import Groq
from agents.lawyer import DefenseLawyer, ProsecutionLawyer
from agents.judge import Judge
from agents.witness import create_witness
from agents.defendant import Defendant
from agents.plaintiff import Plaintiff
from core.trial_manager import TrialManager
from dotenv import load_dotenv

load_dotenv()

def split_case_description(description, chunk_size=2000):
    words = description.split()
    num_chunks = math.ceil(len(words) / chunk_size)
    chunks = [' '.join(words[i*chunk_size: (i+1)*chunk_size]) for i in range(num_chunks)]
    return chunks

def main():
    file_path = "cases.csv"
    output_file = "output.csv"
    
    cases = pd.read_csv(file_path)
    total_cases = len(cases)
    print("\n🎯 Running courtroom simulation on 50 cases...\n")

    client = Groq(api_key=os.getenv("GROQ_API_KEY_78060"))

    results = []

    for case_number in range(50):
        try:
            case_description = cases.iloc[case_number]['text']

            print(f"⚖️ Running case #{case_number}:")
            print(f"   📄 Description: {case_description[:100]}...")

            prosecution = ProsecutionLawyer()
            defense = DefenseLawyer()
            judge = Judge()
            defendant = Defendant()
            plaintiff = Plaintiff()
            witnesses = [create_witness(
                name="witness1",
                background="Ordinary background",
                testimony="She is a witness to this case."
            )]

            trial = TrialManager(
                prosecution=prosecution,
                defense=defense,
                judge=judge,
                defendant=defendant,
                plaintiff=plaintiff,
                witnesses=witnesses
            )

            summary = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": "You are summarizing legal cases for trial. Summary in 7-8 sentences. Only say most important info for the cases"},
                    {"role": "user", "content": case_description}
                ],
                temperature=0.7,
                max_tokens=300,
            )

            summary_text = summary.choices[0].message.content.strip()

            trial.run_opening_statements(summary_text)
            trial.run_witness_interrogation()
            trial.run_closing_statements()
            final_judgement = trial.run_judgement()

            results.append({
                "label": final_judgement
            })

        except Exception as e:
            print(f"❌ Error in case {case_number}: {e}")
            results.append({
                "judge_ruling": f"Error: {e}"
            })

    output_df = pd.DataFrame(results)
    output_df[id] = cases["id"]
    output_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved all judge rulings to {output_file}")

if __name__ == "__main__":
    main()
