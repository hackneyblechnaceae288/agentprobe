"""AgentProbe Fuzzer — runs fuzz strategies against agents."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class FuzzResult:
    strategy_name: str
    total_variants: int
    passed: int
    failed: int
    errors: int
    failure_rate: float
    failed_variants: list[dict] = field(default_factory=list)
    duration_ms: float = 0.0


class Fuzzer:
    """Run fuzz strategies against an agent function.

    Free tier: up to 5 variants per strategy.
    Pro tier: unlimited variants, all strategies, parallel execution.
    """

    FREE_VARIANT_LIMIT = 5

    def __init__(
        self,
        agent: Any = None,
        run_fn: Optional[Callable] = None,
    ) -> None:
        if run_fn is not None:
            self._run_fn = run_fn
        elif agent is not None and hasattr(agent, "run"):
            self._run_fn = agent.run
        elif agent is not None and callable(agent):
            self._run_fn = agent
        else:
            self._run_fn = None

    def run(
        self,
        base_input: str = "",
        strategy: Any = None,
        assertions: Any = None,
        max_variants: Optional[int] = None,
        timeout_per_variant_ms: int = 30000,
        **kwargs,
    ) -> FuzzResult:
        if self._run_fn is None:
            raise ValueError("No agent or run_fn provided.")
        if strategy is None:
            from agentprobe.fuzz.strategies import PromptInjection
            strategy = PromptInjection()

        variants = strategy.generate_variants(base_input)
        limit = min(max_variants or self.FREE_VARIANT_LIMIT, self.FREE_VARIANT_LIMIT)
        variants = variants[:limit]

        passed = 0
        failed = 0
        errors = 0
        failed_variants: list[dict] = []
        start = time.monotonic()

        for variant in variants:
            try:
                output = self._run_fn(variant)
                if assertions:
                    if callable(assertions):
                        try:
                            result = assertions(output, variant)
                            if result is False:
                                failed += 1
                                failed_variants.append({"input": variant, "output": str(output)})
                                continue
                        except Exception as exc:
                            failed += 1
                            failed_variants.append({"input": variant, "error": str(exc)})
                            continue
                passed += 1
            except Exception as exc:
                errors += 1
                failed_variants.append({"input": variant, "error": str(exc)})

        elapsed = (time.monotonic() - start) * 1000
        total = passed + failed + errors

        return FuzzResult(
            strategy_name=type(strategy).__name__,
            total_variants=total,
            passed=passed,
            failed=failed,
            errors=errors,
            failure_rate=((failed + errors) / total * 100) if total > 0 else 0.0,
            failed_variants=failed_variants,
            duration_ms=elapsed,
        )

    def run_all(self, base_input: str = "", assertions: Any = None) -> list[FuzzResult]:
        """Run all available strategies. Pro strategies will raise NotImplementedError."""
        from agentprobe.fuzz.strategies import PromptInjection
        return [self.run(base_input=base_input, strategy=PromptInjection(), assertions=assertions)]
