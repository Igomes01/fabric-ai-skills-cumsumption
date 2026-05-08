"""Manual CU (Compute Units) estimator.

Prompts the user for:
    1. Average input tokens per question
    2. Users per day
    3. Questions per user per day

Formulas (based on calc_fabric.ipynb):
    output_tokens = input_tokens * get_output_factor(input_tokens)
    cu_seconds    = (input_tokens*100 + output_tokens*400)/1000
    cu_minutes    = cu_seconds / 60
    cu_hours      = cu_seconds / 3600
    requests_day  = users_per_day * questions_per_user
    capacity_need = (requests_day * cu_hours) / 24

CLI usage example:
    python manual_cu_estimator.py --avg-input-tokens 80 --users-per-day 1500 --questions-per-user 5
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass

# AIC - Fator de saída dinâmico: quanto menor o avg_input_tokens, maior o fator.
# AIC - Inputs curtos geram respostas proporcionalmente mais longas.
# AIC - Escala suavizada até 2000 tokens para manter output médio entre 600-800.
def get_output_factor(avg_input_tokens: float) -> float:
    """AIC - Retorna o fator multiplicador de output tokens com base na
    quantidade média de tokens de entrada. Faixas definidas:
        ≤ 10      → 20
        11-30     → 15
        31-50     → 10
        51-70     → 8
        71-100    → 5
        101-150   → 4
        151-200   → 2
        201-400   → 1.0
        401-700   → 0.7
        701-1000  → 0.5
        1001-1500 → 0.35
        1501-2000 → 0.3
        > 2000    → 0.25
    """
    if avg_input_tokens <= 10:
        return 20
    if avg_input_tokens <= 30:
        return 15
    if avg_input_tokens <= 50:
        return 10
    if avg_input_tokens <= 70:
        return 8
    if avg_input_tokens <= 100:
        return 5
    if avg_input_tokens <= 150:
        return 4
    if avg_input_tokens <= 200:
        return 2
    if avg_input_tokens <= 400:
        return 1.0
    if avg_input_tokens <= 700:
        return 0.7
    if avg_input_tokens <= 1000:
        return 0.5
    if avg_input_tokens <= 1500:
        return 0.35
    if avg_input_tokens <= 2000:
        return 0.25
    return 0.25

@dataclass
class CapacityResult:
    input_tokens: float
    output_tokens: float
    cu_seconds: float
    cu_minutes: float
    cu_hours: float
    users_per_day: float
    questions_per_user: float
    requests_day: float
    capacity_need: float

    def to_rows(self):
        return [
            ("Input Tokens (avg)", f"{self.input_tokens:.2f}"),
            ("Output Tokens (estimated)", f"{self.output_tokens:.2f}"),
            ("CU Seconds (per request)", f"{self.cu_seconds:.4f}"),
            ("CU Minutes (per request)", f"{self.cu_minutes:.6f}"),
            ("CU Hours (per request)", f"{self.cu_hours:.8f}"),
            ("Users / Day", f"{self.users_per_day:.0f}"),
            ("Questions / User / Day", f"{self.questions_per_user:.2f}"),
            ("Requests / Day", f"{self.requests_day:.0f}"),
            ("Capacity Need (CU)", f"{self.capacity_need:.6f}"),
        ]


def compute_capacity(avg_input_tokens: float, users_per_day: float, questions_per_user: float) -> CapacityResult:
    if avg_input_tokens <= 0:
        raise ValueError("Average input tokens must be > 0")
    if users_per_day <= 0:
        raise ValueError("Users per day must be > 0")
    if questions_per_user <= 0:
        raise ValueError("Questions per user must be > 0")

    # AIC - Obtém o fator de output dinâmico baseado na faixa de input tokens
    factor = get_output_factor(avg_input_tokens)
    output_tokens = avg_input_tokens * factor
    cu_seconds = (avg_input_tokens * 100 + output_tokens * 400) / 1000
    cu_minutes = cu_seconds / 60
    cu_hours = cu_minutes / 60
    requests_day = users_per_day * questions_per_user
    capacity_need = (requests_day * cu_hours) / 24
    return CapacityResult(
        input_tokens=avg_input_tokens,
        output_tokens=output_tokens,
        cu_seconds=cu_seconds,
        cu_minutes=cu_minutes,
        cu_hours=cu_hours,
        users_per_day=users_per_day,
        questions_per_user=questions_per_user,
        requests_day=requests_day,
        capacity_need=capacity_need,
    )


def format_table(rows):
    width = max(len(label) for label, _ in rows) + 2
    lines = []
    for label, value in rows:
        lines.append(f"{label.ljust(width)}: {value}")
    return "\n".join(lines)


def interactive_flow():
    print("=== Manual Compute Units Estimator (Fabric) ===")
    while True:
        try:
            avg_input_tokens = float(input("Average input tokens per question: ").strip())
            users_per_day = float(input("Users per day: ").strip())
            questions_per_user = float(input("Questions per user per day: ").strip())
            result = compute_capacity(avg_input_tokens, users_per_day, questions_per_user)
            print("\nResults:\n")
            print(format_table(result.to_rows()))
            print(f"\nBase formula: cu_seconds = (input*100 + (input*factor)*400)/1000")
            print(f"Note: output factor = {get_output_factor(avg_input_tokens)} (based on input token range)")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            return
        again = input("\nRun again? (y/N): ").strip().lower()
        if again != 'y':
            break


def parse_args():
    p = argparse.ArgumentParser(description="Compute Units (Fabric) estimator based on average input tokens per question.")
    p.add_argument('--avg-input-tokens', type=float, help='Average input tokens per question.')
    p.add_argument('--users-per-day', type=float, help='Users per day.')
    p.add_argument('--questions-per-user', type=float, help='Questions per user per day.')
    return p.parse_args()


def main():
    args = parse_args()
    if args.avg_input_tokens and args.users_per_day and args.questions_per_user:
        result = compute_capacity(args.avg_input_tokens, args.users_per_day, args.questions_per_user)
        print(format_table(result.to_rows()))
    else:
        interactive_flow()


if __name__ == '__main__':
    main()
