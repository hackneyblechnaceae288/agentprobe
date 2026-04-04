# v0.5.0 — Mega Update: 8 New Free Features

**27 new files | 4,187 lines of code | 8 CLI commands | 6 examples**

AgentProbe v0.5.0 is the biggest update yet — eight completely new modules, all free, all local, zero cloud dependency.

---

## New Features

### 1. Timeline — Time Travel Debugger

Step through your agent's execution like a VCR. Navigate forward and backward through every step, inspect tool I/O, LLM prompts and responses, and see costs accrued at each point.

**Key capabilities:**
- Step forward/backward with `step_forward()` and `step_back()`
- Jump to any position with `goto(5)`
- Set breakpoints on tool names, cost thresholds, token limits, errors, or custom predicates
- Run until breakpoint with `run()` and `run_back()`
- Jump to next tool/LLM/error with `next_tool()`, `next_llm()`, `next_error()`
- Full state inspection at every position (cumulative cost, tokens, tools called, errors)
- Interactive TUI mode with keyboard navigation
- Visual timeline bar rendering
- Diff between any two positions

```bash
agentprobe timeline recording.aprobe --interactive
agentprobe timeline recording.aprobe --breakpoint-tool web_search --breakpoint-cost 0.10
```

```python
from agentprobe.timeline import TimelineDebugger

dbg = TimelineDebugger(recording)
dbg.add_breakpoint_tool("web_search")
dbg.add_breakpoint_cost(0.10)
state = dbg.run()  # runs until breakpoint
print(f"Cost at breakpoint: ${state.cumulative_cost:.4f}")
```

---

### 2. DNA — Agent Behavioral Fingerprinting

Generate a unique multi-dimensional behavioral fingerprint for any agent. Enables drift detection, identity comparison, and behavioral clustering.

**10 behavioral traits measured:**
- Verbosity, Tool Diversity, Tool Frequency, Cost Efficiency, Speed
- Retry Tendency, Decisiveness, Depth, Memory Usage, Delegation

**Key capabilities:**
- Single-recording fingerprinting with `fingerprint()`
- Multi-recording averaged fingerprinting with `fingerprint_many()`
- Cosine similarity comparison between agents with `compare()`
- Drift detection with configurable threshold
- Visual DNA double-helix rendering
- Human-readable signature (e.g., `CeSp-VbTf-DeDp`)
- Deterministic SHA-256 hash for identity verification
- Step pattern extraction (e.g., `LTLTTTDL`)
- Tool and model usage profiles

```bash
agentprobe dna recording.aprobe
agentprobe dna recording.aprobe --compare other.aprobe
```

```python
from agentprobe.dna import AgentDNA

dna = AgentDNA()
fp = dna.fingerprint(recording)
print(fp.signature)  # "CeSp-VbTf-DeDp"

cmp = dna.compare(fp, fp2)
print(cmp.verdict)  # "similar" (89.2% similarity)
```

---

### 3. Chaos — Chaos Engineering for Agents

Systematically inject failures into agent execution to test resilience. 12 built-in scenarios covering tool failures, LLM degradation, resource exhaustion, and cascading failures.

**12 built-in scenarios:**
1. Tool Timeout Storm — All tool calls timeout
2. Garbage In, Garbage Out — Tools return random garbage
3. The Slow Lane — 10x latency on all tools
4. LLM Brain Freeze — Responses truncated to 50 tokens
5. Refusal Revolution — LLM refuses 50% of requests
6. Hallucination Station — Confidently wrong answers
7. Cost Explosion — 100x cost multiplier
8. Token Famine — 1000 token budget
9. Flaky Friend — 30% random failure rate
10. Domino Effect — Cascading failure chain
11. Selective Strike — Most-used tool always errors
12. LLM Amnesia — Context forgotten each turn

**Key capabilities:**
- Resilience scoring (0-100) with letter grades
- Recovery analysis (did the agent bounce back?)
- Per-injection tracking with step-level detail
- Custom scenario creation
- Reproducible runs with random seed
- Actionable recommendations based on failures

```bash
agentprobe chaos recording.aprobe
agentprobe chaos recording.aprobe --scenario "Tool Timeout Storm" --scenario "Domino Effect"
agentprobe chaos recording.aprobe --seed 42 --json-output
```

---

### 4. Coverage — Agent Path Coverage

Like code coverage, but for agent decision paths. Tracks which tools, branches, and strategies an agent has exercised across test runs.

**Coverage dimensions:**
- **Tool Coverage** (40% weight) — Which tools have been called vs. available
- **Branch Coverage** (25% weight) — Which decision types have been exercised
- **Step Type Coverage** (20% weight) — LLM calls, tool calls, decisions, handoffs, memory
- **Error Path Coverage** (15% weight) — Have error scenarios been tested?
- **Pattern Diversity** — Unique step sequence patterns discovered

**Key capabilities:**
- Multi-recording aggregation
- Automatic tool discovery from recordings and environment
- Uncovered tool/branch identification
- Step pattern sliding window analysis (2, 3, 4-gram)
- Error recovery path tracking
- Overall coverage grade (A+ to F)
- Actionable suggestions for improving coverage

