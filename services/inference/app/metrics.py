from prometheus_client import Counter, Histogram

PREDICTION_REQUESTS = Counter(
    "lumina_prediction_requests_total",
    "Total number of prediction and recommendation requests",
)

PREDICTION_ERRORS = Counter(
    "lumina_prediction_errors_total",
    "Total number of failed prediction and recommendation requests",
)

PREDICTION_LATENCY = Histogram(
    "lumina_prediction_latency_ms",
    "Prediction and recommendation latency in milliseconds",
)

RATE_LIMIT_ERRORS = Counter(
    "lumina_rate_limit_errors_total",
    "Total number of rate limited requests",
)
