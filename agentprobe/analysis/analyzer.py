"""AgentProbe Analyzer — Cost, latency, drift, and failure analysis.

Basic analysis is included. Advanced analysis (drift detection,
failure classification, token waste) is available in AgentProbe Pro.

Learn more: https://agentprobe.dev/pro
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union

from agentprobe.core.models import AgentRecording


@dataclass
class CostReport:
    total_cost: float
    avg_cost: float
    by_group: dict
    recordings_count: int


class Analyzer:
    """Agent analysis engine.

    Free tier includes: basic cost analysis.
    Pro tier adds: latency percentiles, drift detection, failure classification,
    token waste analysis, comparative runs.
    """

    def _load_recordings(self, recordings: Union[str, List[AgentRecording]]) -> List[AgentRecording]:
        if isinstance(recordings, list):
            return recordings
        path = Path(recordings) if not isinstance(recordings, Path) else recordings
        if path.is_file():
            return [AgentRecording.load(path)]
        results = []
        for f in sorted(path.parent.glob(path.name)):
            try:
                results.append(AgentRecording.load(f))
            except Exception:
                continue
        return results

    def cost_analysis(
        self,
        recordings: Union[str, List[AgentRecording]],
        group_by: str = "model",
    ) -> CostReport:
        """Basic cost analysis — included in free tier."""
        recs = self._load_recordings(recordings)
        if not recs:
            return CostReport(total_cost=0, avg_cost=0, by_group={}, recordings_count=0)

        total = sum(r.total_cost for r in recs)
        avg = total / len(recs) if recs else 0

        groups: dict[str, list[float]] = {}
        for r in recs:
            if group_by == "model":
                key = r.environment.model if r.environment else "unknown"
            elif group_by == "framework":
                key = r.metadata.agent_framework
            elif group_by == "tag":
                for tag in (r.metadata.tags or ["untagged"]):
                    groups.setdefault(tag, []).append(r.total_cost)
                continue
            else:
                key = "all"
            groups.setdefault(key, []).append(r.total_cost)

        by_group = {}
        for k, costs in groups.items():
            by_group[k] = {
                "total": sum(costs),
                "avg": sum(costs) / len(costs),
                "count": len(costs),
            }

        return CostReport(
            total_cost=total,
            avg_cost=avg,
            by_group=by_group,
            recordings_count=len(recs),
        )

    def latency_analysis(self, recordings=None, **kwargs):
        """Advanced latency analysis — available in AgentProbe Pro."""
        raise NotImplementedError(
            "Latency analysis is available in AgentProbe Pro. "
            "Upgrade at https://agentprobe.dev/pro"
        )

    def detect_drift(self, baseline=None, current=None, **kwargs):
        """Drift detection — available in AgentProbe Pro."""
        raise NotImplementedError(
            "Drift detection is available in AgentProbe Pro. "
            "Upgrade at https://agentprobe.dev/pro"
        )

    def failure_analysis(self, recordings=None, **kwargs):
        """Failure classification — available in AgentProbe Pro."""
        raise NotImplementedError(
            "Failure analysis is available in AgentProbe Pro. "
            "Upgrade at https://agentprobe.dev/pro"
        )

    def token_waste(self, recordings=None, **kwargs):
        """Token waste detection — available in AgentProbe Pro."""
        raise NotImplementedError(
            "Token waste analysis is available in AgentProbe Pro. "
            "Upgrade at https://agentprobe.dev/pro"
        )

    def compare_runs(self, run_a=None, run_b=None, **kwargs):
        """Comparative analysis — available in AgentProbe Pro."""
        raise NotImplementedError(
            "Comparative analysis is available in AgentProbe Pro. "
            "Upgrade at https://agentprobe.dev/pro"
        )
