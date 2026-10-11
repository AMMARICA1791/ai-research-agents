"""Benchmark suite for standardized AI tool evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List
from uuid import uuid4


@dataclass
class BenchmarkMetric:
    name: str
    description: str
    unit: str
    compute_fn: Callable[[Any], float] = field(default_factory=lambda: lambda x: 0.0)
    lower_is_better: bool = False


@dataclass
class BenchmarkTask:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    category: str = ""
    metrics: List[BenchmarkMetric] = field(default_factory=list)
    dataset_url: str = ""
    expected_runtime_seconds: float = 0.0


class BenchmarkSuite:
    def __init__(self):
        self.tasks: Dict[str, BenchmarkTask] = {}
        self._initialize_standard_benchmarks()

    def _initialize_standard_benchmarks(self) -> None:
        nlp_task = BenchmarkTask(
            name="GLUE Benchmark",
            description="General Language Understanding Evaluation",
            category="nlp",
            metrics=[
                BenchmarkMetric("accuracy", "Classification accuracy", "%"),
                BenchmarkMetric("f1_score", "Harmonic mean of precision/recall", "score"),
                BenchmarkMetric("inference_time", "Inference latency", "ms", lower_is_better=True),
            ],
            expected_runtime_seconds=3600,
        )
        self.tasks[nlp_task.name] = nlp_task

        vision_task = BenchmarkTask(
            name="ImageNet Evaluation",
            description="Large-scale visual recognition benchmark",
            category="vision",
            metrics=[
                BenchmarkMetric("top1_accuracy", "Top-1 accuracy", "%"),
                BenchmarkMetric("top5_accuracy", "Top-5 accuracy", "%"),
                BenchmarkMetric("latency", "Inference latency per image", "ms", lower_is_better=True),
                BenchmarkMetric("memory", "Peak memory usage", "MB", lower_is_better=True),
            ],
            expected_runtime_seconds=7200,
        )
        self.tasks[vision_task.name] = vision_task

    def get_benchmark(self, name: str) -> BenchmarkTask | None:
        return self.tasks.get(name)

    def list_benchmarks(self, category: str | None = None) -> List[BenchmarkTask]:
        if category:
            return [t for t in self.tasks.values() if t.category == category]
        return list(self.tasks.values())
