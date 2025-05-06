"""A diagnosis of the message metrics."""

from mas.communication.message_metric import MessageMetric


class MetricDiagnosis:
    """Metric diagnosis class.

    This class contains the diagnosis of the message metrics.
    """

    def __init__(self, diagnosis: str) -> None:
        """Initialise the metric diagnosis.

        Args:
            diagnosis (str): The diagnosis of the message metrics.
        """
        self.diagnosis = diagnosis
        """The diagnosis of the message metrics."""

    def metrics_satisfy_diagnosis(self, metrics: list[MessageMetric]) -> bool:
        """Check if the metrics satisfy the diagnosis.

        Args:
            metrics (list[MessageMetric]): The list of metrics to check.

        Returns:
            bool: True if the metrics satisfy the diagnosis, False otherwise.
        """
        raise NotImplementedError(
            "metrics_satisfy_diagnosis method not implemented in MetricDiagnosis class. Please implement it in the subclass."
        )