```bash
agentprobe coverage
agentprobe coverage --path ./recordings --json-output
```

---

### 5. Snapshot — Snapshot Testing for Agent Behavior

Capture agent behavior as snapshots and detect regressions automatically. Like Jest snapshots but for AI agent outputs and decision patterns.

**What gets captured:**
- Output content hash
- Tools used (set and sequence)
- Step count and pattern
- LLM call count
- Total cost and tokens
- Decision summary
- Model used

**Key capabilities:**
- First run creates snapshot, subsequent runs compare
- Configurable tolerances (cost: 20%, tokens: 30%, steps: +/-3)
- Three severity levels: breaking, warning, info
- Snapshot update workflow with `--update` flag
- Snapshot listing and deletion
- JSON-based persistence (`.snap.json` files)

```bash
agentprobe snapshot recording.aprobe --name my_agent_test
agentprobe snapshot recording.aprobe --update
agentprobe snapshot recording.aprobe --list-all
```

---

### 6. Optimizer — Token and Prompt Optimization Engine

Analyzes agent recordings for optimization opportunities with projected cost savings.

**7 optimization analyzers:**
1. Redundant Prompts — Same system prompt repeated across calls
2. Model Downgrade — Opus to Sonnet, GPT-4o to GPT-4o-mini recommendations
3. Cache Opportunities — Low cache hit rate detection
4. Verbose Output — LLM responses over 1000 tokens
5. Redundant Tools — Same tool called with identical input
6. Batching — Sequential tool calls that could be parallelized
7. System Prompt Compression — Oversized system prompts (over 2000 words)

**Key capabilities:**
- Per-optimization savings calculation (USD and %)
- Confidence and effort ratings
- Actionable step-by-step fix instructions
- Monthly/yearly cost projections based on runs-per-day
- Token efficiency score (0-100)
- Multi-recording aggregated analysis
- ROI labeling (HUGE/HIGH/MEDIUM/LOW)

```bash
agentprobe optimize recording.aprobe
agentprobe optimize recording.aprobe --runs-per-day 500 --json-output
```

---

### 7. Watch — Live Monitoring Mode

Real-time file watcher that automatically re-runs tests and analyses when recordings or test files change. Like nodemon for AI agents.

**Monitors:**
- `.aprobe` recording files (new and modified)
- Test files (`test_*.py`, `*_test.py`)
- Config files (`agentprobe.yaml`)

**Key capabilities:**
- Configurable poll interval and debounce
- Event callbacks with decorator syntax
- Auto-run tests, health checks, roast, or X-ray on changes
- Non-blocking async mode available
- File change classification (recording added/modified, test modified, config modified)

```bash
agentprobe watch
agentprobe watch --health --roast --interval 2.0
```

---

### 8. NLTest — Natural Language Test Writer

Write agent tests in plain English. AgentProbe translates them to executable test code with proper assertions.

**Supported patterns (15+):**
- Cost: "cost below $0.10", "spend less than $1"
- Latency: "respond in under 5 seconds", "faster than 200ms"
- Tools: "call the search tool", "use calculator at least 3 times", "never call delete"
- Output: "output contains hello", "response is not empty", "output is valid JSON"
- Steps: "use less than 10 steps"
- Tokens: "use under 5k tokens"
- Security: "no PII in output"
- Success: "complete successfully", "no errors"

**Key capabilities:**
- Single assertion translation with confidence scoring
- Full test function generation with docstrings
- Complete test file generation with imports
- Unmatched description tracking (marked as TODO)
- Custom pattern registration
- Time unit auto-conversion (seconds, ms, minutes)
- Token shorthand support (5k = 5000)

```bash
agentprobe nltest "respond in under 5 seconds" "cost below $0.10" "call the search tool"
agentprobe nltest "no PII in output" "no errors" -n test_safety -o tests/test_safety.py
```

---

## Updated Files

- `agentprobe/__init__.py` — Version bumped to 0.5.0
- `agentprobe/cli/main.py` — 8 new CLI commands added (+447 lines)
- `pyproject.toml` — Version bumped to 0.5.0
- `CHANGELOG.md` — v0.5.0 entry with all new features
- `README.md` — New feature cards, CLI reference, Free vs Pro table, code examples

## New Files (27)

```
agentprobe/timeline/__init__.py       agentprobe/timeline/debugger.py
agentprobe/dna/__init__.py            agentprobe/dna/fingerprint.py
agentprobe/chaos/__init__.py          agentprobe/chaos/engine.py
agentprobe/coverage/__init__.py       agentprobe/coverage/tracker.py
agentprobe/snapshot/__init__.py       agentprobe/snapshot/manager.py
agentprobe/optimizer/__init__.py      agentprobe/optimizer/engine.py
agentprobe/watch/__init__.py          agentprobe/watch/watcher.py
agentprobe/nltest/__init__.py         agentprobe/nltest/generator.py
examples/timeline_example.py          examples/chaos_example.py
examples/nltest_example.py            examples/dna_example.py
examples/coverage_example.py          examples/optimizer_example.py
```
