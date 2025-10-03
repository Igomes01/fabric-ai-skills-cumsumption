"""Interactive Tokens & Capacity Calculator (English).

Prompts the user to paste multiple example questions (one per line) and
computes per-line and aggregate token metrics using `input_estimator`.

Optional capacity estimation (same formula as elsewhere):
  output_tokens = input_tokens * 4
  cu_seconds    = (input_tokens*100 + output_tokens*400)/1000
  cu_hours      = cu_seconds / 3600
  capacity_need = (requests_day * cu_hours) / 24

Supports JSON non-interactive mode.

CLI examples:
  python tokens_calculator.py
  python tokens_calculator.py --model gpt-4o-mini
  python tokens_calculator.py --json --text "Line A\nLine B"
  python tokens_calculator.py --json --capacity --users-per-day 1500 --questions-per-user 5 --text "What is sales by region?"
"""
from __future__ import annotations
import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Embedded analysis logic (merged from former input_estimator.py)
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gpt-4o-mini"
_FALLBACK_ENCODING = "cl100k_base"

try:
    import tiktoken  # type: ignore
except ImportError as e:  # pragma: no cover
    raise ImportError("tiktoken not installed. Run: pip install tiktoken") from e


def _get_encoding(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding(_FALLBACK_ENCODING)


def analyze_multiline(text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Analyze multi-line text returning per-line & aggregate metrics.

    Structure:
    {
      model, lines_count, lines:[{index,text,words,tokens}],
      total_words, total_tokens,
      avg_words_per_line, avg_tokens_per_line, tokens_per_word
    }
    Empty / whitespace-only lines are ignored.
    """
    lines_raw = [l.strip() for l in text.splitlines() if l.strip()]
    encoding = _get_encoding(model)

    per_line: List[Dict[str, Any]] = []
    total_words = 0
    total_tokens = 0

    for i, line in enumerate(lines_raw, start=1):
        words = len(line.split())
        tokens = len(encoding.encode(line))
        total_words += words
        total_tokens += tokens
        per_line.append({
            "index": i,
            "text": line,
            "words": words,
            "tokens": tokens,
        })

    count = len(per_line) or 1
    avg_words = total_words / count
    avg_tokens = total_tokens / count
    tokens_per_word = (total_tokens / total_words) if total_words else 0.0

    return {
        "model": model,
        "lines_count": len(per_line),
        "lines": per_line,
        "total_words": total_words,
        "total_tokens": total_tokens,
        "avg_words_per_line": avg_words,
        "avg_tokens_per_line": avg_tokens,
        "tokens_per_word": tokens_per_word,
    }

OUTPUT_FACTOR = 4  # output tokens = input tokens * 4

@dataclass
class LineResult:
    index: int
    text: str
    words: int
    tokens: int

@dataclass
class Aggregate:
    total_words: int
    total_tokens: int
    avg_words_per_line: float
    avg_tokens_per_line: float
    tokens_per_word: float


def read_multiline(prompt: str = "Paste questions (one per line). Finish with blank line:\n") -> str:
    print(prompt, end='')
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == '' and lines:
            break
        if line.strip() == '' and not lines:
            continue
        lines.append(line.rstrip('\n'))
    return '\n'.join(lines)


def analyze_block(text: str, model: str) -> Dict[str, Any]:
    data = analyze_multiline(text, model=model)
    lines = [LineResult(l['index'], l['text'], l['words'], l['tokens']) for l in data['lines']]
    agg = Aggregate(
        total_words=data['total_words'],
        total_tokens=data['total_tokens'],
        avg_words_per_line=data['avg_words_per_line'],
        avg_tokens_per_line=data['avg_tokens_per_line'],
        tokens_per_word=data['tokens_per_word'],
    )
    return {"lines": lines, "aggregate": agg, "model": data['model']}


def format_lines(lines: List[LineResult]) -> str:
    if not lines:
        return "(No lines)"
    w_idx = max(len(str(l.index)) for l in lines)
    w_words = max(len(str(l.words)) for l in lines)
    w_tokens = max(len(str(l.tokens)) for l in lines)
    header = f"# .{' '*(w_idx-1)}  WORDS{' '*(max(0,w_words-5))}  TOKENS{' '*(max(0,w_tokens-6))}  TEXT"
    sep = '-' * len(header)
    body = []
    for l in lines:
        body.append(f"{str(l.index).rjust(w_idx)}  {str(l.words).rjust(w_words)}  {str(l.tokens).rjust(w_tokens)}  {l.text}")
    return '\n'.join([header, sep, *body])


def format_aggregate(agg: Aggregate) -> str:
    total_lines = int(round(agg.total_words / agg.avg_words_per_line)) if agg.avg_words_per_line else len
    return (
        f"Total lines           : {total_lines}\n"
        f"Total words           : {agg.total_words}\n"
        f"Total tokens          : {agg.total_tokens}\n"
        f"Average words / line  : {agg.avg_words_per_line:.2f}\n"
        f"Average tokens / line : {agg.avg_tokens_per_line:.2f}\n"
        f"Tokens / word         : {agg.tokens_per_word:.4f}"
    )


def capacity_calc(avg_input_tokens: float, users_per_day: float, questions_per_user: float) -> Dict[str, float]:
    output_tokens = avg_input_tokens * OUTPUT_FACTOR
    cu_seconds = (avg_input_tokens * 100 + output_tokens * 400) / 1000
    cu_hours = cu_seconds / 3600
    requests_day = users_per_day * questions_per_user
    capacity_need = (requests_day * cu_hours) / 24
    return {
        "avg_input_tokens": avg_input_tokens,
        "output_tokens_est": output_tokens,
        "cu_seconds_per_request": cu_seconds,
        "cu_hours_per_request": cu_hours,
        "requests_day": requests_day,
        "capacity_need": capacity_need,
    }


def interactive(model: str):
    print("=== Tokens & Capacity Calculator ===")
    print(f"Model: {model}")
    text = read_multiline()
    if not text.strip():
        print("No text provided. Exiting.")
        return
    try:
        data = analyze_block(text, model)
    except Exception as e:  # pragma: no cover
        print(f"Error while analyzing: {e}", file=sys.stderr)
        return
    lines: List[LineResult] = data['lines']
    agg: Aggregate = data['aggregate']

    print("\n--- Per-line Metrics ---")
    print(format_lines(lines))
    print("\n--- Aggregates ---")
    print(format_aggregate(agg))

    if input("\nCompute capacity estimate? (y/N): ").strip().lower() == 'y':
        try:
            users = float(input("Users per day: ").strip())
            q_per_user = float(input("Questions per user per day: ").strip())
            cap = capacity_calc(agg.avg_tokens_per_line, users, q_per_user)
            print("\n--- Capacity Estimate ---")
            print(f"Avg input tokens / request : {cap['avg_input_tokens']:.2f}")
            print(f"Output tokens (est)        : {cap['output_tokens_est']:.2f}")
            print(f"CU Seconds / request       : {cap['cu_seconds_per_request']:.4f}")
            print(f"CU Hours / request         : {cap['cu_hours_per_request']:.8f}")
            print(f"Requests / day             : {cap['requests_day']:.0f}")
            print(f"Capacity Need (CU)         : {cap['capacity_need']:.6f}")
        except ValueError:
            print("Invalid numeric input. Skipping capacity section.")


def parse_args():
    p = argparse.ArgumentParser(description="Tokens & Capacity calculator (tiktoken-backed).")
    p.add_argument('--model', default=DEFAULT_MODEL, help='Model name (default: %(default)s).')
    p.add_argument('--json', action='store_true', help='JSON output mode (non-interactive).')
    p.add_argument('--text', help='Multiline text (use literal \n). Reads stdin if omitted in JSON mode.')
    p.add_argument('--capacity', action='store_true', help='Include capacity block in JSON output.')
    p.add_argument('--users-per-day', type=float, help='Users per day (JSON capacity).')
    p.add_argument('--questions-per-user', type=float, help='Questions per user per day (JSON capacity).')
    return p.parse_args()


def main():
    args = parse_args()
    if not args.json:
        interactive(args.model)
        return

    # JSON mode
    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        print(json.dumps({"error": "No text provided"}))
        return
    try:
        data = analyze_block(text, args.model)
    except Exception as e:  # pragma: no cover
        print(json.dumps({"error": str(e)}))
        return

    lines_ser = [dict(index=l.index, text=l.text, words=l.words, tokens=l.tokens) for l in data['lines']]
    agg: Aggregate = data['aggregate']
    output: Dict[str, Any] = {
        "model": data['model'],
        "totals": {
            "lines": len(lines_ser),
            "words": agg.total_words,
            "tokens": agg.total_tokens,
            "avg_words_per_line": agg.avg_words_per_line,
            "avg_tokens_per_line": agg.avg_tokens_per_line,
            "tokens_per_word": agg.tokens_per_word,
        },
        "lines": lines_ser,
    }
    if args.capacity:
        if args.users_per_day and args.questions_per_user:
            cap = capacity_calc(agg.avg_tokens_per_line, args.users_per_day, args.questions_per_user)
            output['capacity'] = cap
        else:
            output['capacity_error'] = 'users-per-day and questions-per-user required'
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
