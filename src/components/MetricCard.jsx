export default function MetricCard({ metricLabel, metricValue }) {
    return (
        <div className="glass-card metric-card-1">
            <label>{metricLabel}</label>
            <span>{metricValue}</span>
        </div>
    )
}